from claritygov.api.state import State
import requests
from claritygov.utils import us_state_to_abbrev
class House:
    def __init__(self, state: State) -> None:
        self.state = state
        self.state_abbrev = us_state_to_abbrev(state.state)
        self.api_client = state.api_client
    def get_house_members(self):
        resp = self.api_client.get(f'/{self.state_abbrev}/house/members')
        return resp
