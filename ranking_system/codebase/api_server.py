# -*- coding: utf-8 -*-
from flask import request
from flask_api import FlaskAPI
from bson import json_util
# logging
import traceback
import logging
# get config
import yaml
# external modules
import db_helper
import find_helper as findhelper




class Api:
    """
            class for rest interaction
            """
    def __init__(self):
        cfg = yaml.safe_load(open("config.yaml"))
        mongourl = cfg['mongourl']
        database = cfg['database']
        collection = cfg['collection']
        collection_new = cfg['collection_new']
        self.db = db_helper.Db(mongourl, database, collection)
        self.db_new = db_helper.Db(mongourl, database, collection_new)
        self.find = findhelper.Find()
        self.app = FlaskAPI(__name__)
        self.app.add_url_rule("/search/","search", self.search, methods=['POST'])
        self.app.add_url_rule("/populate/","populate", self.insert, methods=['POST'])
        self.app.add_url_rule("/search_trans/","search_trans", self.search_trans, methods=['POST'])
        self.app.add_url_rule("/populate_trans/","populate_trans", self.insert_trans, methods=['POST'])
        self.app.add_url_rule("/find_image/","find_image", self.find_image, methods=['POST'])
        logging.debug('Api has been initialized')


    def search(self):
        """
        get request, search in db for data
        """
        data = request.get_json()
        response = self.db.search_records(data)
        return json_util.dumps(response)

    def insert(self):
        """
        Get POST json. populate db
        """
        data = request.get_json()
        res = self.db.write_record(data)
        return str(res)

    def search_trans(self):
        """
        get request, search in db for data
        """
        data = request.get_json()
        response = self.db_new.search_records(data)
        return json_util.dumps(response)

    def insert_trans(self):
        """
        Get POST json. populate db
        """
        data = request.get_json()
        res = self.db_new.write_record(data)
        return str(res)

    def find_image(self):
        """
        get json with 'photo' : %photo_name%
        :return: search results
        https://pp.userapi.com/c851216/v851216826/efbc4/pnz7eaWD3b8.jpg
        db_new.search_record({'photos_name':{'$elemMatch':{'$in':['pnz7eaWD3b8.jpg']}}})
        """
        try:
            data = request.get_json()
            logging.debug(data)
            response = self.find.main(data['photo'])
            return json_util.dumps(response)
        except Exception:
            logging.error(traceback.format_exc())

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    Api().app.run(host='0.0.0.0', debug=False, threaded=False)
