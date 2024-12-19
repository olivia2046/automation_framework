import pytest
from selenium import webdriver

from proj_spec.triplog.web.po.login.login_page import TriplogLoginPage




# @pytest.fixture(scope="class")
# def browser():
#     driver = webdriver.Chrome() #todo
#     yield driver
#     driver.quit()



# def browser_setup():
#     options = Options()
    # options.add_argument("--no-sandbox")
    # options.add_argument("--headless")
    # options.add_argument("--disable-dev-shm-urage")
    # options.add_argument("--start-maximized")
    # options.add_argument("--no-gpu")
    # options.add_argument("--incognito")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--disable-infobars")


@pytest.fixture(scope="class",autouse=True)
def driver_init(request):
    from base.getdata import GetData
    from base.get_config import GetConfig
    caps = GetConfig.get_capabilities()
    browser_name = caps['browserName']
    if browser_name=='Chrome':
        driver = webdriver.Chrome()
    elif browser_name=='Firefox':
        driver = webdriver.Firefox()
    elif browser_name=='Edge':
        driver = webdriver.Edge()
    request.cls.driver = driver
    login_page = TriplogLoginPage(request.cls.driver)
    if request.cls.user_identifier is not None:
        email, password = GetData.get_user_credential(request.cls.user_identifier)
        request.cls.overview_page = login_page.login(email, password)
    yield
    driver.quit()


