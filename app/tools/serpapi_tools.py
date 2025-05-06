import os
from typing import Dict, List, Optional, Any
from smolagents import Tool
from serpapi import GoogleSearch


class GoogleFlightsTool(Tool):
    name = "google_flights_search"
    description = """
    Search for flights using Google Flights.
    
    Use this tool to find flight options between airports on specific dates.
    You can search for one-way, round-trip, or multi-city flights,
    filter by airline, number of stops, price, and more.
    
    Results will show the best flight options with prices, durations, and details.
    """

    inputs = {
        "departure_id": {
            "description": """
            Airport code or location kgmid for departure.
            
            An airport code is an uppercase 3-letter code (e.g., CDG for Paris Charles de Gaulle, LAX for Los Angeles).
            A location kgmid starts with /m/ (e.g., /m/0vzm for Austin, TX).
            
            You can specify multiple airports by separating with commas (e.g., CDG,ORY,/m/04jpl).
            """,
            "type": "string",
        },
        "arrival_id": {
            "description": """
            Airport code or location kgmid for arrival.
            
            An airport code is an uppercase 3-letter code (e.g., CDG for Paris Charles de Gaulle, LAX for Los Angeles).
            A location kgmid starts with /m/ (e.g., /m/0vzm for Austin, TX).
            
            You can specify multiple airports by separating with commas (e.g., CDG,ORY,/m/04jpl).
            """,
            "type": "string",
        },
        "outbound_date": {
            "description": "Departure date in YYYY-MM-DD format (e.g., 2025-06-15)",
            "type": "string",
        },
        "return_date": {
            "description": "Return date in YYYY-MM-DD format for round trips (e.g., 2025-06-25). Required if type=1 (Round trip).",
            "type": "string",
            "nullable": True,
        },
        "type": {
            "description": """
            Flight type:
            1 = Round trip (default)
            2 = One way
            3 = Multi-city (requires multi_city_json parameter)
            
            For Round Trip (1), you'll need to make another request with departure_token to get returning flight information.
            """,
            "type": "integer",
            "nullable": True,
        },
        "travel_class": {
            "description": """
            Class of travel:
            1 = Economy (default)
            2 = Premium economy
            3 = Business
            4 = First
            """,
            "type": "integer",
            "nullable": True,
        },
        "adults": {
            "description": "Number of adult passengers (default: 1)",
            "type": "integer",
            "nullable": True,
        },
        "children": {
            "description": "Number of children passengers (default: 0)",
            "type": "integer",
            "nullable": True,
        },
        "infants_in_seat": {
            "description": "Number of infants in seats (default: 0)",
            "type": "integer",
            "nullable": True,
        },
        "infants_on_lap": {
            "description": "Number of infants on lap (default: 0)",
            "type": "integer",
            "nullable": True,
        },
        "currency": {
            "description": "Currency for prices (e.g., USD, EUR, JPY) (default: USD). See Google Travel Currencies page for supported codes.",
            "type": "string",
            "nullable": True,
        },
        "stops": {
            "description": """
            Maximum number of stops:
            0 = Any number of stops (default)
            1 = Nonstop only
            2 = 1 stop or fewer
            3 = 2 stops or fewer
            """,
            "type": "integer",
            "nullable": True,
        },
        "max_price": {
            "description": "Maximum price in the specified currency. Default is unlimited.",
            "type": "integer",
            "nullable": True,
        },
        "sort_by": {
            "description": """
            Sort order:
            1 = Top flights (default)
            2 = Price
            3 = Departure time
            4 = Arrival time
            5 = Duration
            6 = Emissions
            """,
            "type": "integer",
            "nullable": True,
        },
        # "airlines": {
        #     "description": """
        #     List of airline codes to include (e.g., ['UA', 'AA']).
        #     Each airline code should be a 2-character IATA code. You can also use alliance codes:
        #     STAR_ALLIANCE = Star Alliance
        #     SKYTEAM = SkyTeam
        #     ONEWORLD = Oneworld
        #     Cannot be used together with exclude_airlines.
        #     """,
        #     "type": "array",
        #     "nullable": True,
        # },
        # "exclude_airlines": {
        #     "description": """
        #     List of airline codes to exclude (e.g., ['UA', 'AA']).
        #     Each airline code should be a 2-character IATA code. You can also use alliance codes:
        #     STAR_ALLIANCE = Star Alliance
        #     SKYTEAM = SkyTeam
        #     ONEWORLD = Oneworld
        #     Cannot be used together with airlines.
        #     """,
        #     "type": "array",
        #     "nullable": True,
        # },
        "deep_search": {
            "description": "When True, produces more precise results identical to browser but increases response time (default: False)",
            "type": "boolean",
            "nullable": True,
        },
        "booking_token": {
            "description": "Token to retrieve booking options for a selected flight. Cannot be used with departure_token.",
            "type": "string",
            "nullable": True,
        },
        "departure_token": {
            "description": "Token to retrieve returning flight information for round trips or the next leg for multi-city trips. Cannot be used with booking_token.",
            "type": "string",
            "nullable": True,
        },
        "locale": {
            "description": "Locale for language and region formatting (e.g., 'en-US', 'fr-FR')",
            "type": "string",
            "nullable": True,
        },
        "hl": {
            "description": "UI language in ISO 639-1 format (e.g., 'en' for English, 'fr' for French). See Google languages page for supported codes.",
            "type": "string",
            "nullable": True,
        },
        "gl": {
            "description": "Country of the search in ISO 3166-1 Alpha-2 format (e.g., 'us', 'fr'). See Google countries page for supported codes.",
            "type": "string",
            "nullable": True,
        },
        "bags": {
            "description": "Number of carry-on bags (default: 0)",
            "type": "integer",
            "nullable": True,
        },
        "show_hidden": {
            "description": "Set to True to include hidden flight results (default: False)",
            "type": "boolean",
            "nullable": True,
        },
        "multi_city_json": {
            "description": """
            JSON string containing multiple flight information objects for multi-city flights. Required when type=3.
            
            Format: [{"departure_id":"CDG","arrival_id":"NRT","date":"2025-05-13"},...]
            
            Each object should contain:
            - departure_id: Departure airport code or location kgmid
            - arrival_id: Arrival airport code or location kgmid
            - date: Flight date in YYYY-MM-DD format
            - times (optional): Time range for the flight
            """,
            "type": "string",
            "nullable": True,
        },
        "outbound_times": {
            "description": """
            Outbound times range as comma-separated numbers. Each number represents the beginning of an hour:
            
            4,18: 4:00 AM - 7:00 PM departure
            0,18: 12:00 AM - 7:00 PM departure
            19,23: 7:00 PM - 12:00 AM departure
            4,18,3,19: 4:00 AM - 7:00 PM departure, 3:00 AM - 8:00 PM arrival
            """,
            "type": "string",
            "nullable": True,
        },
        "return_times": {
            "description": """
            Return times range as comma-separated numbers. Each number represents the beginning of an hour:
            
            4,18: 4:00 AM - 7:00 PM departure
            0,18: 12:00 AM - 7:00 PM departure
            19,23: 7:00 PM - 12:00 AM departure
            4,18,3,19: 4:00 AM - 7:00 PM departure, 3:00 AM - 8:00 PM arrival
            
            Only used when type=1 (Round trip)
            """,
            "type": "string",
            "nullable": True,
        },
        "emissions": {
            "description": """
            Flight emission level:
            1 = Less emissions only
            """,
            "type": "integer",
            "nullable": True,
        },
        "layover_duration": {
            "description": """
            Layover duration in minutes as two comma-separated numbers.
            
            Example: 90,330 for 1 hr 30 min - 5 hr 30 min layover time.
            """,
            "type": "string",
            "nullable": True,
        },
        "exclude_conns": {
            "description": """
            Connecting airport codes to exclude.
            
            Airport codes are uppercase 3-letter codes (e.g., CDG, LAX).
            Multiple airports can be separated by commas (e.g., CDG,LAX).
            """,
            "type": "string",
            "nullable": True,
        },
        "max_duration": {
            "description": "Maximum flight duration in minutes (e.g., 1500 for 25 hours)",
            "type": "integer",
            "nullable": True,
        },
        "no_cache": {
            "description": "When True, forces SerpApi to fetch fresh results instead of using cached results (default: False)",
            "type": "boolean",
            "nullable": True,
        },
        "async_search": {
            "description": "When True, submits search asynchronously; you'll need to use Searches Archive API to retrieve results (default: False)",
            "type": "boolean",
            "nullable": True,
        },
    }
    output_type = "object"

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            print("Warning: SERPAPI_API_KEY not found in environment variables.")

    def forward(
        self,
        departure_id: str,
        arrival_id: str,
        outbound_date: str,
        return_date: Optional[str] = None,
        type: Optional[int] = None,
        travel_class: Optional[int] = None,
        adults: Optional[int] = 1,
        children: Optional[int] = 0,
        infants_in_seat: Optional[int] = 0,
        infants_on_lap: Optional[int] = 0,
        currency: Optional[str] = "USD",
        stops: Optional[int] = None,
        max_price: Optional[int] = None,
        sort_by: Optional[int] = None,
        # airlines: Optional[List[str]] = None,
        # exclude_airlines: Optional[List[str]] = None,
        bags: Optional[int] = None,
        deep_search: Optional[bool] = False,
        booking_token: Optional[str] = None,
        departure_token: Optional[str] = None,
        locale: Optional[str] = "en-US",
        hl: Optional[str] = "en",
        gl: Optional[str] = "us",
        show_hidden: Optional[bool] = False,
        multi_city_json: Optional[str] = None,
        outbound_times: Optional[str] = None,
        return_times: Optional[str] = None,
        emissions: Optional[int] = None,
        layover_duration: Optional[str] = None,
        exclude_conns: Optional[str] = None,
        max_duration: Optional[int] = None,
        no_cache: Optional[bool] = None,
        async_search: Optional[bool] = None,
    ) -> Dict[str, Any]:
        if booking_token:
            return self._get_booking_options_data(booking_token, hl, gl, currency)

        params = {
            "engine": "google_flights",
            "api_key": self.api_key,
            "hl": hl,
            "gl": gl,
            "currency": currency,
            "locale": locale,
            "deep_search": deep_search,
        }

        if departure_id:
            params["departure_id"] = departure_id

        if arrival_id:
            params["arrival_id"] = arrival_id

        if outbound_date:
            params["outbound_date"] = outbound_date

        if return_date:
            params["return_date"] = return_date

        if type is not None:
            params["type"] = type

        if travel_class is not None:
            params["travel_class"] = travel_class

        if adults is not None:
            params["adults"] = adults

        if children is not None:
            params["children"] = children

        if infants_in_seat is not None:
            params["infants_in_seat"] = infants_in_seat

        if infants_on_lap is not None:
            params["infants_on_lap"] = infants_on_lap

        if stops is not None:
            params["stops"] = stops

        if max_price is not None:
            params["max_price"] = max_price

        if sort_by is not None:
            params["sort_by"] = sort_by

        # if airlines:
        #     if isinstance(airlines, list):
        #         airlines_str = ",".join(airlines)
        #         params["include_airlines"] = airlines_str

        # if exclude_airlines:
        #     if isinstance(exclude_airlines, list):
        #         exclude_airlines_str = ",".join(exclude_airlines)
        #         params["exclude_airlines"] = exclude_airlines_str

        if bags is not None:
            params["bags"] = bags

        if show_hidden is not None:
            params["show_hidden"] = show_hidden

        if departure_token is not None:
            params["departure_token"] = departure_token

        # Add new parameters
        if multi_city_json is not None:
            params["multi_city_json"] = multi_city_json

        if outbound_times is not None:
            params["outbound_times"] = outbound_times

        if return_times is not None:
            params["return_times"] = return_times

        if emissions is not None:
            params["emissions"] = emissions

        if layover_duration is not None:
            params["layover_duration"] = layover_duration

        if exclude_conns is not None:
            params["exclude_conns"] = exclude_conns

        if max_duration is not None:
            params["max_duration"] = max_duration

        if no_cache is not None:
            params["no_cache"] = no_cache

        if async_search is not None:
            params["async"] = async_search

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            return results
        except Exception as e:
            return {"error": str(e)}

    def _get_booking_options_data(
        self, booking_token: str, hl: str = "en", gl: str = "us", currency: str = "USD"
    ) -> Dict[str, Any]:
        params = {
            "engine": "google_flights",
            "api_key": self.api_key,
            "booking_token": booking_token,
            "hl": hl,
            "gl": gl,
            "currency": currency,
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            return results
        except Exception as e:
            return {"error": str(e)}


google_flights_tool = GoogleFlightsTool()
