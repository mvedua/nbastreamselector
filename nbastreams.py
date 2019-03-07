# /r/nbastreams Stream selector
# This script will scrape all the game threads off of /r/nbstreams,
# Give you the choice to pick the game you want to watch,
# And open it in a new browser tab automatically

import webbrowser
import httplib2
from bs4 import BeautifulSoup, SoupStrainer

cities = ['atlanta', 'boston', 'brooklyn', 'charlotte', 'chicago', 'cleveland', 'dallas', 'denver', 'detroit', 'golden_state', 'houston',
          'indiana', 'los_angeles', 'la', 'mepmhis', 'minnesota', 'new_orleans', 'new_york', 'miami', 'milwaukee', 'oklahoma_city',
          'sacramento','san_antonio', 'toronto', 'utah', 'orlando', 'philadelphia', 'phoenix', 'portland', 'washington']


http = httplib2.Http()
url = 'https://www.reddit.com/r/nbastreams/'
status, response = http.request(url)

#
# Get all game threads
#
game_threads = []
for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
    if 'http' in link['href']:
        for place in cities:
            if place in link['href'] and link['href'] not in game_threads:
                game_threads.append(link['href'])
                
if len(game_threads) != 0:
    #
    # Choose which game to watch
    #
    for i in range(len(game_threads)):
        old = game_threads[i]
        new = old.split("thread_",1)[1]
        new = new.replace('_', ' ').replace('/', ' ')
        new = new.title()
        game = ''.join([i for i in new if not i.isdigit()])
        print(str(i) + ": " + game)

    game_thread_choice = int(input("Which game? "))


    #
    # Find and open /u/buffstreams url
    #
    url = game_threads[game_thread_choice]
    status, response = http.request(url)

    url_to_watch = ''
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
        if link.has_attr('href') and link['href'][0:4] == 'http' and 'bfst' in link['href']:
            url_to_watch = link['href']
            break

    webbrowser.open_new_tab(url_to_watch)
    
else:
    print("No NBA games on at the moment. Try again later.")
