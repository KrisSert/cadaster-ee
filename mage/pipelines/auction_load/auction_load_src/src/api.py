import requests
import json
import os
from typing import Dict, List
from datetime import datetime

from mage.pipelines.auction_load.auction_load_src.src.utils import utils as u


class AuctionsIdExtractor_API:
    def __init__(self, api_base_url, mode='FULL', size=1000):
        self.api_response = None
        self.api_response_ids: List[str] = None
        self.api_mode = mode
        self.size = size

        if self.api_mode == 'FULL':
            self.api_url = (f"{api_base_url}/auction?size={self.size}&searchType.equals=COMPLEX&searchFinishedAuctions"
                            f".contains=true")
        else:
            self.api_url = (f"{api_base_url}/auction?size={self.size}&searchType.equals=COMPLEX&searchFinishedAuctions"
                            f".contains=false")

    def fetch_content(self):
        """ Fetch the auction's objects
            :return data in json
        """
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            self.api_response = response.json()
            if self.api_response:
                return self
            else:
                raise Exception(f"No data returned via api request {self.api_url}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def get_ids(self):
        """ Fetch all the auctions id's
            :return list of id's
        """
        self.api_response_ids = [auction['id'] for auction in self.api_response]
        return self.api_response_ids


class Auction_API:
    def __init__(self, api_base_url: str, auction_id: str):
        self.api_url = (f"{api_base_url}/auction/object?page=0&size=100&filterType.equals=COMPLEX&"
                        f"auctionId.equals={auction_id}&alsoFinishedAuctionObjects.equals=true")
        self.auction_content = None
        self.auction_id = auction_id

    """
    
    def archive_to_datalake(self, load_id: int) -> None:
        '''
        Store the api response before processing.
        '''
        # Go back one folder
        target_folder_path = os.path.join(os.getcwd(), 'datalake')
        if not os.path.exists(os.path.dirname(target_folder_path)):
            os.makedirs(target_folder_path)

        # create new file_name
        current_date = datetime.now().strftime("%Y_%m_%d")
        base_filename = f"{str(load_id)}_{current_date}_{self.auction_id}"
        filename = os.path.join(target_folder_path, base_filename) 
        
        # Check if the file already exists
        existing_files = [file for file in os.listdir(target_folder_path) if file.startswith(base_filename)]
        count = 0
        while f"{base_filename}_{count}" in existing_files:
            count += 1
        filename = os.path.join(target_folder_path, f"{base_filename}_{count}.json")

        try:
            if self.auction_content:
                with open(filename, "w") as json_file:
                    json.dump(self.auction_content, json_file)
                ## TODO
                pass
        except Exception as e:
            # TODO
            pass
    """

    def fetch_auction_content(self):
        """ Fetch the auction's objects
            :return data in json
        """
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            self.auction_content = response.json()
            if self.auction_content:
                return self.auction_content
            else:
                raise Exception(f"No data returned via api request {self.api_url}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def beautify_json(self):
        formatted_json = json.dumps(self.auction_content, indent=4)
        return formatted_json