import time

from selenium.webdriver.common.by import By

from test_selenium.page.base_page import BasePage
from test_selenium.page.contact import Contact
from test_selenium.page.material import Material
from test_selenium.page.message import Message


class Main(BasePage):
    _base_url = 'https://work.weixin.qq.com/wework_admin/frame#index'

    def download_app(self):
        pass

    def import_user(self, file):
        # upload file of excel
        self.find((By.PARTIAL_LINK_TEXT, '导入成员')).click()
        self.find((By.CSS_SELECTOR, 'a[d_ck="importJump"]')).click()
        self.find((By.CSS_SELECTOR, '#js_upload_file_input')).send_keys(file)
        self.find((By.CSS_SELECTOR, '#submit_csv')).click()
        self.find((By.CSS_SELECTOR, '#reloadContact')).click()
        return self

    def goto_company(self):
        pass

    def show_message(self):
        return True

    def add_member(self):
        locator = (By.LINK_TEXT, '添加成员')
        self.find(locator).click()
        # self._driver.execute_script('arguments[0].click();', self.find(locator))
        return Contact(reuse=True)

    def member_info(self, member_name):
        self.find(By.CSS_SELECTOR, '#menu_contacts').click()
        # 当前部门尚有x人未加入的提示会影响点击错位
        time.sleep(2)
        self.find(By.CSS_SELECTOR, 'td[title="%s"]' % member_name).click()
        self.find(By.CLASS_NAME, 'js_edit').click()
        return Contact(reuse=True)

    def send_message(self):
        self.find(By.CSS_SELECTOR, '.js_groupMessage').click()

        return Message(reuse=True)

    def add_material(self):
        self.find((By.CSS_SELECTOR, '#menu_manageTools')).click()
        self.find(By.CSS_SELECTOR, 'a[href="#material/text"]').click()
        return Material(reuse=True)
