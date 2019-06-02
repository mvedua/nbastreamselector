"""
Functions that will open the desired sport's stream in your browser
"""
import webbrowser
import StreamHelpers
import praw


def get_sport():
    """
    Gets the sport the user wants to watch
    :return: Number of sport in list
    """
    sports = ["NBA Basketball", "NCAA Basketball", 'Major League Baseball', "NHL Hockey"]
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


def display_error(sport, error):
    """
    Displays message if stream could not load
    :param sport: Sport user selected
    :param error: Error Code(-1 = No games; 0 = No streams for game)
    :return: None
    """
    if error == -1:
        print("No {} games on at this moment. Try again later.\n".format(sport))
    elif error == 0:
        print("The {} game you selected has no streams available.\n".format(sport))


def open_stream(sport):
    """
    Calls appropriate stream getter based on sport choice
    :param sport: User's sport choice
    :return: None
    """
    reddit = praw.Reddit(client_id='UhpoGXrFBCU1Mg',
                         client_secret='Hm-aoEziRlyilVKDDLca5pWT-Kw',
                         user_agent='streamselector agent')

    if sport == 'NBA':
        loaded = get_nba_streams(reddit)
    elif sport == 'NCAA Basketball':
        loaded = get_ncaa_bb_streams(reddit)
    elif sport == 'MLB':
        loaded = get_mlb_streams(reddit)
    elif sport == 'NHL':
        loaded = get_nhl_streams(reddit)

    if type(loaded) is str:
        webbrowser.open_new_tab(loaded)
    else:
        if loaded <= 0:
            display_error(sport, loaded)
        else:
            return


def get_nba_streams(reddit):
    """
    Finds and loads the NBA stream you want to watch
    :param reddit: Reddit instance
    :return: string of stream url if loaded, 0 if could not load /u/buffstreams url, 0 if no games
    """
    print("Loading...\n")

    # Load instance of nbastreams subreddit
    subreddit = reddit.subreddit('nbastreams')

    # Get list of game threads, thread ids, and titles from /r/nbastreams
    game_threads, thread_ids, titles = StreamHelpers.get_subreddit_posts(subreddit, 'nba')

    if len(game_threads) != 0:
        # Print titles for user to choose from
        StreamHelpers.print_titles(titles)

        game_thread_choice = StreamHelpers.get_game_thread_choice(len(game_threads))  # Game user selected

        # User exited
        print()
        if game_thread_choice == -1:
            print()
            return 100

        top_level_comments = StreamHelpers.get_comments(reddit, thread_ids, game_thread_choice)

        buffstreams_url = StreamHelpers.get_priority_url('buffstreams', top_level_comments)

        if buffstreams_url != '':
            return buffstreams_url
        else:
            rippledotis_url = StreamHelpers.get_priority_url('rippledotis', top_level_comments)
            if rippledotis_url != '':
                return rippledotis_url
            else:
                urls_to_watch = StreamHelpers.get_urls_to_watch(top_level_comments)
                if len(urls_to_watch) == 0:
                    return 0  # Could not load any streams from the game user selected
                else:
                    return urls_to_watch[0]
    else:
        return -1  # Could not load any game threads


def get_ncaa_bb_streams(reddit):
    """
    Loads NCAA Basketball streams
    :param reddit: Reddit instance
    :return: -1 for no Game Threads, 0 for No streams in game thread, string of stream url if loaded
    """
    print("Loading...\n")

    # Load instance of ncaaBBallStreams subreddit
    subreddit = reddit.subreddit('ncaaBBallStreams')

    # Get list of game threads, thread ids, and titles from /r/ncaaBBallStreams
    game_threads, thread_ids, titles = StreamHelpers.get_subreddit_posts(subreddit, 'ncaabb')

    if len(game_threads) != 0:
        # Print titles of game threads for user to select from
        StreamHelpers.print_titles(titles)
    else:
        return -1  # Could not load any game threads

    game_thread_choice = StreamHelpers.get_game_thread_choice(len(game_threads))  # Game user selected

    # User exited
    if game_thread_choice == -1:
        print()
        return 100

    top_level_comments = StreamHelpers.get_comments(reddit, thread_ids, game_thread_choice)
    urls_to_watch = StreamHelpers.get_urls_to_watch(top_level_comments)

    print()
    if len(urls_to_watch) == 0:
        return 0  # Could not load any streams from the game user selected
    else:
        return urls_to_watch[0]


def get_mlb_streams(reddit):
    """
    Loads MLB streams
    :param reddit: Reddit instance
    :return: -1 for no Game Threads, 0 for No streams in game thread, string of stream url if loaded
    """
    print("Loading...\n")

    # Load instance of mlbstreams subreddit
    subreddit = reddit.subreddit('mlbstreams')

    # Get list of game threads, thread ids, and titles from /r/ncaaBBallStreams
    game_threads, thread_ids, titles = StreamHelpers.get_subreddit_posts(subreddit, 'mlb')

    if len(game_threads) != 0:
        # Print titles of game threads for user to select from
        StreamHelpers.print_titles(titles)
    else:
        return -1  # Could not load any game threads

    game_thread_choice = StreamHelpers.get_game_thread_choice(len(game_threads))  # Game user selected

    # User exited
    if game_thread_choice == -1:
        print()
        return 100

    top_level_comments = StreamHelpers.get_comments(reddit, thread_ids, game_thread_choice)

    print()
    sportsstatsme_url = StreamHelpers.get_priority_url('sportsstatme', top_level_comments)

    if sportsstatsme_url != '':
        return sportsstatsme_url
    else:
        urls_to_watch = StreamHelpers.get_urls_to_watch(top_level_comments)
        if len(urls_to_watch) == 0:
            return 0  # Could not load any streams from the game user selected
        else:
            return urls_to_watch[0]


def get_nhl_streams(reddit):
    """
    Loads NHL streams
    :param reddit: Reddit instance
    :return: -1 for no Game Threads, 0 for No streams in game thread, string of stream url if loaded
    """
    print("Loading...\n")

    # Load instance of mlbstreams subreddit
    subreddit = reddit.subreddit('nhlstreams')

    # Get list of game threads, thread ids, and titles from /r/ncaaBBallStreams
    game_threads, thread_ids, titles = StreamHelpers.get_subreddit_posts(subreddit, 'nhl')

    if len(game_threads) != 0:
        # Print titles of game threads for user to select from
        StreamHelpers.print_titles(titles)
    else:
        return -1  # Could not load any game threads

    game_thread_choice = StreamHelpers.get_game_thread_choice(len(game_threads))  # Game user selected

    # User exited
    if game_thread_choice == -1:
        print()
        return 100

    top_level_comments = StreamHelpers.get_comments(reddit, thread_ids, game_thread_choice)

    print()
    streamingmpi_url = StreamHelpers.get_priority_url('streamingmpi', top_level_comments)

    if streamingmpi_url != '':
        return streamingmpi_url
    else:
        urls_to_watch = StreamHelpers.get_urls_to_watch(top_level_comments)
        if len(urls_to_watch) == 0:
            return 0  # Could not load any streams from the game user selected
        else:
            return urls_to_watch[0]
