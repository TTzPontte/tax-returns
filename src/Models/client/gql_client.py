import logging
from dataclasses import dataclass

import requests

from config import CONFIG

logging.basicConfig(level=logging.INFO)


@dataclass
class GqlClient:
    env: str = 'staging'

    def __post_init__(self):
        self._initialize_config()

    def _initialize_config(self):
        self.config = CONFIG.get(self.env, CONFIG['staging'])
        self.api_key = self.config["api_key"]
        self.url = self.config["url"]
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

    def post(self, query, variables=None):
        payload = {'query': query, 'variables': variables}
        try:
            response = requests.post(self.url, json=payload, headers=self.headers)
            response.raise_for_status()
            data = response.json().get('data')
            if not data:
                logging.error(f"GraphQL Error: {response.json().get('errors')}")
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            return None
