import pathlib
import pathlib
import pytest

from selenium import webdriver
from hunter_automation.Beon import Beon, Careers

DRIVER_PATH = pathlib.Path(__file__).parent.parent / 'webdrivers' / 'chromedriver.exe'


@pytest.fixture()
def chrome_driver():
    driver = webdriver.Chrome(executable_path=str(DRIVER_PATH))
    yield driver
    # driver.close()


def test_main_flow(chrome_driver):
    # 1. Click on Join Us
    main_page = Beon(chrome_driver)
    main_page.join_us()

    # 2. Choose any filter by selecting from the 3 dropdowns options
    carrers_page = Careers(chrome_driver)
    carrers_page.search_for()

    # 3. Verify the result of these filters is correct
    filters = carrers_page.get_filter_values()
    print(filters)
    job_offers = carrers_page.get_search_results()
    if filters.offers > 0:
        # Assert results match filter
        for offer in job_offers:
            print(offer)
            print([filters.role in offer.title, filters.tech in offer.tech, filters.business in offer.business])
            assert all([filters.role in offer.title, filters.tech in offer.tech, filters.business in offer.business])
    else:
        # Assert the no results message is shown
        assert not carrers_page.has_results()
