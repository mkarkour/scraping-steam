import pytest

from src.module.scrapping import Extract


@pytest.fixture
def extract_instance():
    return Extract()


@pytest.fixture
def extract_links():
    return Extract().get_links(1, 2)


def test_get_links_of_extract(extract_instance):
    assert len(extract_instance(1, 636).get_links()) == 635


def test_type_get_links_of_extract(extract_instance):
    assert type(extract_instance.get_links()) is type(list())


def test_parse_content_of_extract(extract_instance, extract_links):
    assert len(extract_instance.parse_content(extract_links[0])) == 25
