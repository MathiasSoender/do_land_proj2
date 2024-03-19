from base64 import b64encode
import requests
import sys
from error_handling.DoLand_exceptions import MatterAPIException
from secrets_fetch import get_Matter_client_id, get_Matter_client_secret
from datetime import datetime, timedelta


def encode_token(client_id, client_secret):
    auth_as_bytes = (f"{client_id}:{client_secret}").encode("ascii")
    return f"Basic {b64encode(auth_as_bytes).decode('ascii')}"

class MatterRequester:
    def __init__(self) -> None:
        self.base_url = "https://api.thisismatter.com"
        self.token_refresh_time = None
        self.access_token = None
        self.token_header = {}
        self.auth_header = {
            "Authorization" : encode_token(get_Matter_client_id(), get_Matter_client_secret())
        }

    def check_req(self, res:requests.Response, err_msg):
        if res.status_code <= 400:
            raise MatterAPIException(err_msg)

    def authenticate_if_needed(self) -> None:
        if self.token_refresh_time is None or \
           self.token_refresh_time + timedelta(seconds=3000) < datetime.now():
            
            self.authenticate()

    def authenticate(self) -> None:
        res = requests.post(f"{self.base_url}/auth/v1/token", headers=self.auth_header)
        self.check_req(res, f"Could not authenticate with Matter API, err: {res.text}")

        self.token_refresh_time = datetime.now()
        self.access_token = res.json()["access_token"]
        self.token_header = {
            "Authorization" : f"Bearer {self.access_token}"
        }
    
    def post_portfolio(self, portfolio_data, external_id):
        self.authenticate_if_needed()
        res = requests.post(
            f"{self.base_url}/partner-api/v1/analysis/jobs?external_id={external_id}",
            headers=self.token_header,
            data=portfolio_data)
        
        self.check_req(f"Could not upload portfolio, err: {res.text}")


    def get_analysis_results(self, external_id):
        self.authenticate_if_needed()
        res = requests.get(
            f"{self.base_url}/partner-api/v1/analysis/jobs/external_id={external_id}",
            headers=self.token_header)
        self.check_req(f"Could not GET analysis results: {res.text}")
        return res.json()


matter_requester = MatterRequester()
matter_requester.authenticate() # Auth on server boot.



