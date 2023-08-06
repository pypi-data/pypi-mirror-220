import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import List

import googlemaps
import requests

from gandai import gpt, helpers, models, query, secrets
from gandai.models import Search

gmaps = googlemaps.Client(key=secrets.access_secret_version("GOOLE_MAPS_KEY"))
MAX_WORKERS = 25


class GoogleMapsWrapper:
    @staticmethod
    def get_loc(text: str = "San Diego, CA") -> tuple:
        resp = gmaps.geocode(text)
        return tuple(resp[0]["geometry"]["location"].values())

    @staticmethod
    def enrich(place_id: str) -> dict:
        resp = gmaps.place(place_id=place_id)
        return resp["result"]

    @staticmethod
    def fetch_unique_place_ids(
        search_phrase: str, locations: List[str], radius_miles: int = 25
    ) -> list:
        main_func = partial(
            GoogleMapsWrapper._fetch_place_ids,
            search_phrase=search_phrase,
            radius_miles=radius_miles,
        )
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as exec:
            futures = exec.map(main_func, locations)

        place_ids = []
        for future in futures:
            try:
                place_ids.extend(list(future))
            except Exception as e:
                print(e)

        place_ids = list(set(place_ids))
        len(place_ids)
        return place_ids

    @staticmethod
    def _fetch_place_ids(
        location_text: str, search_phrase: str, radius_miles: int = 25
    ) -> list:
        try:
            METERS_PER_MILE = 1609.34
            radius_meters = radius_miles * METERS_PER_MILE

            loc: tuple = GoogleMapsWrapper.get_loc(location_text)

            results = []

            response = gmaps.places(
                query=search_phrase,
                location=loc,
                radius=radius_meters,
            )

            results.extend(response["results"])
            next_page_token = response.get("next_page_token", None)
            while next_page_token:
                time.sleep(2)
                response = gmaps.places(
                    query=search_phrase,
                    location=loc,
                    radius=radius_meters,
                    page_token=next_page_token,
                )
                results.extend(response["results"])
                next_page_token = response.get("next_page_token", None)

            place_ids = [result["place_id"] for result in results]
            print(
                f"{search_phrase} in {location_text} within {radius_miles} miles -> {len(place_ids)} results"
            )
            return place_ids
        except Exception as e:
            print(f"Error with {location_text} {search_phrase}: {e}")
            return []

    @staticmethod
    def build_target_from_place_id(
        place_id: str, search_uid: int, append_to_prompt: str = None
    ) -> models.Company:
        """takes in an (eriched) place and inserts it as a company"""
        # really more of an upsert, but multiple txns for now

        place = GoogleMapsWrapper.enrich(place_id)

        existing_search_domains = query.unique_domains(search_uid=search_uid)[
            "domain"
        ].to_list()

        if "website" not in place:
            print(f"no website for {place_id}")
            return

        if helpers.clean_domain(place["website"]) in existing_search_domains:
            print(f"skipping {place['website']} - already in search_uid {search_uid}")
            return

        gpt_prompt = (" ").join(
            [
                f"Q: Based on these reviews:",
                f"{[review['text'] for review in place['reviews']]}",
                f"as well as what you already know about {place['website']},",
                f"what products and services does {place['name']} offer?",
            ]
        )
        if append_to_prompt:
            gpt_prompt += " " + append_to_prompt
        # print(gpt_prompt)

        company = models.Company(
            name=place["name"],
            domain=helpers.clean_domain(place["website"]),
            description="",
        )

        query.insert_company(company)  # on conflict does nothing

        # save the place in meta
        company = query.find_company_by_domain(company.domain)
        if "google_places" not in company.meta:
            company.meta["google_places"] = {}
        company.meta["google_places"][place_id] = place
        query.update_company(company)
        ###

        print(f"adding {company.domain} - search_uid {search_uid}")
        query.insert_event(
            models.Event(
                search_uid=search_uid,
                actor_key="chatgpt",
                type="comment",
                domain=company.domain,
                data={"comment": f"chatgpt - {gpt.ask_gpt(gpt_prompt)}"},
            )
        )

        query.insert_event(
            models.Event(
                search_uid=search_uid,
                actor_key="google",
                type="create",
                domain=company.domain,
            )
        )

        return company

    def build_place_ids_async(place_ids: list, search: models.Search):
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for place_id in place_ids:
                executor.submit(
                    GoogleMapsWrapper.build_target_from_place_id,
                    place_id=place_id,
                    search_uid=search.uid,
                )


