from dataclasses import dataclass
from copy import deepcopy

from items import Items
from auction import Auction
from utils.logger import logger

@dataclass
class AuctionObject:
    auction_obj_json: dict
    
    status: str = None  # can only contain (one dict) as a value (only 1 status)
    areaUnit: str = None  # can only contain (one dict or Null) as a value
    
    items: Items = None
    auction: Auction = None
    
    auction_obj_parsed: dict = None

    def parse(self):
        self.auction_obj_parsed = deepcopy(self.auction_obj_json)

        try: 
            for key, value in self.auction_obj_json.items():

                if key == "status" and isinstance(value, dict):
                    if value:
                        self.status = value.get("code")
                        self.auction_obj_parsed[key] = value.get("code")
                        self.auction_obj_parsed["status_name"] = value.get("name")
                    else:
                        self.auction_obj_parsed[key] = None

                elif key == "items" and isinstance(value, list):
                    if value:
                        self.items = Items(value)

                        auction_item_ids = []
                        for item in value:  # for item in items(list of)
                            if isinstance(item, dict):
                                first_key, first_value = next(iter(item.items()), (None, None))
                                if first_key == "id":
                                    auction_item_ids.append(str(first_value))
                        self.auction_obj_parsed[key] = ",".join(auction_item_ids)
                    else:
                        self.auction_obj_parsed[key] = None

                elif key == "auction" and isinstance(value, dict):
                    if value:
                        self.auction = Auction(value)

                        first_key, first_value = next(iter(value.items()), (None, None))
                        if first_key == "id":
                            self.auction_obj_parsed[key] = first_value
                    else:
                        self.auction_obj_parsed[key] = None

                elif key == "areaUnit" and isinstance(value, dict):
                    if value:
                        self.areaUnit = value.get("name")
                        self.auction_obj_parsed[key] = value.get("name")
                    else:
                        self.auction_obj_parsed[key] = None

        except Exception as e:
            logger.error(f"issue in class.auctionobject parsing auctionobject: error message {e}")

        self.items.parse_items()
        self.auction.parse_auction()

    def remove_newlines(self):
        def remove_newlines_recursive(obj):
            """Recursively remove newline characters from dictionary values."""
            for key, value in obj.items():
                if isinstance(value, dict):
                    # If the value is another dictionary, call the function recursively
                    obj[key] = remove_newlines_recursive(value) if value is not None else None
                elif isinstance(value, (list, tuple)):
                    # If the value is a list or tuple, iterate through its items
                    obj[key] = [remove_newlines_recursive(item) if item is not None else None for item in value]
                elif isinstance(value, str):
                    # If the value is a string, replace newline characters
                    obj[key] = value.replace('\n', ' ')
            return obj

        self.auction_obj_parsed = remove_newlines_recursive(self.auction_obj_parsed)
