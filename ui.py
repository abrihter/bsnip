#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
BSNIP SIMPLE UI

Simple UI for BSnip class

versions:
    V1.0.0 [25.02.2019]
        - first wrking version
'''

__author__ = "Bojan"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Bojan"
__status__ = "Development"

import sys

class UI:
    '''user interface class'''

    COMMANDS = {
        'add': 'Add new snippet',
        'delete': 'Delete snippet <bsnip delete 23>',
        'update': 'Update snippet <bsnip update 23>',
        'list': 'List snippets',
        'search': 'Search snippets <bsnip search test>',
        'run': 'Run snippet <bsnip run 23>',
        '--version': 'App version',
        '--help': 'This help'
    }

    def __init__(self, bs):
        '''init'''
        self.params = sys.argv
        self.bsnip = bs

    def __is_int(self, number):
        '''check if it is integer
        :param number: To check
        :return int: Return integer value if converted or None on issue
        '''
        try:
            return int(number)
        except:
            return None

    def __is_params_exist(self, command):
        '''check if params exist in command'''
        if 'params' in command:
            if not command['params']:
                print('Please enter param(s)!')
                return None
            return True
        print('Please enter param(s)!')
        return None

    def __parse_command(self):
        '''parse command
        :return dict: Return parsed command as dict or None on issue
        '''
        if len(self.params) < 2:
            print('Please enter command!')
            print('For list of commands try < bsnip --help >')
            return None
        if self.params[1].lower() not in self.COMMANDS.keys():
            print('Please enter valid command!')
            return None
        command = {'comm': self.params[1].lower()}
        if len(self.params) > 2:
            command['params'] = self.params[2:]
        return command

    def __command_add(self):
        '''add command'''
        comm = input('Command:')
        desc = input('Description:')
        snip = {
            'desc': desc,
            'comm': comm,
        }
        return self.bsnip.add(snip)

    def __command_delete(self, command):
        '''delete command'''
        if 'params' in command:
            if not command['params']:
                print('Please enter ID for snippet to delete!')
                return None
            snippet_id = self.__is_int(command['params'][0])
            if snippet_id:
                return self.bsnip.delete(snippet_id)
            print('ID need to be integer!')
            return None
        print('Please enter ID for snippet to run!')
        return None

    def __command_update(self, command):
        '''update command'''
        if self.__is_params_exist(command):
            snippet_id = self.__is_int(command['params'][0])
            if snippet_id:
                snip = self.bsnip.get_by_id(snippet_id)
                if snip:
                    print('Old Command:', snip['comm'])
                    comm = input('Command:')
                    print('Old Description:', snip['desc'])
                    desc = input('Description:')
                    snip = {
                        'id': snip['id'],
                        'desc': desc,
                        'comm': comm,
                    }
                    return self.bsnip.update(snip)
                print('No snippet ID: {}!'.format(command['params'][0]))
                return None
            print('ID need to be integer!')
            return None
        return None

    def __command_run(self, command):
        '''run command'''
        if self.__is_params_exist(command):
            snippet_id = self.__is_int(command['params'][0])
            if snippet_id:
                return self.bsnip.run(snippet_id)
            print('Command ID: {} not found!'.format(command['comm'][0]))
            return None
        return None

    def __command_search(self, command):
        '''search command'''
        if self.__is_params_exist(command):
            search_term = ' '.join(command['params'])
            snips = self.bsnip.search(search_term)
            if snips:
                self.__command_list(snips)
                return True
            print('Can\'t find snippets for search: [{}]!'.format(search_term))
            return None
        return None

    def __command_list(self, snips):
        '''liat command'''
        if not snips:
            print('No data to display!')
        for snip in snips:
            print('#{:5} {}'.format(snip['id'], snip['desc']))
            print('>', snip['comm'])
            print('----------')
        return True

    def run_command(self):
        '''run command
        :return bool: Return True if all is OK
        '''
        command = self.__parse_command()
        if not command:
            return None
        if command['comm'] == 'add':
            return self.__command_add()
        if command['comm'] == 'delete':
            return self.__command_delete(command)
        if command['comm'] == 'update':
            return self.__command_update(command)
        if command['comm'] == 'list':
            return self.__command_list(self.bsnip.snips)
        if command['comm'] == 'search':
            return self.__command_search(command)
        if command['comm'] == 'run':
            return self.__command_run(command)
        if command['comm'] == '--help':
            for comm in self.COMMANDS:
                print('{:10} {}'.format(comm, self.COMMANDS[comm]))
        elif command['comm'] == '--version':
            print(__version__)
        return None


