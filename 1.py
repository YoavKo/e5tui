import requests 
from bs4 import BeautifulSoup
import sys

''' classes dont have tb
    main page lineage have no table

    nither backruond
    items dont have mutch
    feat dont have table and bullet points
    Miscellaneous have no title

'''


class HtmlReader():

    def __init__(self, content_name):
        DIV_AND_FUNC = {'#toc' : [self.extract_main_title, self.extract_sub_title, self.extract_main_paragraph],
                        '#page-content' : [self.extract_main_title, self.extract_main_paragraph]
                        }
        # self.html = HtmlReader.open_file()   
        self.html = HtmlReader.read_from_site_to_text(content_name)
        self.res = []
        soup = BeautifulSoup(self.html, 'html.parser')
        self.main_content = soup.select_one('.main-content')
        # print(main_content)
        for key, val in DIV_AND_FUNC.items():
            self.sub_main_content_div = self.main_content.select_one(key)
            if self.sub_main_content_div:
                for funk in val:
                    funk()

        # self.toc = self.main_content.select_one('#toc')
        # if self.toc:
        #     self.extract_main_title()
        #     self.extract_sub_title()
        #     self.extract_main_paragraph()
       
        # else:
        #     self.toc = self.main_content.select_one('#page-content')
        #     self.extract_main_title()
        #     self.extract_main_paragraph()
    
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


    def extract_main_title(self) -> None:
        page_title = self.main_content.select_one('.page-title')
        self.res.append('# ' + page_title.text)
        self.res.append(HtmlReader.make_underline(self.res[-1], '='))
        self.res.append('')

    def extract_sub_title(self) -> None:
        title = self.sub_main_content_div.select_one('.title').text
        self.res.append('## ' + title)
        self.res.append(HtmlReader.make_underline(self.res[-1]))
        toc_list = self.sub_main_content_div.select_one('#toc-list')
        for subject in toc_list.findChildren('a'):
            self.res.append('* ' + subject.text)

        self.res.append('')

    def extract_main_paragraph(self) -> None:
        for el in self.sub_main_content_div.next_elements:
            if el.name == 'p':
                self.res.append(el.text)
                self.res.append('')

            elif el.name == 'h1':
                self.res.append('> ' + el.text)
                self.res.append('')
            
            elif el.name == 'td':
                print(f'{el.text=}')            
            
            else:
                pass
                # print(el.name)

if __name__ == '__main__':
    if len(sys.argv) == 2:content_name = sys.argv[1]
    HtmlReader(content_name)