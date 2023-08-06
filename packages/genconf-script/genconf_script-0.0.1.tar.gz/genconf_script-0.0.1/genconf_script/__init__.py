# __init__.py
__version__ = "0.0.1"

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

############
#### Constants
############

gen_conf_url_root1 = 'https://www.churchofjesuschrist.org/study/general-conference/'

ref_dict = {
    '1-ne':'1 Nephi',
    '2-ne':'2 Nephi',
    'jacob':'Jacob',
    'enos':'Enos',
    'jarom':'Jarom',
    'omni':'Omni',
    'w-of-m':'Words of Mormon',
    'mosiah':'Mosiah',
    'alma':'Alma',
    'hel':'Helaman',
    '3-ne':'3 Nephi',
    '4-ne':'4 Nephi',
    'morm':'Mormon',
    'ether':'Ether',
    'moro':'Moroni'
    }


############
#### Functions
############

def expand_hyphen_ref(x):
    first_digit = int(x.split('-')[0])
    last_digit = int(x.split('-')[1])
    all_verses = list(range(first_digit, last_digit + 1))
    return all_verses

def get_conf_urls(years):
    urls = []
    for year in years:
        url_april = gen_conf_url_root1 + str(year) + '/04' 
        url_oct = gen_conf_url_root1 + str(year) + '/10'
        urls.append(url_april)
        urls.append(url_oct)
    
    return urls

def get_book_verse(x):
    first_split = x.split('bofm/')[1]
    book = ref_dict[first_split.split('/')[0]]
    verse = re.findall('\.(.*?)\?', first_split)[0]
    chapter = re.findall('\/(.*?)\.', first_split)[0]
    if '-' in verse:
        verse_final = expand_hyphen_ref(verse)
        book_final = [book] * len(verse_final)
        chapter_final = [chapter] * len(verse_final)
        return book_final, chapter_final, verse_final
    else:
        return book, chapter, verse

def scrape_talk_footnotes(url, print_progress = False):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    talk_toc_items = soup.find_all("a", {"class": "item-U_5Ca"}, href = True)
    talk_link_prefix = 'https://www.churchofjesuschrist.org/'
    talk_links = [talk_link_prefix + x['href'] for x in talk_toc_items]
    del talk_links[0]
    
    ########### Get the footnote links from each talk
    url_indiv_talk = talk_links[0]
    page_indiv_talk = requests.get(url_indiv_talk)
    soup_indiv_talk = BeautifulSoup(page_indiv_talk.content, "html.parser")
    footnotes = soup_indiv_talk.find_all('a', {'class':'scripture-ref'}, href = True)
    footnotes_links = [talk_link_prefix + x['href'] for x in footnotes]


    talk_names = []
    book_list = []
    chapter_list = []
    verse_list = []
    
    for url_indiv_talk in talk_links:
        if print_progress == True:
            print('Scraping ' + url_indiv_talk)
        page_indiv_talk = requests.get(url_indiv_talk)
        soup_indiv_talk = BeautifulSoup(page_indiv_talk.content, "html.parser")
        footnotes = soup_indiv_talk.find_all('a', {'class':'scripture-ref'}, href = True)
        footnotes_links = [talk_link_prefix + x['href'] for x in footnotes]
        for note in footnotes_links:
            if 'bofm' in note:
                
                try:
                    ref = get_book_verse(note)
                    book_list.append(ref[0])
                    chapter_list.append(ref[1])
                    verse_list.append(ref[2])
                    talk_names.append(url_indiv_talk)
    
                except:
                    next
            else:
                continue

    refs_df = pd.DataFrame({'talk':talk_names,
                  'books':book_list,
                  'chapters':chapter_list,
                  'verses':verse_list}).explode(['books','chapters','verses']).reset_index(drop=True)

    return refs_df

def check_verse(book, chapter, verse, refs_df, multiple_verse = False):
    chapter_str = str(chapter)
    if multiple_verse == True:
        verses_str = [str(x) for x in verse]
        talks = refs_df.query('books == @book & chapters == @chapter_str & verses in @verses_str') 
    else:
        verses_str = str(verse)
        talks = refs_df.query('books == @book & chapters == @chapter_str & verses == @verses_str')
    return [x for x in talks['talk']]
