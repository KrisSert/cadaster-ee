from typing import Dict, List

from mage.pipelines.auction_load.auction_load_src.src.api import AuctionsIdExtractor_API, Auction_API
from mage.pipelines.auction_load.auction_load_src.src.auctionobject import AuctionObject
from mage.pipelines.auction_load.auction_load_src.src.auction_extractor import AuctionExtractor

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def auction_load(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    
    api_url = 'https://riigimaaoksjon.ee/public-api'
    ids_size = 3
    
    # exctraction for more than one auction_id (incl. historical load)
    auction_extractor = AuctionExtractor(type='bulk',
                                         api_url=api_url,
                                         ids_size=ids_size)
    auction_extractor.load()

    return {None}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
