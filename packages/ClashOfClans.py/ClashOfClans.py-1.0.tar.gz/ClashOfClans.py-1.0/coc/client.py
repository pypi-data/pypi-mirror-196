from requests import Session
from json import loads

from .utils import objects
from .utils.headers import Headers
from .utils.exception import checkException

class Client:
	def __init__(self, token: str, proxies: dict = None):
		self.api = 'https://api.clashofclans.com/v1'
		self.session = Session()
		self.headers = Headers()
		self.proxies=proxies
		self.token = token


	def get_current_league_war(self, clan_tag: str):

		endpoint = f'/clans/%23{clan_tag}/currentwar/leaguegroup'
		response = self.session.get(f"{self.api}{endpoint}",  headers=self.headers.official_api_headers(self.token), proxies=self.proxies)
		return checkException(response.text) if response.status_code != 200 else objects.CuttentWarLeagueGroup(loads(response.text))


	def get_individual_war_league(self, war_tag: str):

		endpoint = f'/clanwarleagues/wars/%23{war_tag}'
		response = self.session.get(f"{self.api}{endpoint}",  headers=self.headers.official_api_headers(self.token), proxies=self.proxies)
		return checkException(response.text) if response.status_code != 200 else objects.IndividualWarLeagues(loads(response.text))



	def get_war_log(self, clan_tag: str, size: int = 10, after = None, before = None):

		endpoint = f'/v1/clans/%23{clan_tag}/warlog?limit={size}'
		if after:endpoint+=f'&after={after}'
		elif after:endpoint+=f'&before={before}'

		response = self.session.get(f"{self.api}{endpoint}",  headers=self.headers.official_api_headers(self.token), proxies=self.proxies)
		return checkException(response.text) if response.status_code != 200 else objects.WarLog(loads(response.text))