import pytest
from ak_selenium import Chrome

@pytest.fixture(scope="module")
def chrome_instance():
    chrome = Chrome(headless=True)
    yield chrome
    del chrome

def test_init_chrome(chrome_instance):
    assert chrome_instance.init_chrome()

def test_implicitly_wait_time(chrome_instance):
    assert chrome_instance.IMPLICITLY_WAIT_TIME == 3

def test_max_wait_time(chrome_instance):
    assert chrome_instance.MAX_WAIT_TIME == 5

def test_chrome_user_agent(chrome_instance):
    assert chrome_instance.USERAGENT == 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/83.0.4103.53 Safari/537.36'

def test_half_screen(chrome_instance):
    assert chrome_instance.half_screen is True

def test_str_method(chrome_instance):
    assert str(chrome_instance) == f"""
        Chrome.Object
        UserAgent:{chrome_instance.USERAGENT}
        Implicit Wait Time: {chrome_instance.IMPLICITLY_WAIT_TIME:.2f}s
        Max Wait Time: {chrome_instance.MAX_WAIT_TIME:.2f}s
        Headless: {chrome_instance.headless}
        Chrome Userdata Path: {chrome_instance.chrome_userdata_path}
        Half Screen View: {chrome_instance.half_screen}
        """