class GrataWrapper:
    HEADERS = {
        "Authorization": secrets.access_secret_version("GRATA_API_TOKEN"),
        "Content-Type": "application/json",
    }

    def find_similar(domain: str, search: models.Search) -> list:
        api_filters = GrataWrapper._get_api_filter(search)
        response = requests.post(
            "https://search.grata.com/api/v1.2/search-similar/",
            headers=GrataWrapper.HEADERS,
            json={
                "domain": domain,
                "grata_employees_estimates_range": api_filters[
                    "grata_employees_estimates_range"
                ],
                "headquarters": api_filters["headquarters"],
            },
        )
        data = response.json()
        print("find_similar:", data)
        data["companies"] = data.get("results", [])  # asking grata about this

        return data["companies"]

    def find_by_criteria(search: models.Search) -> dict:
        api_filters = GrataWrapper._get_api_filter(search)
        response = requests.post(
            "https://search.grata.com/api/v1.2/search/",
            headers=GrataWrapper.HEADERS,
            json=api_filters,
        )
        data = response.json()
        print("find_by_criteria: ", data)
        return data["companies"]

    def enrich(domain: str) -> dict:
        response = requests.post(
            "https://search.grata.com/api/v1.2/enrich/",
            headers=GrataWrapper.HEADERS,
            json={"domain": domain},
        )
        data = response.json()
        data["linkedin"] = data.get("social_linkedin")
        data["ownership"] = data.get("ownership_status")
        return data

    def _get_api_filter(search: models.Search) -> dict:
        STATES = {
            "AL": "Alabama",
            "AK": "Alaska",
            "AZ": "Arizona",
            "AR": "Arkansas",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DE": "Delaware",
            "FL": "Florida",
            "GA": "Georgia",
            "HI": "Hawaii",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "IA": "Iowa",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "ME": "Maine",
            "MD": "Maryland",
            "MA": "Massachusetts",
            "MI": "Michigan",
            "MN": "Minnesota",
            "MS": "Mississippi",
            "MO": "Missouri",
            "MT": "Montana",
            "NE": "Nebraska",
            "NV": "Nevada",
            "NH": "New Hampshire",
            "NJ": "New Jersey",
            "NM": "New Mexico",
            "NY": "New York",
            "NC": "North Carolina",
            "ND": "North Dakota",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PA": "Pennsylvania",
            "RI": "Rhode Island",
            "SC": "South Carolina",
            "SD": "South Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "UT": "Utah",
            "VT": "Vermont",
            "VA": "Virginia",
            "WA": "Washington",
            "WV": "West Virginia",
            "WI": "Wisconsin",
            "WY": "Wyoming",
        }

        COUNTRIES = {
            "USA": "United States",
            "CAN": "Canada",
            "MEX": "Mexico",
            "GBR": "United Kingdom",
        }

        def _hq_include() -> list:
            include = []
            cities = search.inclusion.get("city", [])
            states = search.inclusion.get("state", [])
            countries = search.inclusion.get("country", [])

            if len(cities) > 0:
                # front-end validates only one state when city selected
                state = STATES[states[0]]
                for city in cities:
                    include.append(
                        {"city": city, "state": state, "country": "United States"}
                    )
                return include

            if len(states) > 0:
                for state in states:
                    # NB: API wants full state name, but product wants state code
                    include.append({"state": STATES[state]})

            if len(countries) > 0:
                for country in countries:
                    include.append({"country": COUNTRIES[country]})
            return include

        def _hq_exclude() -> list:
            exclude = []
            for state in search.exclusion.get("state", []):
                exclude.append({"state": STATES[state]})
            return exclude

        return {
            "op": "any",
            "include": search.inclusion.get("keywords", []),
            "exclude": search.exclusion.get("keywords", []),
            "grata_employees_estimates_range": search.inclusion.get(
                "employees_range", []
            ),
            "ownership": search.inclusion.get("ownership", ""),
            "headquarters": {
                "include": _hq_include(),
                "exclude": _hq_exclude(),
            },
        }


class SourceScrubWrapper:
    def find_similar(domain: str, search: Search) -> dict:
        pass

    def find_by_criteria(search: Search) -> dict:
        pass

    def enrich(domain: str) -> dict:
        pass
