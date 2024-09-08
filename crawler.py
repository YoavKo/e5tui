import requests 
import sys
from bs4 import BeautifulSoup
import time
import os 
from pathlib import Path

def main() -> None:
    if not Path('htmls').is_dir(): 
        os.mkdir('htmls')

    for i in range(1,15):
        html = read_from_site_to_text(f'system:list-all-pages/p/{i}')
        soup = BeautifulSoup(html, 'html.parser')
        main_content = soup.select_one('.main-content')
        url_list = main_content.select_one('.list-pages-box').find_next("ul")
        for link in url_list.find_all('a', href=True):
            url_ending = link['href']
            download_html(url_ending)

def download_html(url_ending) -> None:
    html_file = read_from_site_to_text(url_ending)
    save_text_to_file(html_file, f'htmls/{url_ending}.html')
    print(url_ending)
    time.sleep(2)

def read_from_site_to_text(url_ending : str) -> str:
    url=f'http://dnd5e.wikidot.com/{url_ending}'
    contents = requests.get(url)
    return contents.text

def save_text_to_file(text, file_name: str='11.html') -> None:
    with open(file_name, 'w') as f:
        f.write(text)

if __name__ == '__main__':
    main()