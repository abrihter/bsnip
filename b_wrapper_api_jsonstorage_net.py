#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
wrapper-api-jsonstorage-net

Wrapper for jsonstorage.net API, created by Alexander Doroshenko

Allow users to manipulate JSON objects on jsonstorage.net

versions:
    V1.0.0 [05.04.2019]
        - first wrking version
'''

__author__ = "Bojan"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Bojan"
__status__ = "Development"

import requests

class bErrorCreatingJSONObject(Exception):
    pass

class bErrorLoadingJSONObject(Exception):
    pass

class bErrorUpdatingJSONObject(Exception):
    pass

class bAPIWrapperJsonstorageNet:
    '''wrapper class'''

    api_endpoint = 'https://jsonstorage.net/api/items'

    def _extract_id_from_response(self, jsn):
        '''extract object id from response
        :para json jsn: JSON object
        :return str: Returns JSON object ID or None on issue
        '''
        try:
            return jsn['uri'].split('/')[-1].strip()
        except:
            return None

    def create(self, jsn):
        '''create json object
        :param json jsn: JSON object to create
        :retrun str: Returns ID of saved object or raise exception
        '''
        r = requests.post(self.api_endpoint, json=jsn)
        if r.status_code == 201:
            return self._extract_id_from_response(r.json())
        raise bErrorCreatingJSONObject(
            'Error creating JSON object. Code {}'.format(r.status_code))

    def load(self, object_id):
        '''load json object
        :param str object_id: JSON object ID
        :retrun json: Returns JSON object or raise exception
        '''
        r = requests.get('{}/{}'.format(self.api_endpoint, object_id))
        if r.status_code == 200:
            return r.json()
        raise bErrorLoadingJSONObject(
            'Error loading JSON object. Code {}'.format(r.status_code))

    def update(self, object_id, jsn):
        '''update json object
        :param str object_id: JSON object ID
        :param json jsn: JSON object to update
        :retrun bool: Returns TRUE if object updated or raise exception
        '''
        r = requests.put('{}/{}'.format(
            self.api_endpoint, object_id), json=jsn)
        if r.status_code == 201:
            return True
        raise bErrorUpdatingJSONObject(
            'Error updating JSON object. Code {}'.format(r.status_code))
