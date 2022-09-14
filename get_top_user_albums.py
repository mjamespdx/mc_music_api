from bs4 import BeautifulSoup
import requests
#from get_genres import get_genre
from time import sleep
import pandas as pd

def get_genre(url):
# function for getting album genres from their page
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'www.metacritic.com',
        'Referer': 'https://www.metacritic.com/browse/albums/score/userscore/all/filtered?view=detailed&sort=desc',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0'}
    
    page = requests.get('https://www.metacritic.com/' + url, headers = headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    #print(url)
    try:
        genre = soup.find('span', itemprop = 'genre').text
    except AttributeError:
        #print('Genre not found.')
        genre = 'Unspecified'
    
    #sleep to not overload site
    sleep(.75)
    return genre

def get_albums(num):
# function for retrieving albums from a page
# headers for valid request
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'www.metacritic.com',
        'Referer': 'https://www.metacritic.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0'}
    
    #num = 0
    url = 'https://www.metacritic.com/browse/albums/score/userscore/all/filtered?view=detailed&sort=desc&page={}'.format(num)
    
    albums = requests.get(url, headers = headers)
    
    soup = BeautifulSoup(albums.text, 'html.parser')
    
    # extract artist, album, and links to each album page
    artists = [artist.text.strip()[3:] for artist in soup.find_all('div', class_ = 'artist')]
    titles = [title.text for title in soup.find_all('a', class_ = 'title')]
    meta_scores = [score.text for score in soup.find_all('div', class_ = 'metascore_w large release positive')]
    user_scores = [score.text for score in soup.find_all('div', class_ = 'metascore_w user large release positive')]
    links = [link['href'] for link in soup.find_all('a') if link.parent in soup.find_all('td', class_ = 'clamp-image-wrap')]
    #genres = [get_genre(link) for link in links]
    album_df = pd.DataFrame(zip(artists, titles, meta_scores, user_scores, links), 
                            columns = ['artist', 'title', 'metascore', 'user_score', 'url'])
    
    #sleep to not overload site
    # not necessary because grabbing the link takes so long
    #sleep(1)
    
    # make artist/title strings
    #[str(x + ' - ' +  y) for x, y in zip(artists, titles)]
    return album_df

if __name__ == '__main__':
    print('Retrieving albums from metacritic...')
    albums = pd.concat([get_albums(i) for i in range(0, 10)], axis = 0)
    print('Retrieving genres...')
    albums['genre'] = [get_genre(link) for link in albums.url]
    print('Writing to csv...')
    albums.to_csv('albums.csv', index = False)
    print('Completed.')
