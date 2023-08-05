import requests

from dcentrapi.Base import Base

class Web3Index(Base):

    def get_pairs(self, network_name: str, token_address: str):
        url = self.web3index_url + "pairs" + f"/{network_name}/{token_address}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_factories(self):
        url = self.web3index_url + "factories"
        response = requests.get(url, headers=self.headers)
        return response.json()
