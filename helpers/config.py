import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)


CONFIG_GQL = {
    'staging': {
        "url": "https://nce2nzequnem3jijcrgturt4oe.appsync-api.us-east-1.amazonaws.com/graphql",
        "api_key": "da2-2ystthtjuvd5nhwu47qecm3ekm",

    },
}
@dataclass
class Config:
    env: str = 'staging'

    def __post_init__(self):
        self.config = CONFIG_GQL.get(self.env, CONFIG_GQL['staging'])

