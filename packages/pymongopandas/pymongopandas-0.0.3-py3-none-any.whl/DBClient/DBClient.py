from typing import Mapping, Any, Union, List, Dict
from datetime import datetime

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

import pandas as pd
import pymongo.cursor
from pymongo.results import BulkWriteResult
from pymongo import MongoClient, UpdateOne
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.typings import _Pipeline

from tqdm import tqdm


Query_Options = dict(projection=None, skip=0, limit=0, no_cursor_timeout=False, sort=None, allow_partial_results=False,
                     oplog_replay=False, batch_size=0, collation=None, hint=None, max_scan=None, max_time_ms=None,
                     max=None, min=None, return_key=False, show_record_id=False, snapshot=False, comment=None,
                     session=None, allow_disk_use=None)


class DBClient:
    client: MongoClient
    db: Database
    collections: List[str]
    id_key: str
    progress_bar: bool

    def __init__(self, connection_string: str, db_name: str, id_key: str = None, progress_bar=False):
        self.client = MongoClient(connection_string)
        self.db = self.get_db(db_name)
        self.collections = self.db.list_collection_names()
        self.id_key = id_key if id_key else '_id'
        self.progress_bar = progress_bar

    def get_db(self, db_name: str):
        return self.client[db_name]

    @staticmethod
    def __add_update_time(data: Mapping[str, Any]):
        data.update({'updated_at': datetime.now()})
        return data

    def __add_update_time_list(self, data: List[Dict]):
        return [self.__add_update_time(d) for d in data]

    def __check_collection(self, collection: str):
        if collection not in self.collections:
            raise Exception(f'No collection named {collection}.')

    @staticmethod
    def __parse_options(options: Dict = None) -> Query_Options:
        if not options:
            options = {}
        return options

    def upsert(self, collection: str, query: Mapping[str, Any], data: Union[Mapping[str, Any], _Pipeline], options: None):
        self.__check_collection(collection)
        c: Collection = self.db[collection]
        return c.update_many(
            filter=query,
            update={
                '$set': data
            },
            upsert=True
        )

    def upsert_dataframe(self, collection: str, df: pd.DataFrame, query: Mapping[str, Any] = None, id_key=None, options=None) -> BulkWriteResult:
        self.__check_collection(collection)
        id_key = id_key if id_key else self.id_key
        # range = tqdm(df.iterrows) if self.progress_bar else df.iterrows
        c: Collection = self.db[collection]
        operations = [
            UpdateOne(
                {id_key: r[id_key]},
                {'$set': self.__add_update_time(r.to_dict())},
                upsert=True
            )
            for i, r in tqdm(df.iterrows(), total=df.shape[0])]
        return c.bulk_write(operations)

    def insert_dataframe(self, collection: str, df: pd.DataFrame):
        self.__check_collection(collection)
        self.db[collection].insert_many(df.to_dict())

    def find(self, collection: str, query: Mapping[str, Any] = None, options: Query_Options = None) -> pymongo.cursor.Cursor:
        options = self.__parse_options(options)
        self.__check_collection(collection)
        return self.db[collection].find(query, **options)

    def find_as_df(self, collection: str, query: Mapping[str, Any] = None, remove_id=False, options: Query_Options = None) -> pd.DataFrame:
        cursor = self.find(collection, query, options)
        df = pd.DataFrame(list(cursor))
        if remove_id:
            del df['_id']
        return df


if __name__ == '__main__':
    print('start')
    print('end')
