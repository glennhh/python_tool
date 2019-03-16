#!/usr/bin/env python3

import requests
import bs4


def open_url(url):
    #proxy
    #proxies = {"http": "127.0.0.1:1080", "https": "127.0.0.1:1000"}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7'}
    
    # res = requests.get(url, headers=headers, proxies=proxies)
    res = requests.get(url, headers=headers)  #  auth=('user', 'pass')
    #print(res.encoding)
    #print(res.text)
    return res

def find_movies(res):
    #print(res)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    
    movies = []
    targets = soup.find_all("div", class_="hd")
    for each in targets:
        #print(each)
        try:
            movies.append(each.a.span.text)
        except:
            continue
    #print(movies)
    
    ranks = []
    targets = soup.find_all("span", class_="rating_num")
    for each in targets:
        try:
            ranks.append('rating: %s' % each.text)
        except:
            continue
    #print(ranks)
    
    messages = []
    targets = soup.find_all("div", class_="bd")
    for each in targets:
        try:
            messages.append(each.p.text.split('\n')[1]).strip() + each.p.text.split('\n')[2].strip()
        except:
            continue
    #print(messages)
    
    result = []
    length = len(movies)
    for i in range(length):
        result.append(movies[i] + ranks[i] + messages[i] + '\n')
    
    #print(result)    
    return result

def find_depth(res):
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    depth = soup.find('span', class_='next').previous_sibling.previous_sibling.text 
    
    return int(depth)

def main():
    #host = "https://www.google.com"
    host = "https://movie.douban.com/top250"
    res = open_url(host)
    depth = find_depth(res)
    
    result = []
    for i in range(depth):
        if i == 0:
            url = host
        else:
            url = host +'?start=' + str(25 * i) + '&filter=' 
        res = open_url(url)
        result.extend(find_movies(res))
        #print(result)
    
    with open("top250.txt", "w", encoding="utf-8") as f:
        for each in result:
            f.write(each)


if __name__ == "__main__":
    main()
    
    