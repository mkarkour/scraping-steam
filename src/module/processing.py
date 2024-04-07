import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pandas as pd
from pandas import DataFrame, Series


class Transform:
    """
    This class is used to transform the scraped data into a usable format.
    """
    def __init__(self) -> None:
        """
        Initialize the Transform class by setting the logging level.
        """
        self.logger = logging.basicConfig(
            format='%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%m-%d-%Y %H:%M:%S',
            level=logging.INFO)

    def transform_to_df(self, list_of_scrapes_data: List[Dict[str, str]]) -> DataFrame:
        """
        This method transforms the scraped data into a usable format.

        Args:
            list_of_scrapes_data (List[Dict[str, str]]): A list of dictionaries containing
            the scraped data.

        Returns:
            DataFrame: A pandas dataframe containing the transformed data.
        """
        return pd.concat([pd.DataFrame(raw_data) for raw_data in list_of_scrapes_data])

    def transform_date(self, creation_date_col: List[str]) -> str:
        """_summary_

        Args:
            creation_date_col (List[str]): _description_

        Returns:
            str: _description_
        """
        return (" ".join(creation_date_col[::-1])).replace(",", "")

    def transform_price(self, price_col: str) -> Series:
        """_summary_

        Args:
            price_col (str): _description_

        Returns:
            Series: _description_
        """
        if '€' not in price_col or 'Free' in price_col or 'Free!' in price_col:
            original_price = 0.00
            final_price = 'free game'

        elif '%' not in price_col:
            original_price = float(price_col.replace('€', '').replace(',', '.'))
            final_price = 0.00

        else:
            prices = price_col.split('%')[-1].split('€')
            original_price = float(prices[0].replace(",", "."))
            final_price = float(prices[1].replace(",", "."))

        return pd.Series({'original_price': original_price, 'final_price': final_price})

    def clean_and_transform_data(self, raw_df: DataFrame) -> Tuple[DataFrame, DataFrame]:
        """
        This method cleans and transforms the raw data scraped to have the correct format
        and returns the cleaned and transformed data.

        Args:
            raw_df (DataFrame): A DataFrame containing the raw data scraped from steam.

        Returns:
            DataFrame: The DataFrame containing the cleaned and transformed data.
            DataFrame: The DataFrame containing invalid data.
        """
        not_good_price = raw_df[~raw_df['price'].str.contains('€|Free', na=False)]
        raw_df.drop(not_good_price.index, inplace=True)

        raw_df['name'] = raw_df['name'].apply(lambda x: " ".join(x[::-1]))
        raw_df['creation_date'] = raw_df['creation_date'].apply(
            lambda x: self.transform_date(x))

        idx_loc, value_loc = [], []
        for idx, value in enumerate(raw_df['creation_date']):
            try:
                datetime.strptime(value, '%d %b %Y')

            except ValueError:
                idx_loc.append(idx)
                value_loc.append(value)

        not_good_date = raw_df.iloc[idx_loc]
        not_good = pd.concat([not_good_date, not_good_price])
        raw_df.drop(not_good_date.index, inplace=True)
        raw_df['creation_date'] = raw_df['creation_date'].apply(
            lambda x: datetime.strptime(x, '%d %b %Y'))
        raw_df[['original_price', 'final_price']] = raw_df['price'].apply(
            lambda x: self.transform_price(x))
        raw_df.drop(columns=['price'], inplace=True)

        return raw_df, not_good
