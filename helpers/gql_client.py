import logging
import requests as re
from dataclasses import dataclass

from .config import CONFIG_GQL

logging.basicConfig(level=logging.INFO)


@dataclass
class GqlClient:
    env: str = 'staging'

    def __post_init__(self):
        self._initialize_config()

    def _initialize_config(self):
        self.config = CONFIG_GQL.get(self.env, CONFIG_GQL['staging'])
        self.api_key = self.config["api_key"]
        self.url = self.config["url"]
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

    def post(self, query, variables=None):
        payload = {'query': query, 'variables': variables}

        print(variables)
        try:
            response = re.post(self.url, json=payload, headers=self.headers)
            print(response.json())
            response.raise_for_status()
            data = response.json().get('data')
            if not data:
                logging.error(f"GraphQL Error: {response.json().get('errors')}")
            return data
        except re.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            return None
