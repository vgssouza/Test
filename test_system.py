import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from app import app, get_db, init_db


class TestSistema(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')
        init_db()

    def tearDown(self):
        self.driver.quit()

    def test_register_and_login(self):
        driver = self.driver
        driver.find_element_by_link_text('Registre-se aqui').click()
        username = driver.find_element_by_name('username')
        password = driver.find_element_by_name('password')
        username.send_keys('testuser')
        password.send_keys('testpassword')
        password.send_keys(Keys.RETURN)
        assert 'Arquivos disponíveis para download' in driver.page_source

    def test_upload_file(self):
        driver = self.driver
        driver.find_element_by_link_text('Registre-se aqui').click()
        username = driver.find_element_by_name('username')
        password = driver.find_element_by_name('password')
        username.send_keys('testuser')
        password.send_keys('testpassword')
        password.send_keys(Keys.RETURN)
        driver.find_element_by_name('file').send_keys('path_to_file')
        driver.find_element_by_xpath(
            "//button[contains(text(),'Upload')]").click()
        assert 'File uploaded to Azure' in driver.page_source

    def test_download_file(self):
        driver = self.driver
        driver.find_element_by_link_text('Registre-se aqui').click()
        username = driver.find_element_by_name('username')
        password = driver.find_element_by_name('password')
        username.send_keys('testuser')
        password.send_keys('testpassword')
        password.send_keys(Keys.RETURN)
        driver.find_element_by_link_text('file_name').click()
        assert 'File downloaded successfully' in driver.page_source


if __name__ == '__main__':
    unittest.main()
