"""
Stream selector
This script will load all the game threads off of /r/nbstreams or /r/ncaaBBstreams or /r/mlbstreams,
Give you the choice to pick the game you want to watch,
And open it in a new browser tab automatically
"""

import StreamGetter
import StreamHelpers
import praw
import json


def main():

    with open('keys.json') as json_file:
        data = json.load(json_file)
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')
    agent = data.get('user_agent')

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=agent)
    while True:
        choice = StreamHelpers.get_sport()
        if choice == -1:
            break
        if choice == 0:
            loaded = StreamGetter.get_nba_streams(reddit)
            if loaded <= 0:
                StreamGetter.display_error("NBA", loaded)
        elif choice == 1:
            loaded = StreamGetter.get_ncaa_bb_streams(reddit)
            if loaded <= 0:
                StreamGetter.display_error("NCAA Basketball", loaded)
        elif choice == 2:
            loaded = StreamGetter.get_mlb_streams(reddit)
            if loaded <= 0:
                StreamGetter.display_error("MLB", loaded)


if __name__ == '__main__':
    main()
