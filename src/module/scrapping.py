import logging
import sys
from typing import Any, Dict, List

import httplib2
import requests
import setup_logging
from bs4 import BeautifulSoup, SoupStrainer, Tag


class Extract:
    """
    This class is used to extract information from the Steam store website.
    """
    def __init__(self) -> None:
        """
        Initializing the extraction class involves providing the URL from which data
        is to be extracted, as well as specifying the range of pages from which
        extraction is to be performed.
        """
        self.url = "https://store.steampowered.com/search/?"
        self.logger = logging.getLogger(__name__)

    def get_links(self, page_start: int, page_end: int) -> list[str]:
        """
        This method returns a list of all the links on the different page to be extracted.

        Returns:
            list[str]: A list of all the links to be extracted.
        """
        return [self.url + str(f"page={i}") for i in range(page_start, page_end)]

    def retrieval_infos(self, list_of_element: List[str]) -> Dict[str, str]:
        """
        This method facilitates the retrieval of necessary information in a dictionary
        format, ensuring adherence to established standards.

        Args:
            list_of_element (List[str]): A list of all the different information for
                                          each video game.

        Returns:
            Dict[str, str]: A list containing all the information needed for each
                            video game. This list contains a dictionary containing the
                            name of the video game, the price of the game, the creation
                            date of the game, and the corresponding link.
        """
        return {
            'name': list_of_element[-5:-(len(list_of_element) + 1):-1],
            'price': list_of_element[-1],
            'creation_date': list_of_element[-2:-5:-1],
        }

    def insert_corresponding_links(self,
                                   links_page: List[str],
                                   segmented_infos: List[Dict[str, str]]
                                   ) -> List[Dict[str, str]]:
        """
        This method facilitates the retrieval of the appropriate link corresponding to the
        game's accurate name, enabling the addition of the link to the information
        dictionary.

        Args:
            links_page (List[str]): A compilation of links for all video games.
                                    This list must accurately correspond to the respective
                                    pages for extraction.
            segmented_infos (List[Dict[str, str]]): A list containing the initial
                                                    segmentation of various information
                                                    for each video game.

        Returns:
            List[Dict[str, str]]: A list containing all the information needed for each
                                   video game. This list contains a dictionary containing
                                   the name of the video game, the price of the game,
                                   the creation date of the game, and the corresponding
                                   link.
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
        This method is used to parse the content of a given link.

        Args:
            link (str): The link to be parsed.

        Returns:
            List[Dict[str, str]]: A list containing all the information needed for each
                                  video game. This list contains a dictionary containing
                                  the name of the video game, the price of the game,
                                  the creation date of the game, and the corresponding
                                  link.
        """
        page = requests.get(link)
        parser = BeautifulSoup(page.content, 'html.parser')
        infos = list(parser.findAll(class_="responsive_search_name_combined"))
        initial_segmented_infos = [
            self.retrieval_infos(i.get_text().split()) for i in infos]

        http = httplib2.Http()
        status, response = http.request(link)
        b = BeautifulSoup(response, parse_only=SoupStrainer('a'), features="lxml")
        links_page = [i.get('href') for i in b.find_all('a') if "/app/" in i.get('href')]
        return self.insert_corresponding_links(links_page, initial_segmented_infos)

    def mapping_values(raw_infos_extracted: List[Dict[str, str]]) -> List[Any]:
        """_summary_

        Args:
            raw_infos_extracted (List[Dict[str, str]]): _description_

        Returns:
            List[Any]: _description_
        """
        for raw in raw_infos_extracted:
            finale_title = " ".join(raw['name'][::-1])
            date = " ".join(raw['creation_date'][::-1])
            link = raw['link']
            print(link, date, finale_title)
            if (raw['price'] == 'Free') or (raw['price'] == 'Free!') or (raw['price'] == 'Play'):
                price = 0.00
            else:
                price = raw['price'].split("€")
                print(price)
                if len(price) > 2:
                    discounted_price = float(price[1].strip().replace(',', '.'))
                    originale_price = float(
                        price[0].split("%")[-1].strip().replace(',', '.'))
                else:
                    originale_price = float(((price[0]).strip()).replace(',', '.'))
                    discounted_price = None
        return [
            finale_title,
            date,
            originale_price,
            discounted_price,
            link]
