import sys
from bs4 import BeautifulSoup
from bs4.element import Tag 
import pandas as pd


def main(file_name):
    html_text = open_file(file_name)
    soup = BeautifulSoup(html_text, 'html.parser')
    page_title = extract_title(soup)
    page_content = select_main_content_tag(soup)
    # print(page_content)
    spell_to_dict(page_content)

def open_file(file_name) -> str:
    with open(file_name, 'r') as f:
        return f.read()

def extract_title(soup) -> Tag:
    page_title = soup.select_one('.page-title')
    return page_title

def select_main_content_tag(soup) -> Tag:
    if main_content := soup.select_one('#toc'):
        return main_content

    elif main_content := soup.select_one('#page-content'):
        return main_content

def spell_to_dict(page_content):
    spell_keys = ['source', 'school', 'spell_parameters', 'effect', 'higher_level', 'spell_list']
    spell_dict = {}
    peregragh = page_content.select('p')
    for i, p in enumerate(peregragh):
        if spell_keys[i] == 'spell_parameters':
            split_text = p.text.split('\n')
            for item in split_text:
                item = item.split(':')
                spell_dict.update({item[0] : item[1]})

            continue
        
        spell_dict.update({spell_keys[i] : p})


    # print(page_content.formatter_for_name)
    for key, val in spell_dict.items():
        print(f'{key} : {val}')
    # print(dir(page_content))
    # print(help(page_content.formatter_for_name))


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
    file_name = sys.argv[1]
    main(file_name)