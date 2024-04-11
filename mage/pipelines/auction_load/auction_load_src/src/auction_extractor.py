#!/usr/bin/env python3
import argparse
import concurrent.futures
from pathlib import Path
from typing import Dict, List

import pandas as pd
from tqdm import tqdm

from utils.utils import Database
from utils.logger import logger
from api import AuctionsIdExtractor_API, Auction_API
from auctionobject import AuctionObject


class AuctionExtractor:
    # single: extract only one auction_id of data.
    # bulk: extract one or more than one auction_id of data.
    EXTRACTOR_TYPES = {'single', 'bulk'}
    
    def __init__(self, type: str, api_url: str, ids_size=None):
        if type not in self.EXTRACTOR_TYPES:
            raise ValueError(f"Invalid extractor type during initialization. Allowed values are {self.EXTRACTOR_TYPES}.")
        self.extractor_type = type
        # ids_size only used for 'bulk' load
        self.ids_size = ids_size
        self.api_url = api_url
        self.load_id = None
        self.db = None

    def load(self):
        # create new db connection
        self.db = Database()
        logger.info(f'Created db connection to {self.db.get_conn_data()}')
        self.load_id = self.db.metadata_get_new_load_id()

        try:
            logger.info(f"Initiating load with load_id: {self.load_id}")
            if self.extractor_type == 'bulk': 
                self.load_bulk()
            elif self.extractor_type == 'single': 
                self.load_single("2113054")
            else: 
                raise Exception("AuctionExtractor.type error")

        except Exception as e:
            logger.error(f"Error during initialization: {e}")

        finally:
            self.db.close()
            logger.close()

    def load_bulk(self):
        """
        Func. to extract bulk auction_ids: auction_ids-> auction_contents-> auction_objects
            :return: None
        """

        # retrieving auction_id's
        auctions_id_extractor = AuctionsIdExtractor_API(api_base_url=self.api_url, size=self.ids_size)
        auction_ids = auctions_id_extractor.fetch_content().get_ids()
        logger.info(f"load_bulk.retrieved new_auction_ids: {auction_ids}")
        
        with tqdm(total=len(auction_ids), desc=f"Bulk loading {len(auction_ids)} auction_id's.", unit="auction_id") as pbar:
            for auction_id in auction_ids:
                self.load_single(auction_id)
                pbar.update(1)

    def load_single(self, auction_id: str) -> None:
        """
        Func. to extract data of one auction (list of up to 50 auction_objects) & write it to db in target tables
            :param auction_id
            :return: None
        """

        def add_to_data(k: str, v: List[dict], dataset: Dict[str, List[dict]]) -> None:

            if (v != [None]) and v:
                if k in dataset:
                    # If the key already exists, append the new list of dictionaries to the existing list
                    for new_entry in v:
                        #testing:
                        #for entry in dataset[k]:
                        #    if entry is None:
                        #        print(entry)
                        if not any(entry.get('id') == new_entry.get('id') for entry in dataset[k]):
                            dataset[k].append(new_entry)
                else:
                    # If the key does not exist, create a new key-value pair
                    dataset[k] = v
            

        # define the output data structures/tables:
        data: Dict[str, List[dict]] = {}

        # Visualisation of the dict, where each key is the table_name:
        """  
        data = {
            "auction_object": [
                {"id": 13134, ..},
                {"id": 2, ..}
            ],
            "auction_asset_status": [
                {"id": 1333, ..},
                {"id": 1334, ..}
            ],
            "auction": [
                {"id": 135233,..},
                {"id": 136547,..}
            ],
            .....
        }
        """

        # Create Auction (collection of 10 to 50 auction objects), data from the API
        auction_obj_set = Auction_API(api_base_url=self.api_url, auction_id=auction_id)

        # fetch data from api
        raw_json = auction_obj_set.fetch_auction_content()

        # archive source json file before processing.
        # auction_obj_set.archive_to_datalake(self.load_id)

        # iterate over the auction objects cleaning/parsing/normalising them
        for auction_obj in raw_json:
            auction_object = AuctionObject(auction_obj)
            auction_object.parse()

            # to "auction_object" table
            auction_obj_parsed = auction_object.auction_obj_parsed
            add_to_data("auction_object", [auction_obj_parsed], data)

            # to "items" table
            items: List[dict] = auction_object.items.items_parsed
            add_to_data("items", items, data)

            # to "document" table
            documents: List[dict] = auction_object.items.documents
            add_to_data("document", documents, data)

            # to "auction" table
            auction = auction_object.auction.auction_parsed
            add_to_data("auction", [auction], data)

            

        logger.info(f"load_single.retrieved new_auction_id: {auction_id}, " 
                    f"tables: {data.keys()}")
        self.db.insert_tables_to_db_stg(load_id=self.load_id, data=data)
        