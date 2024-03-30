import pytest
from src.module.scrapping import Extract


def test_get_links_of_extract():
    assert len(Extract(1, 636).get_links()) == 635
