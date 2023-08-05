import os
import logging
from typing import Callable

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from webdriver_manager.chrome import ChromeDriverManager


class BaseWebInteractor:
    """ """

    def __init__(
        self,
        headless: bool = True,
        wait_time: int = 5,
        logging_level: int = 20,  # This is equal to logging.INFO
        *args,
        **kwargs,
    ):
        """
        Parameters
        ----------
        headless : bool
            Whether to run selenium in headless mode or not
        wait_time : int
            The time in seconds for selenium to wait for elements before timing out
            See more here <https://www.selenium.dev/documentation/en/webdriver/waits/>

        Returns
        -------
        None
        """
        chrome_options = webdriver.ChromeOptions()
        self.headless = headless
        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("window-size=1024,768")
            chrome_options.add_argument("--no-sandbox")
        # TODO: Remove the next line if unnecessary
        # Added due to this issue <https://stackoverflow.com/a/65497385/4260991>
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options
        )
        self.wait_time = wait_time
        self.ignored_exceptions = (
            NoSuchElementException,
            StaleElementReferenceException,
        )
        logging.basicConfig(level=logging_level)

    def find(self, by: str, identifier: str):
        """Find an element

        by (str):
            The method to use in the identifier
            See acceptable values here
            <https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.by.html>
        identifier (str):
            The identifier for the element to find
        """
        result = WebDriverWait(
            self.driver, self.wait_time, ignored_exceptions=self.ignored_exceptions
        ).until(expected_conditions.presence_of_element_located((by, identifier)))
        return result

    def find_multiple(self, by: str, identifier: str):
        """Find a list of elements

        Args:
            by (str): The method to use in the identifier
            identifier (str): _description_

        Returns:
            _type_: _description_
        """
        result = WebDriverWait(
            self.driver, self.wait_time, ignored_exceptions=self.ignored_exceptions
        ).until(expected_conditions.presence_of_all_elements_located((by, identifier)))
        return result

    def data_to_sql(
        self,
        data_collector: Callable,
        name: str,
        con,
        schema=None,
        if_exists: str = "fail",
        **kwargs,
    ):
        """Runs a function that outputs a pandas dataframe and commits it to a
        database.

        Parameters
        ----------
        data_collector : Callable
            A function that will run some selenium code and return a pandas
            dataframe.
        name : str
            Name of SQL table.
            See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
        con : sqlalchemy.engine.(Engine or Connection) or sqlite3.Connection
            Using SQLAlchemy makes it possible to use any DB supported by that library.
            See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
        schema : str, optional
            Specify the schema (if database flavor supports this). If None, use default schema.
            See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
        if_exists : {‘fail’, ‘replace’, ‘append’}, default ‘fail’
            How to behave if the table already exists.
                fail: Raise a ValueError.
                replace: Drop the table before inserting new values.
                append: Insert new values to the existing table.
            See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html

        Returns
        -------
        None

        """
        # try:
        df = data_collector(**kwargs)
        df.to_sql(name=name, con=con, schema=schema, if_exists=if_exists, index=False)
        # except e:
        #     logging.debug(e)
        return df

    def data_to_bigquery(
        self,
        data_collector: Callable,
        table_id: str,
    ):
        pass

    def data_to_csv(
        self,
        data_collector: Callable,
        path: str,
        if_exists: str = "fail",
    ):
        """Runs a function that outputs a pandas dataframe and commits it to a CSV file.

        Args:
            data_collector (Callable): A function that will run some selenium code and return a pandas dataframe.
            path (str): A path to the CSV file.
            if_exists (str, optional): What to do if a file already exists at the specified path. Defaults to "fail".
        """
        df = data_collector()
        if if_exists == "fail":
            if os.path.exists(path):
                raise FileExistsError(f"File already exists at {path}")
        df.to_csv(path, index=False)
