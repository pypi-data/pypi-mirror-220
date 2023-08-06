import requests

class ClarityAPIClient:
    def __init__(self, base_url="https://server-4pgh2arjbq-uc.a.run.app"):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint):
        # implementation for GET request
        response = self.session.get(self.base_url + endpoint)
        return response

    def post(self, endpoint, data):
        # implementation for POST request
        pass

    def put(self, endpoint, data):
        # implementation for PUT request
        pass

    def delete(self, endpoint):
        # implementation for DELETE request
        pass