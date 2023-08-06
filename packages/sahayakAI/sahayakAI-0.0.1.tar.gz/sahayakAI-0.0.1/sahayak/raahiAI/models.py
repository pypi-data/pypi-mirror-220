from pydantic import BaseModel, Field
from typing import List
import requests
import logging
from config import RahiAIConfig

rahi_config = RahiAIConfig()

RAPID_API_KEY = rahi_config.rapid_api_key
RAPID_API_HOST = rahi_config.rapid_api_host
RAPID_API_ENDPOINT = rahi_config.rapid_api_endpoint


class TravelPlan(BaseModel):
    """Model for holding travel details such as source, destination and date of travel in India by train"""
    sourceCity: str = Field(
        description="Indian Railway Station code of the source station")
    destinationCity: str = Field(
        description="Indian Railway Station code of the destination station")
    dateOfJourney: str = Field(
        description="Date of the journey in DD-MM-YYYY format")


class TrainDetail(BaseModel):
    number: str = Field(description="Train number")
    name: str = Field(description="Name of the train")
    source_station: str = Field("Name and station code of the source station")
    arrival_at_source: str = Field("Arrival time at the source station")
    departure_from_source: str = Field(
        "Departure time from the source station")
    destination_station: str = Field(
        "Name and station code of the destination station")
    arrival_at_destination: str = Field(
        "Arrival time at the destination station")
    departure_from_destination: str = Field(
        "Departure time from the destination station")
    days: List = Field("Days on which this train runs")


class RapidAPI(BaseModel):
    """Rapid API Wrapper for calling Rapid API endpoints"""
    rapid_api_key: str = RAPID_API_KEY
    rapid_api_host: str = RAPID_API_HOST
    rapid_api_endpoint: str = RAPID_API_ENDPOINT

    def make_api_call(self, query_params: dict):
        rapid_api_headers = {
            "X-RapidAPI-Key": self.rapid_api_key,
            "X-RapidAPI-Host": self.rapid_api_host
        }
        response = requests.get(
            self.rapid_api_endpoint, headers=rapid_api_headers, params=query_params)
        logging.info("RAPID API Response: %s", response)
        return response.json()
