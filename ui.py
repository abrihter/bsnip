#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
BSNIP SIMPLE UI

Simple UI for BSnip class

versions:
    V1.0.0 [25.02.2019]
        - first wrking version
    V1.1.0 [06.04.2019]
        - added option to save snippets on jsonstorage.net
'''

__author__ = "Bojan"
__license__ = "GPL"
__version__ = "1.1.0"
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
        'save-cloud': 'Save snippets in cloud (using jsonstorage.net)',
        'load-cloud': 'Load snippets from cloud (using jsonstorage.net)',
        'get-cloud-id': 'Get local cloud ID',
        'set-cloud-id': 'Set local cloud ID',
        'list-cloud-for-id': 'List snippets online for cloud ID',
        '--version': 'App version',
        '--help': 'This help'
    }

    def __init__(self, bs):
        '''init'''
        self.params = sys.argv
        self.bsnip = bs

    def _is_int(self, number):
        '''check if it is integer
        :param number: To check
        :return int: Return integer value if converted or None on issue
        '''
        try:
            return int(number)
        except:
            return None

    def _is_params_exist(self, command):
        '''check if params exist in command'''
        if 'params' in command:
            if not command['params']:
                print('Please enter param(s)!')
                return None
            return True
        print('Please enter param(s)!')
        return None

    def _parse_command(self):
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

    def _command_add(self):
        '''add command'''
        comm = input('Command:')
        desc = input('Description:')
        snip = {
            'desc': desc,
            'comm': comm,
        }
        return self.bsnip.add(snip)

    def _command_delete(self, command):
        '''delete command'''
        if 'params' in command:
            if not command['params']:
                print('Please enter ID for snippet to delete!')
                return None
            snippet_id = self._is_int(command['params'][0])
            if snippet_id:
                return self.bsnip.delete(snippet_id)
            print('ID need to be integer!')
            return None
        print('Please enter ID for snippet to run!')
        return None

    def _command_update(self, command):
        '''update command'''
        if self._is_params_exist(command):
            snippet_id = self._is_int(command['params'][0])
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

    def _command_run(self, command):
        '''run command'''
        if self._is_params_exist(command):
            snippet_id = self._is_int(command['params'][0])
            if snippet_id:
                return self.bsnip.run(snippet_id)
            print('Command ID: {} not found!'.format(command['comm'][0]))
            return None
        return None

    def _command_search(self, command):
        '''search command'''
        if self._is_params_exist(command):
            search_term = ' '.join(command['params'])
            snips = self.bsnip.search(search_term)
            if snips:
                self._command_list(snips)
                return True
            print('Can\'t find snippets for search: [{}]!'.format(search_term))
            return None
        return None

    def _command_list(self, snips):
        '''list command'''
        if not snips:
            print('No data to display!')
            return None
        print('Snippets list:')
        if self.bsnip.snips['snips-online-id']:
            print('CLOUD ID:', self.bsnip.snips['snips-online-id'])
        else:
            print('CLOUD ID: not set')
        for snip in snips:
            print('#{:5} {}'.format(snip['id'], snip['desc']))
            print('>', snip['comm'])
            print('----------')
        return True

    def _command_save_cloud(self):
        '''save cloud command'''
        if self.bsnip.write_db_cloud():
            print('Snippets saved to cloud!')

    def _command_load_cloud(self):
        '''load cloud command'''
        if not self.bsnip.get_snips_online_id():
            print('Cloud ID need to be set!')
            return None
        if self.bsnip.load_db_cloud():
            print('Snippets loaded from cloud!')
        else:
            print('Issues loading snippets from clud!')
        return None

    def _command_get_cloud_id(self):
        '''get cloud id command'''
        cloud_id = self.bsnip.get_snips_online_id()
        if cloud_id:
            print('Cloud ID:', cloud_id)
        else:
            print('Cloud ID not set!')

    def _command_set_cloud_id(self):
        '''set cloud id command'''
        cloud_id = input('Enter cloud ID:')
        if not cloud_id.strip():
            if input('Confirm empty cloud ID [Y/n]:') != 'Y':
                print('Cloud ID not changed!')
                return None
        self.bsnip.udate_snips_online_id(cloud_id.strip())
        self._command_get_cloud_id()
        return None

    def _command_list_cloud_snips_for_id(self):
        '''list command from cloud for selected ID
        :return bool: Return True if OK or none on issue
        '''
        cloud_id = input('Enter cloud ID to search for:')
        snips = self.bsnip.get_snips_online_for_id(cloud_id)
        if not snips:
            print('Not valid snips ID!')
            return None
        print('Snippets list:')
        if snips['snips-online-id']:
            print('Cloud ID:', snips['snips-online-id'])
        else:
            print('Cloud ID: not set')
        for snip in snips['snips']:
            print('#{:5} {}'.format(snip['id'], snip['desc']))
            print('>', snip['comm'])
            print('----------')
        return True

    def run_command(self):
        '''run command
        :return bool: Return True if all is OK
        '''
        command = self._parse_command()
        if not command:
            return None
        if command['comm'] == 'add':
            return self._command_add()
        if command['comm'] == 'delete':
            return self._command_delete(command)
        if command['comm'] == 'update':
            return self._command_update(command)
        if command['comm'] == 'list':
            return self._command_list(self.bsnip.snips['snips'])
        if command['comm'] == 'search':
            return self._command_search(command)
        if command['comm'] == 'run':
            return self._command_run(command)
        if command['comm'] == 'save-cloud':
            return self._command_save_cloud()
        if command['comm'] == 'load-cloud':
            return self._command_load_cloud()
        if command['comm'] == 'get-cloud-id':
            return self._command_get_cloud_id()
        if command['comm'] == 'set-cloud-id':
            return self._command_set_cloud_id()
        if command['comm'] == 'list-cloud-for-id':
            return self._command_list_cloud_snips_for_id()
        if command['comm'] == '--help':
            print('bSnip, simple snippet manager')
            print('COMMANDS:')
            for comm in self.COMMANDS:
                print('{:20} {}'.format(comm, self.COMMANDS[comm]))
        elif command['comm'] == '--version':
            print(__version__)
        return None
