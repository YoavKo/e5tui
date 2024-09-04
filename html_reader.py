import requests 
from bs4 import BeautifulSoup
from bs4.element import Tag 
import sys
import pandas as pd


''' classes dont have tb
    main page lineage have no table

    nither backruond
    items dont have mutch
    feat dont have table and bullet points
    Miscellaneous have no title

'''


class HtmlReader():

    def __init__(self, content_name):
        # self.html = HtmlReader.open_file()   
        self.html = HtmlReader.read_from_site_to_text(content_name)
        self.res = []
        soup = BeautifulSoup(self.html, 'html.parser')
        self.main_content = soup.select_one('.main-content')
        self.sub_main_content_tag = self.select_main_content_tag()
        self.extract_main_title() 
        self.extract_sub_title()
        self.extract_main_paragraph()
        # print('\n'.join(self.res))


    @staticmethod
    def read_from_site_to_text(content_name:str) -> str:
        url=f'http://dnd5e.wikidot.com/{content_name}'
        contents = requests.get(url)
        return contents.text

    @staticmethod
    def save_text_to_file(text, file_name:str='11.html') -> None:
        with open(file_name, 'w') as f:
            f.write(text)

    @staticmethod
    def open_file(file_name:str='11.html') -> str:
        with open(file_name, 'r') as f:
            html = f.read()
            #print(html)
            return html

    @staticmethod
    def make_underline(text: str, line_type:str = '-') -> str:
        return line_type * len(text)

    def select_main_content_tag(self) -> Tag:
        if self.main_content.select_one('#toc'): string = '#toc'
        elif self.main_content.select_one('#page-content'): string = '#page-content'
        return self.main_content.select_one(string)

    def extract_main_title(self) -> None:
        page_title = self.main_content.select_one('.page-title')
        self.res.append('# ' + page_title.text)
        self.res.append(HtmlReader.make_underline(self.res[-1], '='))
        self.res.append('')

    def extract_sub_title(self) -> None:
        title = self.sub_main_content_tag.select_one('.title')
        if title: 
            title = title.text
            self.res.append('## ' + title)
            self.res.append(HtmlReader.make_underline(self.res[-1]))
            toc_list = self.sub_main_content_tag.select_one('#toc-list')
            for subject in toc_list.findChildren('a'):
                self.res.append('* ' + subject.text)

            self.res.append('')

    def extract_main_paragraph(self) -> None:
        for el in self.sub_main_content_tag.next_elements:
            if el.name == 'p':
                self.res.append(el.text)
                self.res.append('')

            elif el.name != None and 'h' in el.name:
                self.res.append('> ' + el.text)
                self.res.append('')
            
            elif el.name == 'tr':
                self.constract_table(el)
                # print(f'{el.text=}')            
            
            elif el.name == 'div':
                print(f'{el.text} \n\n')
                break

            elif el.name == None or el.name == 'br' or el.name == 'None':
                pass

            else:
                pass
                # print(el.name)

    def constract_table(self, el) -> str:#TODO: need a beater print
        table_text = []
        for td in el:
            if td.name == 'td' and td.text: 
                table_text.append(td.text)
        else:
            table_text.append('\n')

        self.res.append(''.join(table_text))

if __name__ == '__main__':
    # my_table = ['1', 'dd12', '123']
    # new_table = []
    # len_longest_string = len(max(my_table))
    # for num in my_table:
    #     len_empty_space = len_longest_string - len(num) 
    #     new_table.append(num + (' ' * len_empty_space))



    # print('|'.join(new_table))

    if len(sys.argv) == 2:content_name = sys.argv[1]
    else:content_name = ''
    HtmlReader(content_name)
