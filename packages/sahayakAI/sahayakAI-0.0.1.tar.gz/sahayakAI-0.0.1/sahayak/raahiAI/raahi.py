import logging

from simpleaichat import AIChat

from config import CommonConfig
from sahayak.raahiAI.models import TravelPlan, TrainDetail, RapidAPI
from sahayak.raahiAI.prompts import RAHI_SYSTEM_PROMPT

# The name will resolve to raahi
# This will load raahi logger
logger = logging.getLogger(__name__)

common_config = CommonConfig()

OPEN_AI_MODEL = common_config.chat_model
OPEN_AI_API_KEY = common_config.openai_api_key


async def _get_train_info(travelInfo: TravelPlan):
    """Return the information about trains running between two stations for the given date."""
    query_params = {
        "fromStationCode": travelInfo.sourceCity,
        "toStationCode": travelInfo.destinationCity,
        "dateOfJourney": travelInfo.dateOfJourney
    }
    rapid_api = RapidAPI()
    logger.info("Making RapidAPI Call with params:", query_params)
    return rapid_api.make_api_call(query_params)


def get_agent():
    """Return simpleai chat agent"""
    logger.info("Trying to create SimpleAIChat agent")
    return AIChat(system=RAHI_SYSTEM_PROMPT, model=OPEN_AI_MODEL, save_messages=False, api_key=OPEN_AI_API_KEY)


def get_user_friendly_message(rapid_api_response):
    """Return user-friendly message from the json response received from RapidAPI"""
    logger.info(
        "Trying to create user friendly message from RapidAPI response")
    trains = list()
    for train_details in rapid_api_response["data"]:
        train = TrainDetail(
            number=train_details["train_number"],
            name=train_details["train_name"],
            source_station=train_details["from_station_name"] +
            " (" + train_details["from"] + ")",
            arrival_at_source=train_details["from_sta"],
            departure_from_source=train_details["from_std"],
            destination_station=train_details["to_station_name"] +
            " (" + train_details["to"] + ")",
            arrival_at_destination=train_details["to_sta"],
            departure_from_destination=train_details["to_std"],
            days=train_details["run_days"]
        )
        trains.append(train)
    logger.info("Parsing of user friendly message is successful")
    return trains


async def get_train_info(query: str):
    """Return train information based on natural language query from the user"""
    agent = get_agent()
    logger.info("SimpleAiChat agent created successfully.")
    # Get the output in the form of a schema expected by the RapidAPI Endpoint
    output = agent(query, output_schema=TravelPlan)
    logger.info("Agent Output:", output)
    travel_details = TravelPlan.parse_obj(output)
    logger.info("OpenAI Response (Travel Details): %s", travel_details)
    rapid_api_response = await _get_train_info(travel_details)
    return get_user_friendly_message(rapid_api_response)
