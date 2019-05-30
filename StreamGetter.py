"""
Functions that will open the desired sport's stream in your browser
"""
import webbrowser
import StreamHelpers


def get_sport():
    """
    Gets the sport the user wants to watch
    :return: Number of sport in list
    """
    sports = ["NBA Basketball", "NCAA Basketball", 'Major League Baseball']
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


def get_nba_streams(reddit):
    """
    Finds and loads the NBA stream you want to watch
    :param reddit: Reddit instance
    :return: 1 if loaded /u/buffstreams url, 0 if could not load /u/buffstreams url, 0 if no games
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
        
        print()
        if game_thread_choice == -1:
            print()
            return 100

        top_level_comments = StreamHelpers.get_comments(reddit, thread_ids, game_thread_choice)

        buffstreams_url = ''
        rippledotis_url = ''
        for comment in top_level_comments:
            if comment.author == 'buffstreams':
                buffstreams_url = StreamHelpers.get_stream_url(comment)
            elif comment.author == 'rippledotis':
                rippledotis_url = StreamHelpers.get_stream_url(comment)

        if buffstreams_url != '':
            webbrowser.open_new_tab(buffstreams_url)
        elif rippledotis_url != '':
            webbrowser.open_new_tab(rippledotis_url)
        else:
            urls_to_watch = StreamHelpers.get_urls_to_watch(top_level_comments)
            if len(urls_to_watch) == 0:
                return 0  # Could not load any streams from the game user selected
            else:
                webbrowser.open_new_tab(urls_to_watch[0])
        return 1  # Successfully loaded /u/rippledotis or /u/buffstreams url or other
    else:
        return -1  # Could not load any game threads


def get_ncaa_bb_streams(reddit):
    """
    Loads NCAA Basketball streams
    :param reddit: Reddit instance
    :return: -1 for no Game Threads, 0 for No streams in game thread, 1 for Game Thread with stream(s)
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
    if game_thread_choice == -1:
        print()
        return 100

    top_level_comments = StreamHelpers.get_comments(reddit, thread_ids, game_thread_choice)
    urls_to_watch = StreamHelpers.get_urls_to_watch(top_level_comments)

    print()
    if len(urls_to_watch) == 0:
        return 0  # Could not load any streams from the game user selected
    else:
        webbrowser.open_new_tab(urls_to_watch[0])
        return 1  # Loaded selected stream


def get_mlb_streams(reddit):
    """
    Loads NCAA Basketball streams
    :param reddit: Reddit instance
    :return: -1 for no Game Threads, 0 for No streams in game thread, 1 for Game Thread with stream(s)
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
    if game_thread_choice == -1:
        print()
        return 100

    top_level_comments = StreamHelpers.get_comments(reddit, thread_ids, game_thread_choice)

    print()
    sportsstatsme_url = ''
    for comment in top_level_comments:
        if comment.author == 'sportsstatsme':
            sportsstatsme_url = StreamHelpers.get_stream_url(comment)

    if sportsstatsme_url != '':
        webbrowser.open_new_tab(sportsstatsme_url)
    else:
        urls_to_watch = StreamHelpers.get_urls_to_watch(top_level_comments)
        if len(urls_to_watch) == 0:
            return 0  # Could not load any streams from the game user selected
        else:
            webbrowser.open_new_tab(urls_to_watch[0])
    
    return 1  # Loaded selected stream


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
