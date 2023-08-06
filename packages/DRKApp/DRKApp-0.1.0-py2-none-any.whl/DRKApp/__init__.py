import requests


class DRKApp:
    """
    The DRKApp class is used to interact with the DRKApp API. It requires a token to be passed in the header for authentication. 
    It can be used to fetch data from different APIs based on the source (mattr, cache, or list), API type (test, staging, or production), 
    and API endpoint (partner_list, vulnerabilities, dropdowns, or case_list).
    """

    def __init__(self, token=None, api_type=None, source=None, api=None):
        """
        Initializes a new instance of the DRKApp class with the given token, api_type, source, and api.

        Args:
            token (str): The authentication token to use when interacting with the DRKApp API.
            api_type (str): The type of the API to use (test, staging, or production).
            source (str): The source of the API to use (mattr, cache, or list).
            api (str): The API endpoint to interact with (partner_list, vulnerabilities, dropdowns, or case_list).
        """
        self.token = token
        self.api_type = api_type
        self.source = source
        self.api = api

        # dictionary to store all the API URLs
        self.api_base_list = {
            "mattr": {
                "test": "https://api-mattr.aftrdrk.io/",
                "staging": "https://api-mattr.aftrdrk.io/",
                "production": "https://api-mattr.aftrdrk.io/"
            },
            "cache": {
                "test": "https://api-cache.aftrdrk.io/",
                "staging": "https://api-cache.aftrdrk.io/",
                "production": "https://api-cache.aftrdrk.io/"
            },
            "list": {
                "test": "https://api-list.aftrdrk.io/",
                "staging": "https://api-list.aftrdrk.io/",
                "production": "https://api-list.aftrdrk.io/"
            }
        }

    def all_api_list(self):
        """
        Returns a dictionary of all the available APIs and their endpoints.
        """
        return {
            "partner_list": "users/partner-list/",
            "vulnerabilities": "case/vulnerabilities/",
            "dropdowns": "case/dropdown/",
            "case_list": "case/all-case/",
        }

    def check_required_params(self):
        """
        Checks whether all the required parameters are provided.
        """
        if not self.token:
            raise ValueError("Token is required")

        if not self.api_type:
            raise ValueError(
                "API type is required (test, staging, production)")

        if not self.source:
            raise ValueError("Source is required")

        if not self.api:
            raise ValueError("API is required")

    def get_api_url(self):
        """
        Returns the API URL based on the provided API type and source.
        """
        self.check_required_params()

        source_url_dict = self.api_base_list.get(self.source.lower(), None)

        if source_url_dict is None:
            raise ValueError(f"Invalid Source '{self.source}'")

        api_url = source_url_dict.get(self.api_type.lower(), None)

        if api_url is None:
            raise ValueError(f"Invalid API Type '{self.api_type}'")

        return api_url

    def get_data(self, api=None):
        """
        Fetches data from the API based on the provided API type and source.
        """
        self.check_required_params()

        api_url = self.get_api_url()

        api = self.all_api_list().get(api, None)

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "origin": api_url
        }

        response = requests.get(f"{api_url}{api}", headers=headers)

        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            return {"data": data, "status": response.status_code}
        else:
            raise Exception(
                f"Failed to fetch data from API with status code {response.status_code} and message {response.text}")

    def get_single_id_(self, api=None, id=None):

        self.check_required_params()

        if id is None:
            raise ValueError("ID is required")

        api_url = self.get_api_url()

        api = self.all_api_list().get(api, None)

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "origin": api_url
        }

        response = requests.get(f"{api_url}{api}/{id}/", headers=headers)

        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            return {"data": data, "status": response.status_code}
        else:
            raise Exception(
                f"Failed to fetch data from API with status code {response.status_code} and message {response.text}")
