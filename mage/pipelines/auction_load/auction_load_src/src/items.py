from dataclasses import dataclass, field
from typing import List
from copy import deepcopy

from utils.logger import logger

@dataclass
class Items:
    items: List[dict]
    areaUnit: str = None 
    intendedUse: str = None 
    documents: List[dict] = None  # elements will go into documents table
    documentType: List[str] = field(default_factory=list) 
    items_parsed: List[dict] = None

    def parse_items(self):
        self.items_parsed = deepcopy(self.items)

        for index, item in enumerate(self.items):

            try:
                # parse areaUnit
                if item["areaUnit"]:
                    self.areaUnit = item["areaUnit"].get("name")
                    area_unit_name = item["areaUnit"].get("name")
                    self.items_parsed[index]["areaUnit"] = area_unit_name

            except Exception as e:
                logger.error(f"issue in class.items parsing areaUnit: error message {e}")

            try:
                # parse intendedUse
                self.items_parsed[index]["intendedUse"] = []
                for use in item["intendedUse"]:
                    name = use.get("name")
                    perc = use.get("percentage")
                    new_value = f'{perc}%:{name}'
                    self.items_parsed[index]["intendedUse"].append(new_value)
                self.items_parsed[index]["intendedUse"] = ",".join(self.items_parsed[index]["intendedUse"])

            except Exception as e:
                logger.error(f"issue in class.items parsing intendedUse: error message {e}")

            try:
                # parse documents
                if item["documents"]:
                    self.documents = item["documents"]
                    self.items_parsed[index]["documents"] = []
                    for doc_index, doc in enumerate(item["documents"]):
                        
                        if doc["type"] and isinstance(doc["type"], dict):
                            # add documentType of document
                            self.documentType.append(doc["type"]["name"])
                            # make the documentType in the document dict into just the name.
                            self.documents[doc_index]["type"] = doc["type"]["name"]
                            # add document id's to items_parsed
                            self.items_parsed[index]["documents"].append(str(item["documents"][doc_index]["id"]))

                    self.items_parsed[index]["documents"] = ",".join(self.items_parsed[index]["documents"])
                elif not item["documents"]:
                    # if documents is empty list, set it to None.
                    self.items_parsed[index]["documents"] = None

            except Exception as e:
                logger.error(f"issue in class.items parsing documents: error message {e}")
