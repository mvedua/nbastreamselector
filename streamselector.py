"""
Stream selector
This script will load all the game threads off of /r/nbstreams or /r/ncaaBBstreams,
Give you the choice to pick the game you want to watch,
And open it in a new browser tab automatically
"""

import webbrowser
import praw


def get_nba_streams(reddit):
    """
    Finds and loads the NBA stream you want to watch
    :param reddit: Reddit instance
    :return: 1 if loaded /u/buffstreams url, 0 if could not load /u/buffstreams url, 0 if no games
    """
    print("Loading...")
    print()

    # Load instance of nbastreams subreddit
    subreddit = reddit.subreddit('nbastreams')

    # Get list of game threads, thread ids, and titles from /r/nbastreams
    game_threads, thread_ids, titles = get_subreddit_posts(subreddit, 'nba')

    if len(game_threads) != 0:
        # Print titles for user to choose from
        print_titles(titles)

        game_thread_choice = get_game_thread_choice(len(game_threads))  # Game user selected
        submission_id = thread_ids[game_thread_choice]                  # Submission id of game user selected
        submission = reddit.submission(id=submission_id)                # Instance of the submission user selected
        submission.comment_sort = 'hot'                                 # How to sort comments
        top_level_comments = list(submission.comments)          # List of top level comment from game user selected

        buffstreams_url = ''
        rippledotis_url = ''
        for comment in top_level_comments:
            if comment.author == 'buffstreams':
                buffstreams_url = get_stream_url(comment)
            elif comment.author == 'rippledotis':
                rippledotis_url= get_stream_url(comment)

        if buffstreams_url != '':
            webbrowser.open_new_tab(buffstreams_url)
        elif rippledotis_url != '':
            webbrowser.open_new_tab(rippledotis_url)
        else:
            return 0    # Loaded game thread but not buffstreams or rippledotis url
        return 1  # Successfully loaded /u/rippledotis or /u/buffstreams url
    else:
        return -1       # Could not load any game threads


def get_ncaa_bb_streams(reddit):
    """
    Loads NCAA Basketball streams
    :param reddit: Reddit instance
    :return: -1 for no Game Threads, 0 for No streams in game thread, 1 for Game Thread with stream(s)
    """
    print("Loading...")

    # Load instance of ncaaBBallStreams subreddit
    subreddit = reddit.subreddit('ncaaBBallStreams')

    # Get list of game threads, thread ids, and titles from /r/ncaaBBallStreams
    game_threads, thread_ids, titles = get_subreddit_posts(subreddit, 'ncaabb')

    print()
    if len(game_threads) != 0:
        # Print titles of game threads for user to select from
        print_titles(titles)
    else:
        return -1   # Could not load any game threads

    game_thread_choice = get_game_thread_choice(len(game_threads))  # Game user selected
    submission_id = thread_ids[game_thread_choice]                  # Submission id of game user selected
    submission = reddit.submission(id=submission_id)                # Instance of the submission user selected
    submission.comment_sort = 'hot'                                 # How to sort comments
    top_level_comments = list(submission.comments)                  # List of top level comment from game user selected

    urls_to_watch = []
    '''
    Load all HD urls in the game thread
    '''
    for comment in top_level_comments:
        if 'HD' in comment.body:
            url = get_stream_url(comment)
            if 'http' in url:
                urls_to_watch.append(url)

    if len(urls_to_watch) == 0:
        for comment in top_level_comments:
            if 'SD' in comment.body:
                url = get_stream_url(comment)
                if 'http' in url:
                    urls_to_watch.append(url)
    print()
    if len(urls_to_watch) == 0:
        return 0    # Could not load any streams from the game user selected
    else:
        webbrowser.open_new_tab(urls_to_watch[0])
        return 1    # Loaded selected stream


def print_titles(thread_titles):
    """
    Prints out list of game threads
    :param thread_titles: List of game thread titles
    :return: None
    """
    for i in range(len(thread_titles)):
        print(str(i) + ": " + thread_titles[i])


def get_game_thread_choice(games):
    """
    Lets user select the one to watch
    :param games: Number of game threads
    :return: None
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


def get_subreddit_posts(subreddit, sport):
    """
    Gets list of game threads, thread ids, and thread titles
    :param subreddit: Instance of a subreddit
    :param sport: Sport user selected
    :return: list of game threads, thread ids, and thread titles
    """
    game_threads = []
    thread_ids = []
    titles = []

    if sport == 'nba':
        to_replace = 'Game Thread: '
    else:
        to_replace = 'Game thread: '

    for submission in subreddit.hot(limit=20):
        if 'game_thread' in submission.url and submission.url not in game_threads and 'bot' not in submission.title:
            game_threads.append(submission.url)
            thread_ids.append(submission.id)
            titles.append(submission.title.replace(to_replace, ''))
    return game_threads, thread_ids, titles


def get_stream_url(comment):
    """
    Gets a url in a comment's body
    :param comment: Instance of a comment
    :return: url of game stream
    """
    return comment.body[comment.body.index('(') + 1: comment.body.index(')')]


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
    reddit = praw.Reddit(client_id='UhpoGXrFBCU1Mg',
                         client_secret='Hm-aoEziRlyilVKDDLca5pWT-Kw',
                         user_agent='streamselector agent')
    while True:
        choice = get_sport()
        if choice == -1:
            break
        if choice == 0:
            loaded = get_nba_streams(reddit)
            if loaded == -1:
                print("No NBA games on at the moment. Try again later.")
            elif loaded == 0:
                print("Could not load stream url. Try again later.")
        elif choice == 1:
            loaded = get_ncaa_bb_streams(reddit)
            if loaded == -1:
                print("No NCAA games on at this moment. Try again later.")
            elif loaded == 0:
                print("The NCAA game you selected has no streams available.")

        print()


if __name__ == '__main__':
    main()
