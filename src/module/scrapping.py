import logging
from datetime import datetime
from typing import Any, Dict, List

import httplib2
import requests
from bs4 import BeautifulSoup, SoupStrainer, Tag


class Extract:
    """
    The class is used to extract information from the Steam store website.
    """
    def __init__(self) -> None:
        """
        Initializing the extraction class involves providing the URL from which data
        is to be extracted, as well as specifying the range of pages from which
        extraction is to be performed.
        """
        self.url = "https://store.steampowered.com/search/?"
        self.logger = logging.basicConfig(
            format='%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%m-%d-%Y %H:%M:%S',
            level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def get_links(self, page_start: int, page_end: int) -> list[str]:
        """
        The method returns a list of all the links on the different page to be extracted.

        Returns:
            list[str]: A list of all the links to be extracted.
        """
        return [self.url + str(f"page={i}") for i in range(page_start, page_end)]

    def retrieval_infos(self, list_of_element: List[str]) -> Dict[str, str]:
        """
        The method facilitates the retrieval of necessary information in a dictionary
        format, ensuring adherence to established standards.

        Args:
            list_of_element (List[str]): A list of all the different information for each
            video game.

        Returns:
            Dict[str, str]: A list containing all the information needed for each video
            game. This list contains a dictionary containing the name of the video game,
            the price of the game, the creation date of the game, and the corresponding
            link.
        """
        return {
            'name': list_of_element[-5:-(len(list_of_element) + 1):-1],
            'price': list_of_element[-1],
            'creation_date': list_of_element[-2:-5:-1],
            'extraction_date': datetime.now().date()
        }

    def insert_corresponding_links(self,
                                   links_page: List[str],
                                   segmented_infos: List[Dict[str, str]]
                                   ) -> List[Dict[str, str]]:
        """
        The method facilitates the retrieval of the appropriate link corresponding to the
        game's accurate name, enabling the addition of the link to the information
        dictionary.

        Args:
            links_page (List[str]): A compilation of links for all video games.
            This list must accurately correspond to the respective pages for extraction.

            segmented_infos (List[Dict[str, str]]): A list containing the initial
            segmentation of various information for each video game.

        Returns:
            List[Dict[str, str]]: A list containing all the information needed for each
            video game. This list contains a dictionary containing the name of the video
            game, the price of the game, the creation date of the game, and the
            corresponding link.
        """
        updated_list = list()
        for link in links_page:
            for value in segmented_infos:
                if len(value['name']) > 1:
                    if value['name'][::-1][0] in link and value['name'][::-1][1] in link:
                        value['link'] = link
                        updated_list.append(value)
                else:
                    if len(value["name"]) != 0:
                        if value['name'][::-1][0] in link:
                            value['link'] = link
                            updated_list.append(value)
        return updated_list

    def parse_content(self, link: str) -> List[Dict[str, str]]:
        """
        The method is used to parse the content of a given link.

        Args:
            link (str): The link to be parsed.

        Returns:
            List[Dict[str, str]]: A list containing all the information needed for each
            video game. This list contains a dictionary containing the name of the video
            game, the price of the game, the creation date of the game, and the
            corresponding link.
        """
        page = requests.get(link)
        parser = BeautifulSoup(page.content, 'html.parser')
        infos = list(parser.findAll(class_="responsive_search_name_combined"))
        initial_segmented_infos = [
            self.retrieval_infos(i.get_text().split()) for i in infos]

        to_review = [
            one_info for one_info in initial_segmented_infos
            if '€' not in one_info.get('price') and 'Free' not in one_info.get('price')]

        self.logger.warning(f"There are {len(to_review)} data that should be reviewed.")
        if len(to_review) != 0:
            self.logger.info(f"{to_review} details that should be reviewed.")

        http = httplib2.Http()
        status, response = http.request(link)
        b = BeautifulSoup(response, parse_only=SoupStrainer('a'), features="lxml")
        links_page = [i.get('href') for i in b.find_all('a') if "/app/" in i.get('href')]
        return self.insert_corresponding_links(links_page, initial_segmented_infos)
