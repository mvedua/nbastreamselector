"""
Stream selector
This script will load all the game threads off of /r/nbstreams or /r/ncaaBBstreams or /r/mlbstreams,
Give you the choice to pick the game you want to watch,
And open it in a new browser tab automatically
"""

import StreamGetter
import praw


def main():
    message = ("|-------------------------------------------------|\n"
               "|                 streamselector                  |\n"
               "|                                                 |\n"
               "|  Watch live game streams for MLB, NBA, NCAA BB  |\n"
               "|-------------------------------------------------|\n"
     )

    reddit = praw.Reddit(client_id='UhpoGXrFBCU1Mg',
                         client_secret='Hm-aoEziRlyilVKDDLca5pWT-Kw',
                         user_agent='streamselector agent')
    print(message)
    while True:
        choice = StreamGetter.get_sport()
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
