"""
/r/nbastreams Stream selector
This script will scrape all the game threads off of /r/nbstreams,
Give you the choice to pick the game you want to watch,
And open it in a new browser tab automatically
"""

import webbrowser
import httplib2
from bs4 import BeautifulSoup, SoupStrainer


def get_nba_streams():
    """
    Finds and loads the NBA stream you want to watch
    :return:
    """
    print("Loading...")
    print()
    http = httplib2.Http()
    url = 'https://www.reddit.com/r/nbastreams/'
    status, response = http.request(url)

    # Get all game threads
    game_threads = []
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
        if 'game_thread' in link['href'] and 'http' in link['href'] and link['href'] not in game_threads:
            game_threads.append(link['href'])

    if len(game_threads) != 0:
        # Choose which game to watch
        print_game_threads(game_threads, "nba")

        game_thread_choice = get_game_thread_choice(len(game_threads))

        # Find and open /u/buffstreams url
        url = game_threads[game_thread_choice]
        status, response = http.request(url)

        url_to_watch = ''
        for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
            if link.has_attr('href') and link['href'][0:4] == 'http' and 'bfst' in link['href']:
                url_to_watch = link['href']
                break

        webbrowser.open_new_tab(url_to_watch)
        return True
    else:
        return False


def get_ncaa_bb_streams():
    """
    Loads NCAA Basketball streams
    :return: -1 for no Game Threads, 0 for No streams in game thread, 1 for Game Thread with stream(s)
    """
    print("Loading...")
    http = httplib2.Http()
    url = 'https://www.reddit.com/r/ncaaBBallStreams/'
    status, response = http.request(url)

    game_threads = []
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
        if 'http' in link['href'] and 'game_thread' in link['href'] and link['href'] not in game_threads:
            game_threads.append(link['href'])

    print()
    if len(game_threads) != 0:
        # Choose which game to watch
        print_game_threads(game_threads, "ncaabb")

    else:
        return -1

    game_thread_choice = get_game_thread_choice(len(game_threads))
    url = game_threads[game_thread_choice]
    status, response = http.request(url)

    urls_to_watch = []
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
        if link.has_attr('href') and link['href'][0:4] == 'http' and 'reddit' not in link['href']:
            urls_to_watch.append(link['href'])

    print()
    if len(urls_to_watch) == 0:
        return 0
    else:
        for i in range(len(urls_to_watch)):
            print("Link", str(i))
        while True:
            stream_choice = input("Link to watch: ")
            if stream_choice.isdigit():
                if int(stream_choice) in range(len(urls_to_watch)):
                    webbrowser.open_new_tab(urls_to_watch[int(stream_choice)])
                    return 1
                else:
                    print("Link " + stream_choice + " is not valid.")
            else:
                print("Please enter a digit in the list.")


def print_game_threads(threads, sport):
    """
    Prints out list of game threads
    :param threads: List of game threads
    :param sport: Sport user selected
    :return: None
    """
    if sport == "nba":
        for i in range(len(threads)):
            old = threads[i]
            new = old.split("thread_",1)[1]
            new = new.replace('_', ' ').replace('/', ' ')
            new = new.title()
            game = ''.join([i for i in new if not i.isdigit()])
            print(str(i) + ": " + game)
    elif sport == "ncaabb":
        for i in range(len(threads)):
            old = threads[i]
            new = old.split("thread_",1)[1]
            new = new.replace('_', ' ').replace('/', ' ')
            new = new.title()
            game = ''.join([i for i in new if not i.isdigit()])
            game = game.replace('Pm', '').replace('Est', '')
            print(str(i) + ": " + game)


def get_game_thread_choice(games):
    """
    Lets user select the one to watch
    :param games: Number of game threads
    :return:
    """
    while True:
        game_thread_choice = input("Game to watch: ")
        if game_thread_choice.isdigit():
            if int(game_thread_choice) in range(games):
                return int(game_thread_choice)
            else:
                print("Choice not valid. Please try again")
        else:
            print("Please enter a valid number in the list")


def get_sport():
    """
    Gets the sport the user wants to watch
    :return: Number of sport in list
    """
    sports = ["NBA Basketball", "NCAA Basketball"]
    for i in range(len(sports)):
        print(str(i) + ": " + sports[i])

    while True:
        choice = input("Choice ([Enter] to exit): ")
        if choice.isdigit():
            if int(choice) in range(len(sports)):
                return int(choice)
            else:
                print("Invalid choice. Please enter again.")
        elif choice == '':
            return -1
        else:
            print("Please enter a number in the list.")


def main():
    while True:
        choice = get_sport()
        if choice == -1:
            break
        if choice == 0:
            loaded = get_nba_streams()
            if not loaded:
                print("No NBA games on at the moment. Try again later.")
        elif choice == 1:
            loaded = get_ncaa_bb_streams()
            if loaded == -1:
                print("No NCAA games on at this moment. Try again later.")
            elif loaded == 0:
                print("The NCAA game you selected has no streams available.")

        print()


if __name__ == '__main__':
    main()