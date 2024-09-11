import sys
from bs4 import BeautifulSoup
from bs4.element import Tag 
import pandas as pd
import os
import pickle
from pathlib import Path
import json

def main():
    pickle_dir = 'jar_of_spells'
    make_dir_if_not_exist(pickle_dir)        
    json_dir = 'jsons_spells'
    make_dir_if_not_exist(json_dir)


    files = os.walk('htmls')
    for root, dirs, file_names in files:
        for file_name in file_names:
            if file_name[:6] == 'spell:':
                try:
                    spell_dict = reconstract_one_spell(file_name)
                    # pickle.dump(spell_dict, save_text_to_file('', f"{pickle_dir}/{spell_dict['name']}.pickle"))
                    dump_data_into_json(spell_dict,  f'{json_dir}/{spell_dict["name"]}.json')
                except Exception as e:
                    save_text_to_file(file_name, 'errored_spells.text')

def dump_data_into_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)

def make_dir_if_not_exist(dir_name):
    if not Path(dir_name).is_dir(): 
        os.mkdir(dir_name)

def reconstract_one_spell(file_name):
    html_text = open_file(f'htmls/{file_name}')
    soup = BeautifulSoup(html_text, 'html.parser')
    page_title = extract_title(soup)
    page_content = select_main_content_tag(soup)
    spell_dict = spell_to_dict(page_title, page_content)
    return spell_dict

def open_file(file_name) -> str:
    with open(file_name, 'r') as f:
        return f.read()

def extract_title(soup) -> Tag:
    page_title = soup.select_one('.page-title')
    return page_title.text

def select_main_content_tag(soup) -> Tag:
    if main_content := soup.select_one('#toc'):
        return main_content

    elif main_content := soup.select_one('#page-content'):
        return main_content

def spell_to_dict(page_title, page_content) -> dict:
    effect =  'effect'
    spell_keys = ['source', 'school', 'spell_parameters', effect, 'spell_list']
    spell_dict = {'name' : page_title}
    peregragh = page_content.select('p')
    if 'Higher Levels' in peregragh[-2].text:
        spell_keys.insert(-1, 'higher_level')

    if 'HB' in peregragh[-1].text:
        spell_keys.insert(len(spell_keys), 'HB')

    if len(peregragh) > len(spell_keys):
        for _ in range(len(peregragh) - len(spell_keys)):
            spell_keys.insert(3, effect)

    print(spell_keys)

    for i, p in enumerate(peregragh):
        print(p)
        if spell_keys[i] == 'source':
            item = p.text.split(':')
            spell_dict.update({item[0].lower() : item[1]})

        elif spell_keys[i] == 'school':
            text_list = p.text.split(' ')
            school = text_list[-1]
            level = text_list[0][0]
            spell_dict.update({'school' : school, 
                               'level' : level})

        elif spell_keys[i] == 'spell_parameters':
            split_text = p.text.split('\n')
            for string in split_text:
                string_list = string.split(':')
                spell_dict.update({string_list[0].lower() : string_list[1]})

        elif spell_keys[i] == 'effect':
            if 'effect' in spell_dict.keys():
               spell_dict['effect'] += '\n' + p.text
               continue

            spell_dict.update({spell_keys[i] : p.text})

        elif spell_keys[i] == 'higher_level':
            spell_dict.update({spell_keys[i] : p.text[18:]})

        elif spell_keys[i] == 'spell_list':
            magic_users = [item.text for item in p.select('a')]
            spell_dict.update({spell_keys[i] : magic_users})
        
        elif spell_keys[i] == 'HB':
            spell_dict.update({spell_keys[i]: p.text})

    return spell_dict



def save_text_to_file(text, file_name: str='') -> None:
    with open(file_name, 'w') as f:
        f.write(text)
        return f

if __name__ == '__main__':
    main()
