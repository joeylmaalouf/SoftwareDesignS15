from cPickle     import dump, load
from json        import loads
from operator    import itemgetter
from os.path     import exists
from pattern.web import URL
from pprint      import pprint
from sys         import argv
from time        import sleep


def get_data_from_url(url):
	sleep(1)  #  be nice and don't overload the servers
	return loads(URL(url).download())


def main(argv):
	my_steam_api_key = ""  #  get from http://steamcommunity.com/dev/apikey, I'm not putting my unique key on GitHub

	#  get the hero data, parse it, and reformat it into a dictionary of dictionaries
	#  (not a list of dictionaries because not every hero id # is used)
	heroes_url = "https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/?language=en_us&key="+my_steam_api_key
	hero_data = get_data_from_url(heroes_url)["result"]["heroes"]
	hero_dict = {}
	for hero in hero_data:
		hero_dict[hero["id"]] = {"name": hero["name"],
								 "localized_name": hero["localized_name"],
								 "pick_count": 0,
								 "win_count": 0,
								 "win_rate": 0.0}
	del hero_data

	#  get the most recent matches and pull their ids
	num_matches = 100
	matches_url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?min_players=10&matches_requested="+str(num_matches)+"&key="+my_steam_api_key
	match_data = get_data_from_url(matches_url)["result"]["matches"]
	match_ids = [match["match_id"] for match in match_data]
	del match_data

	#  read in our previously collected data
	file_name = "match_data_list.txt"
	game_details = {}
	if not exists(file_name):
		file_object = open(file_name, "wb")
		dump(game_details, file_object)
		file_object.close()
	else:
		file_object = open(file_name, "rb")
		game_details = load(file_object)
		file_object.close()

	#  using the above ids, get the detailed information for each game
	new_game_details = {}
	for match_id in match_ids:
		new_game_details[match_id] = get_data_from_url("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id="+str(match_id)+"&key="+my_steam_api_key)["result"]
		if new_game_details[match_id]["first_blood_time"] == 0:
			del new_game_details[match_id]

	#  for any newly found matches that aren't in the old database, add them
	for match_id in new_game_details:
		if match_id not in game_details:
			game_details[match_id] = new_game_details[match_id]
	del new_game_details

	#  save our new dict of matches
	file_object = open(file_name, "wb")
	dump(game_details, file_object)
	file_object.close()

	#  for each game, calculate the pick count, win count, and win rate statistics
	for game in game_details.values():
		radiant_win = game["radiant_win"]
		for player in game["players"]:
			player_hero = player["hero_id"]
			if player_hero in hero_dict:
				hero_dict[player_hero]["pick_count"] += 1
				if (player["player_slot"] < 5 and radiant_win) or (player["player_slot"] > 127 and not radiant_win):
					hero_dict[player_hero]["win_count"] += 1
				hero_dict[player_hero]["win_rate"] = float(hero_dict[player_hero]["win_count"])/hero_dict[player_hero]["pick_count"]

	#  pull the informative stats, sort the list of tuples, and display it
	win_rates = [(h[1]["localized_name"], h[1]["win_count"], h[1]["pick_count"], h[1]["win_rate"]) for h in hero_dict.items()]
	win_rates = sorted(win_rates, key = itemgetter(3), reverse = True)
	print("Matches analyzed: "+str(len(game_details)))
	print("Hero, Win Count, Pick Count, Win Rate")
	pprint(win_rates)


if __name__ == "__main__":
	main(argv)
