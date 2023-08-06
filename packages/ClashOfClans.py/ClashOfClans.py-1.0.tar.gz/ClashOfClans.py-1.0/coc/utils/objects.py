

class Media:
	def __init__(self, data: dict):
		self.json = data
		self.small = self.json.get('small', None)
		self.large = self.json.get('large', None)
		self.medium = self.json.get('medium', None)


#--------------clan
class CuttentWarLeagueGroup:
	def __init__(self, data: dict):
		self.json = data
		self.state = self.json.get('state', None)
		self.season = self.json.get('season', None)
		self.clans = list()
		for clan in self.json.get('clans', []):
			self.clans.append(self.Clan(clan))



	class Clan:
		def __init__(self, data: dict):
			self.json = data
			self.clanTag = self.json.get('tag', None)
			self.name = self.json.get('name', None)
			self.clanLevel = self.json.get('clanLevel', None)
			self.badgeUrls = Media(self.json.get('badgeUrls', {}))
			self.members = list()
			for member in self.json.get('members', []):
				self.members.append(self.Member(member))


		class Member:
			def __init__(self, data: dict):
				self.json = data
				self.tag = self.json.get('tag', None)
				self.name = self.json.get('name', None)
				self.townHallLevel = self.json.get('townHallLevel', None)





class IndividualWarLeagues:
	def __init__(self, data: dict):
		self.json = data


class WarLog:
	def __init__(self, data: dict):
		self.json = data


class Clans:
	def __init__(self, data: dict):
		self.json = data


class CuttentWar:
	def __init__(self, data: dict):
		self.json = data


class ClanInfo:
	def __init__(self, data: dict):
		self.json = data


class ClanMembers:
	def __init__(self, data: dict):
		self.json = data


class RaidSeason:
	def __init__(self, data: dict):
		self.json = data


#--------------players
class PlayerInfo:
	def __init__(self, data: dict):
		self.json = data






#--------------labels
class PlayerLabels:
	def __init__(self, data: dict):
		self.json = data

class ClanLabels:
	def __init__(self, data: dict):
		self.json = data




#--------------gold pass
class GoldPassSeason:
	def __init__(self, data: dict):
		self.json = data