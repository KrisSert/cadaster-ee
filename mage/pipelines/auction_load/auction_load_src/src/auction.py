from dataclasses import dataclass
from copy import deepcopy
from utils.logger import logger

@dataclass
class Auction:
    auction: dict

    owner: str = None
    auctionStatus: str = None
    purpose: str = None
    type: str = None
    contract_type: str = None
    assetOwner: str = None
    assetManager: str = None
    contractDeadlineUnit: str = None

    auction_parsed: dict = None

    def parse_auction(self):
        self.auction_parsed = deepcopy(self.auction)
        
        try:
            for key, value in self.auction.items():

                # owner
                if key == "owner" and isinstance(value, dict) and value:
                    self.owner = value.get("name")
                    self.auction_parsed["owner"] = value.get("name")

                # auctionStatus
                if key == "status" and isinstance(value, dict) and value:
                    self.auctionStatus = value.get("code")
                    self.auction_parsed["status"] = value.get("code")
                    self.auction_parsed["status_name"] = value.get("name")

                # purpose
                if key == "purpose" and isinstance(value, dict) and value:
                    self.purpose = value.get("code")
                    self.auction_parsed["purpose"] = value.get("code")
                    self.auction_parsed["purpose_name"] = value.get("name")

                # type
                if key == "type" and isinstance(value, dict) and value:
                    self.type = value.get("code")
                    self.auction_parsed["type"] = value.get("code")
                    self.auction_parsed["type_name"] = value.get("name")

                # contract_type
                if key == "contractType" and isinstance(value, dict) and value:
                    self.type = value.get("name")
                    self.auction_parsed["contractType"] = value.get("name")

                # assetOwner
                if key == "assetOwner" and isinstance(value, dict) and value:
                    self.assetOwner = value.get("name")
                    self.auction_parsed["assetOwner"] = value.get("name")

                # assetManager
                if key == "assetManager" and isinstance(value, dict) and value:
                    self.assetManager = value.get("name")
                    self.auction_parsed["assetManager"] = value.get("name")

                # contractDeadlineUnit
                if key == "contractDeadlineUnit" and isinstance(value, dict) and value:
                    self.contractDeadlineUnit = value.get("code")
                    self.auction_parsed["contractDeadlineUnit"] = value.get("code")
                    self.auction_parsed["contractDeadlineUnit_name"] = value.get("name")

        except Exception as e:
            logger.error(f"issue in class.auction parsing auction: error message {e}")