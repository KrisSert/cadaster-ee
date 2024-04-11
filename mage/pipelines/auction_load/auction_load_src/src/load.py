#!/usr/bin/env python3
import argparse
import concurrent.futures
from pathlib import Path
from typing import Dict, List

from utils.logger import logger
from api import AuctionsIdExtractor_API, Auction_API
from auctionobject import AuctionObject
from auction_extractor import AuctionExtractor


if __name__ == "__main__":
    # Set up argparse
    parser = argparse.ArgumentParser(description='Extract auctions data from "Estonian Land Registry"/"Maa-amet" '
                                                 'auction environment via API.')

    parser.add_argument('-api_url', type=str, default='https://riigimaaoksjon.ee/public-api',
                        help='Base URL of the API. default=https://riigimaaoksjon.ee/public-api')
    parser.add_argument('-f', '--full_mode', action='store_true',
                        help='Use this option to modify the nr auctions data you want to pull to max=700, '
                             'otherwise it uses the default value 10')
    parser.add_argument('-a', '--ids_size', type=int, default=5,
                        help='Number of auctions to fetch data for')

    # arguments for defining tables which are to be populated.
    # parser.add_argument('-auctionobject')
    # parser.add_argument('-auction')
    # parser.add_argument('-items')
    # parser.add_argument('-documents')
    # parser.add_argument('-documenttype')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Set ids_size based on the presence of --full_mode or the value provided with -auctions
    ids_size = 700 if args.full_mode else args.ids_size


    # Log the command-line arguments
    logger.info(f'Command-line arguments: {args}')

    #extraction for single auction
    '''
    auction_extractor = AuctionExtractor(type='single',
                                         auction_id=auction_id,
                                         api_url=args.api_url,
                                         logger=logger)
    auction_extractor.load()
    extract_bulk_auction_data()
    '''

    #exctraction for more than one auction_id (incl. historical load)
    auction_extractor = AuctionExtractor(type='bulk',
                                         api_url=args.api_url,
                                         ids_size=ids_size)
    auction_extractor.load()
