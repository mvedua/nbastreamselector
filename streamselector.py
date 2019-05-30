"""
Stream selector
This script will load all the game threads off of /r/nbstreams, /r/ncaaBBstreams, /r/mlbstreams, /r/nhlstreams
Give you the choice to pick the game you want to watch,
And open it in a new browser tab automatically
"""

import StreamGetter
import praw


def main():
    message = ("|-------------------------------------------------|\n"
               "|                 streamselector                  |\n"
               "|                                                 |\n"
               "|  Watch live games for MLB, NBA, NCAA BB, & NHL  |\n"
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
        elif choice == 3:
            loaded = StreamGetter.get_nhl_streams(reddit)
            if loaded <= 0:
                StreamGetter.display_error("NHL", loaded)


if __name__ == '__main__':
    main()
