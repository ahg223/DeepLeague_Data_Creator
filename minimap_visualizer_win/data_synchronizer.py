import json
from jungle_handler.parse_title import parse_video_title
def join_data_file(champion_json, jungle_json, event_json):
    joined_dict = {}

    game_data = event_json["gameInfo"]
    game_length = round(game_data["length"])
    game_participants = game_data["champ"]

    master_events = event_json["byTimeLines"]

    jungle_keyframes = jungle_json["keyframes"]

    joined_dict["keyframes"] = {}
    for current_time in range(game_length):
        current_time = str(current_time)
        print("creating keyframe {0}...".format(current_time), end="")
        joined_dict["keyframes"][current_time] = {}
        joined_dict["keyframes"][current_time]["champ_data"] = {}
        joined_dict["keyframes"][current_time]["camp_data"] = {}
        joined_dict["keyframes"][current_time]["events"] = []
        #print(jungle_keyframes[current_time])
        try:

            joined_dict["keyframes"][current_time]["camp_data"] = jungle_keyframes[current_time]
        except:
            print("No jungle data found...", end="")

        print("Processing champ data for keyframe {0}...".format(current_time), end="")
        for key, val in champion_json[current_time].items():
            if key == "timestamp" or key == "total": continue
            champ_dict = {"confidence": val["Confidence"],
                          "left": val["left"],
                          "top": val["top"],
                          "right": val["right"],
                          "bottom": val["bottom"]}
            joined_dict["keyframes"][current_time]["champ_data"][key] = champ_dict

        print("done")

    #process gamedata
    events = [  # event_type, key  to use for time, parameters
        ("tower", "time", ("towerType", "laneType", "killerId", "teamId")),
        ("champKill", "death_time", ("death_time", "respawn_time", "place", "victim")),
        ("eliteKill", "time", ("monsterSubType", "monsterType", "killerId"))
    ]


    for event, event_time_key, vals in events:
        print("Processing event data for event type {0}...".format(event), end="")
        sub_events = master_events[event]
        for x in sub_events:
            oc_time = round(x[event_time_key])
            struct = {}
            struct["type"] = event
            for param in vals:
                try:
                    struct[param] = x[param]
                except:
                    pass
            joined_dict["keyframes"][str(oc_time)]["events"].append(struct)
        print("done")

    joined_dict["gamelength"] = game_length
    joined_dict["participants"] = game_participants
    return joined_dict

if __name__ == '__main__':
    champion_json = json.load(open("game_data/deepleague_enhanced_X2F16_9-13_KR-3725708658_05.json"))
    event_json = json.load(open("game_data/3725708658_gameData.json"))
    jungle_json = json.load(open("game_data/3725708658_jungle.json"))
    processed = join_data_file(champion_json, jungle_json, event_json)
    with open("game_data/join_data_file_out.json", "w") as f:
        json.dump(processed, f)


