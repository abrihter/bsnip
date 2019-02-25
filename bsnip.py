#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
BSNIP
small CLI snippet manager

Allow users to manage CLI snippets and execute code with just short commands,
calling snippets by IDs

versions:
    V1.0.0 [25.02.2019]
        - first wrking version
'''

__author__ = "Bojan"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Bojan"
__status__ = "Development"

import os
import json

class BSnip:
    '''bsnip main class'''

    def __init__(self):
        '''init'''
        self.db_path = os.path.join(os.path.expanduser('~'), '.bsnip')
        self.snips = self.__load_db()

    def __load_db(self):
        '''load db data set
        :return array: Returns DB data set
        '''
        if not os.path.exists(self.db_path):
            return []
        with open(self.db_path, 'r') as f:
            return json.loads(f.read())

    def __write_db(self):
        '''write db dataset
        :return bool: Returns True if all is OK
        '''
        with open(self.db_path, 'w') as f:
            f.write(json.dumps(self.snips))
        return True

    def add(self, snip):
        '''add snippet

        snip = {
            'desc': 'snippet description',
            'comm': 'command'
        }

        :param dict snip: Snippet data set
        :return bool: Return tru if all is OK
        '''
        if 'desc' in snip and 'comm' in snip:
            if snip['desc'].strip() != '' and snip['comm'].strip() != '':
                if self.snips:
                    snip['id'] = self.snips[-1]['id'] + 1
                else:
                    snip['id'] = 1
                self.snips.append(snip)
                return self.__write_db()
            print('Description or command can\'t be empty!')
            return False
        return False

    def delete(self, snippet_id):
        '''delete snippet
        :param int snippet_id: Snippet ID
        :return bool: Return True if all is OK
        '''
        for i in range(len(self.snips)):
            if self.snips[i]['id'] == snippet_id:
                del self.snips[i]
                return self.__write_db()
        return False

    def update(self, snip):
        '''update snippet

        snip = {
            'id': snippet ID
            'desc': 'snippet description',
            'comm': 'command'
        }

        :param dict snip: Snippet data set
        :return bool: Return tru if all is OK
        '''
        if 'desc' in snip and 'comm' in snip:
            if snip['desc'].strip() != '' and snip['comm'].strip() != '':
                for i in range(len(self.snips)):
                    if self.snips[i]['id'] == snip['id']:
                        self.snips[i]['desc'] = snip['desc']
                        self.snips[i]['comm'] = snip['comm']
                        return self.__write_db()
                return False
            print('Description or command can\'t be empty!')
            return False
        return False

    def get_by_id(self, snippet_id):
        '''get snippet by ID
        :param int snippet_id: Snippet ID
        :return dict: Return snippet data set or None on issue
        '''
        for i in range(len(self.snips)):
            if self.snips[i]['id'] == snippet_id:
                return self.snips[i]
        return None

    def search(self, search_term):
        '''search snippets
        :param str search_term: Search term
        :return list: Return list of all found snippets
        '''
        res = []
        for snip in self.snips:
            src = '{} {}'.format(snip['desc'], snip['comm'])
            if search_term.lower() in src.lower():
                res.append(snip)
        return res

    def run(self, snippet_id):
        '''execute snip by ID
        :param int snippet_id: Snippet ID
        :return bool: Returns True if executed or None on issue
        '''
        snip = self.get_by_id(snippet_id)
        if snip:
            try:
                os.system(snip['comm'])
            except Exception as error:
                print(error)
                return None
            return True
        return None

