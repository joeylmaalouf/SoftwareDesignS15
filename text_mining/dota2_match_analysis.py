from json import loads
from operator import itemgetter
from pattern.web import URL
from pprint import pprint
from sys import argv
from time import sleep


def get_data_from_url(url):
	sleep(1)
	return loads(URL(url).download())


def main(argv):
	my_steam_api_key = "844A4778443A1AD62EB93C10766E3D23"

	heroes_url = "https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/?language=en_us&key="+my_steam_api_key
	hero_data = get_data_from_url(heroes_url)["result"]["heroes"]
	hero_dict = {}
	for hero in hero_data:
		hero_dict[hero["id"]] = {"name": hero["name"],
								 "localized_name": hero["localized_name"],
								 "pick_count": 0,
								 "win_count": 0,
								 "win_rate": 0.0,}
	del hero_data

	num_matches = 20
	matches_url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?min_players=10&matches_requested="+str(num_matches)+"&key="+my_steam_api_key
	match_data = get_data_from_url(matches_url)["result"]["matches"]
	match_ids = [match["match_id"] for match in match_data]
	del match_data

	game_details = [get_data_from_url("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id="+str(match_id)+"&key="+my_steam_api_key)["result"] for match_id in match_ids]
	game_details = [game for game in game_details if game["first_blood_time"] > 0.0]

	for game in game_details:
		radiant_win = game["radiant_win"]
		for player in game["players"]:
			player_hero = player["hero_id"]
			if player_hero in hero_dict:
				hero_dict[player_hero]["pick_count"] += 1
			if (player["player_slot"] < 5 and radiant_win) or (player["player_slot"] > 127 and not radiant_win):
				hero_dict[player_hero]["win_count"] += 1

	for hero_id in hero_dict:
		hero_dict[hero_id]["win_rate"] = float(hero_dict[hero_id]["win_count"])/hero_dict[hero_id]["pick_count"]

	print(sorted(hero_dict.items(), key = itemgetter("win_rate"), reverse = True)[:10])


if __name__ == "__main__":
	main(argv)
