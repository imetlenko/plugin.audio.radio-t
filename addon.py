#-*- coding: utf-8 -*-
import os
import sys
import urllib
import urlparse
import xbmcaddon
import xbmcgui
import xbmc

import xbmcplugin
import requests
from bs4 import BeautifulSoup

def build_url(query):
    base_url = sys.argv[0]
    return base_url + '?' + urllib.urlencode(query)
    
def get_page(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')
    
def parse_page(page):
    songs = {}
    index = 1
    try:
        for item in page.find_all('item'):
            topics = ""

            sub_item = BeautifulSoup(item.find("description").text, "html.parser")
                
            for topic in sub_item.find_all('a'):
                topics = "{}{}\n".format(topics, topic.string.encode('utf-8'))

            if len(sub_item.img['src']) > 1:
                album_cover = sub_item.img['src']

            if len(sub_item.audio['src']) > 1:
                songs.update({index: {'album_cover': album_cover, 'title': item.title.text.encode('utf-8'), 'url': sub_item.audio["src"], 'topics': topics}})
                index += 1
    except Exception as e:
        xbmc.log("[plugin.radiot] {}".format(e), xbmc.LOGERROR)

    return songs
    
def build_song_list(songs):
    song_list = []

    for song in songs:
        li = xbmcgui.ListItem(label=songs[song]['title'], thumbnailImage=songs[song]['album_cover'])
        li.setInfo('music', {'Artist': songs[song]['title'], 'Title': songs[song]['topics'] })
        li.setProperty('fanart_image', songs[song]['album_cover'])
        li.setProperty('IsPlayable', 'true')
        url = build_url({'mode': 'stream', 'url': songs[song]['url'], 'title': songs[song]['title']})
        song_list.append((url, li, False))
    
    xbmcplugin.addDirectoryItems(addon_handle, song_list, len(song_list))
    xbmcplugin.setContent(addon_handle, 'songs')
    xbmcplugin.endOfDirectory(addon_handle)
    
def play_song(url):
    play_item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

def main():
    args = urlparse.parse_qs(sys.argv[2][1:])
    mode = args.get('mode', None)

    if mode is None:
        page = get_page(rss_feeds_url)
        content = parse_page(page)
        build_song_list(content)
    elif mode[0] == 'stream':
        play_song(args['url'][0])
    
if __name__ == '__main__':
    rss_feeds_url = 'http://feeds.rucast.net/radio-t'
    addon_handle = int(sys.argv[1])
    main()
