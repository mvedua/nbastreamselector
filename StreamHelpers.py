"""
Functions that help StreamGetter open the streams
"""


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

def print_titles(thread_titles):
    """
    Prints out list of game threads
    :param thread_titles: List of game thread titles
    :return: None
    """
    for i in range(len(thread_titles)):
        print(str(i) + ": " + thread_titles[i])


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

    if sport in ['mlb', 'nba']:
        to_replace = 'Game Thread: '
    else:
        to_replace = 'Game thread: '

    for submission in subreddit.hot(limit=20):
        if 'game_thread' in submission.url and submission.url not in game_threads and 'bot' not in submission.title:
            game_threads.append(submission.url)
            thread_ids.append(submission.id)
            titles.append(submission.title.replace(to_replace, ''))
    return game_threads, thread_ids, titles


def get_game_thread_choice(games):
    """
    Lets user select the one to watch
    :param games: Number of game threads
    :return: -1 if user exits, None otherwise
    """
    print('e: Go Back')
    while True:
        game_thread_choice = input("Game to watch: ")
        if game_thread_choice.isdigit():
            if int(game_thread_choice) in range(games):
                return int(game_thread_choice)
            else:
                print("Choice not valid. Please try again")
        elif game_thread_choice.lower() == 'e':
            return -1
        else:
            print("Please enter a valid number in the list")



def get_comments(reddit, thread_ids, game_thread_choice):
    """
    Gets the comments from a thread
    :param reddit: Reddit instance
    :param thread_ids: IDs of threads from a subreddit
    :param game_thread_choice: Game user wanted to watch
    :return: Top level comments from a game thread
    """
    submission_id = thread_ids[game_thread_choice]  # Submission id of game user selected
    submission = reddit.submission(id=submission_id)  # Instance of the submission user selected
    submission.comment_sort = 'hot'  # How to sort comments
    top_level_comments = list(submission.comments)  # List of top level comment from game user selected

    return top_level_comments


def get_urls_to_watch(top_level_comments):
    """
    Gets urls of a stream from comments
    :param top_level_comments: Comments from a game thread
    :return: list of stream urls
    """
    urls_to_watch = []
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
    return urls_to_watch


def get_stream_url(comment):
    """
    Gets a url in a comment's body
    :param comment: Instance of a comment
    :return: url of game stream
    """
    return comment.body[comment.body.index('(') + 1: comment.body.index(')')]
