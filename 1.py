import requests 
from bs4 import BeautifulSoup

'''
url = 'http://dnd5e.wikidot.com/background:inheritor'
contents = requests.get(url)
#print(contents.text)
with open('11.html', 'w') as f:
    f.write(contents.text)
'''

with open('11.html', 'r') as f:
    html = f.read()
    #print(html)

def make_underline(text: str, line_type:str = '-') -> str:
    return line_type * len(text)

res = []

soup = BeautifulSoup(html, 'html.parser')
main_content = soup.select_one('.main-content')

page_title = main_content.select_one('.page-title')
res.append('# ' + page_title.text)
res.append(make_underline(res[-1], '='))
res.append('')

toc = main_content.select_one('#toc')
toc_title = toc.select_one('.title').text
res.append('## ' + toc_title)
res.append(make_underline(res[-1]))
toc_list = toc.select_one('#toc-list')
for subject in toc_list.findChildren('a'):
    res.append('* ' + subject.text)
res.append('')

for el in toc.next_elements:
    if el.name == 'p':
        res.append(el.text)
        res.append('')

    elif el.name == 'h1':
        res.append('# ' + el.text)
        res.append('')
    
    else:
        print(el.name)


print('\n'.join(res))