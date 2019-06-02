"""
Stream selector
This script will load all the game threads off of /r/nbstreams, /r/ncaaBBstreams, /r/mlbstreams, /r/nhlstreams
Give you the choice to pick the game you want to watch,
And open it in a new browser tab automatically
"""

import StreamGetter


def main():
    message = ("|-------------------------------------------------|\n"
               "|                 streamselector                  |\n"
               "|                                                 |\n"
               "|  Watch live games for MLB, NBA, NCAA BB, & NHL  |\n"
               "|-------------------------------------------------|\n"
     )

    print(message)
    while True:
        choice = StreamGetter.get_sport()
        if choice == -1:
            break
        if choice == 0:
            StreamGetter.open_stream('NBA')
        elif choice == 1:
            StreamGetter.open_stream('NCAA Basketball')
        elif choice == 2:
            StreamGetter.open_stream('MLB')
        elif choice == 3:
            StreamGetter.open_stream('NHL')


if __name__ == '__main__':
    main()
