from urllib import request, error
from bs4 import BeautifulSoup
from json import loads, dumps
import os

CONFIG_FILE_PATH = './settings.json'


def get_config(config_file_path):
    with open(config_file_path) as f:
        config = loads(f.read())
    return config

def parse_list_elem(elem):
    return {
        'name': elem.next_element['name'],
        'description': elem.text.split(' - ')[1],
        'elementType': elem.name
    }

class TFResource(object):
    def __init__(self, id=None, docs_url=''):
        self.id = id
        self.docs_url = docs_url
        #self.doc_type = doc_type
        self.content = request.urlopen(docs_url).read()
        self.soup = soup = BeautifulSoup(self.content, features='html.parser')
        self.type = self.get_resource_type()
        self.properties = self.get_properties()

    def get_resource_type(self):
        resource_name = self.soup.find(id='inner').h1.contents
        return resource_name[-1].split(':')[1].strip()

    def get_properties(self):
        elements = self.soup \
            .find(id='inner') \
            .find(id='argument-reference') \
            .find_next_siblings()

        properties = [{
            'name': '',
            'description': str(elements[0]),
            'elementType': 'p'
        }]

        arguments = filter(lambda x: x != '\n', elements[1])
        ## TODO - properly deal with list depth, probably best to just do a straight port of what's here...
        for argument in arguments:
            prop = parse_list_elem(argument)






class Provider(object):
    def __init__(self, name='', url='', valid_doc_string='', doc_types={}, base_url=''):
        self.name = name
        self.url = url
        self.valid_doc_string = valid_doc_string
        self.doc_types = doc_types
        self.base_url = base_url

    def get_doc_links(self):
        content = request.urlopen(self.url)
        soup = BeautifulSoup(content, features='html.parser')
        symbol_exclude_list = ['/', '#', 'None', None]

        links = [x.get('href') for x in soup.find_all('a')]
        return list(filter(lambda x:
                                x not in symbol_exclude_list and
                                x[0] != '#' and
                                x.startswith(self.valid_doc_string),
                                links))

    def get_resource_pages(self):
        resource_links = self.get_doc_links()
        resource_link = resource_links[22]

        resource = TFResource(id=1, docs_url=f'{self.base_url}{resource_link}')
        print(resource.type)





def main():
    config = get_config(CONFIG_FILE_PATH)
    providers = [Provider(**x, base_url=config['base_url']) for x in config['providers']]
    providers[0].get_resource_pages()



if __name__ == '__main__':
    main()