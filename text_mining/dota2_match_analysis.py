""" Defense of the Ancients 2 Match Analysis
	This program calls Valve's Steam Web API in order to get match information
	for recent DotA 2 games. It calculates the pick count, win count, and win
	rate of each hero in the game, and outputs these results to an easily-parsed
	.csv file. The match data is stored in a pickled data file, so that our
	database is always expanding.

	Joey L. Maalouf
"""


#  module imports
from cPickle     import dump, load
from json        import loads
from operator    import itemgetter
from os.path     import exists
from pattern.web import URL
from pprint      import pprint
from sys         import argv
from time        import sleep


def get_data_from_url(url):
	""" Given some URL pointing to a JSON object,
		download its contents and convert them
		to a Python object.
	"""
	#  be nice and don't overload the servers; sleep between requests
	sleep(1)
	return loads(URL(url).download())


def main(argv):
	#  ----  GENERAL PURPOSE VARIABLES  ----------------------------------------
	#  I'm not putting my unique key on GitHub, get a key from
	#  http://steamcommunity.com/dev/apikey
	my_steam_api_key = ""
	steam_base_url = "https://api.steampowered.com/"
	data_file = "dota2_match_data_list.txt"
	output_file = "dota2_match_results.csv"

	#  ----  HERO LIST CREATION  -----------------------------------------------
	#  get the hero data, parse it, and reformat it
	#  into a dictionary of dictionaries, not a list
	#  of dictionaries because not every hero id is used
	heroes_url = steam_base_url+"IEconDOTA2_570/GetHeroes/v0001/?language=en_us&key="+my_steam_api_key
	hero_data = get_data_from_url(heroes_url)["result"]["heroes"]
	hero_dict = {}
	for hero in hero_data:
		hero_dict[hero["id"]] = {"name": hero["name"],
								 "localized_name": hero["localized_name"],
								 "pick_count": 0,
								 "win_count": 0,
								 "win_rate": 0.0}
	del hero_data

	#  ----  ID PULLING  -------------------------------------------------------
	#  get the most recent matches and pull their ids
	num_matches = 100
	matches_url = steam_base_url+"IDOTA2Match_570/GetMatchHistory/V001/?min_players=10&matches_requested="+str(num_matches)+"&key="+my_steam_api_key
	match_data = get_data_from_url(matches_url)["result"]["matches"]
	match_ids = [match["match_id"] for match in match_data]
	del match_data

	#  ----  UNPICKLING  -------------------------------------------------------
	#  read in our previously collected data,
	#  or make an empty database if it doesn't exist
	game_details = {}
	if not exists(data_file):
		file_object = open(data_file, "wb")
		dump(game_details, file_object)
		file_object.close()
	else:
		file_object = open(data_file, "rb")
		game_details = load(file_object)
		file_object.close()

	#  ----  DETAIL ACQUISITION  -----------------------------------------------
	#  using the above ids, get the detailed information for each game
	new_game_details = {}
	for match_id in match_ids:
		new_game_details[match_id] = get_data_from_url(steam_base_url+"IDOTA2Match_570/GetMatchDetails/V001/?match_id="+str(match_id)+"&key="+my_steam_api_key)["result"]
		if new_game_details[match_id]["first_blood_time"] == 0:
			del new_game_details[match_id]

	#  ----  DATABASE ADDITIONS  -----------------------------------------------
	#  for any new matches that aren't in the old database, add their details
	for match_id in new_game_details:
		if match_id not in game_details:
			game_details[match_id] = new_game_details[match_id]
	del new_game_details

	#  ----  PICKLING  ---------------------------------------------------------
	#  save our new dict of matches
	file_object = open(data_file, "wb")
	dump(game_details, file_object)
	file_object.close()

	#  ----  STAT CALCULATION  -------------------------------------------------
	#  for each game, calculate the pick count, win count, and win rate stats
	for game in game_details.values():
		radiant_win = game["radiant_win"]
		for player in game["players"]:
			player_hero = player["hero_id"]
			if player_hero in hero_dict:
				hero_dict[player_hero]["pick_count"] += 1
				if (player["player_slot"] < 5 and radiant_win) or (player["player_slot"] > 127 and not radiant_win):
					hero_dict[player_hero]["win_count"] += 1
				hero_dict[player_hero]["win_rate"] = float(hero_dict[player_hero]["win_count"])/hero_dict[player_hero]["pick_count"]

	#  ----  STAT SORTING  -----------------------------------------------------
	#  pull the informative stats and sort the list of tuples
	win_rates = [(h[1]["localized_name"], h[1]["win_count"], h[1]["pick_count"], h[1]["win_rate"]) for h in hero_dict.items()]
	win_rates = sorted(win_rates, key = itemgetter(3), reverse = True)

	#  ----  ANALYSIS OUTPUT  --------------------------------------------------
	#  save our output to a .csv file
	file_object = open(output_file, "wb")
	output_string = "Matches analyzed:"+str(len(game_details))+"\nHeroName,WinCount,PickCount,WinRate\n"
	for hero in win_rates:
		output_string += str(hero[0])+","+str(hero[1])+","+str(hero[2])+","+str(hero[3])+"\n"
	file_object.write(output_string)
	file_object.close()


#  ----  MAIN CHECK  -----------------------------------------------------------
#  check if __main__ so that we only do things if this file is run, but def main
#  so that other files which import this one can still call main if they want to
if __name__ == "__main__":
	main(argv)
