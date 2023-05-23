from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import itertools
import time

# TODO: Create another class for encapsulation of dashboards params.

class BrowserHandler:
    '''
    A class that iteratively displays dashbords using Chrome in kiosk mode.
    ---
    Attributes
    ---
    dashboards: dict
        A python dict that contains a list of dashboards and some configuration settings. Times must be entered in seconds.
        Example:
            {
              "dashboards": [
                {
                  "url": "",
                  "update_every": 180,
                  "how_long_to_stay": 60,
                  "updated_at": ""
                }
              ]
            }
    '''
 
    def __init__(self, dashboards):
        self.open_tabs = {}
        self.dashboards = dashboards.get('dashboards')

    def start_browser(self, kiosk=True):
        # Open Chrome webdrive and navigates to the login of your Tableau instance.
        chrome_options = Options()
        if kiosk:
            chrome_options.add_argument("--kiosk")
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(options=chrome_options)

    def set_open_tabs(self):
        # Assign values ​​to the attribute with configuration data
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            for dashboard in self.dashboards:
                if self.driver.current_url == dashboard.get('url'):
                    self.open_tabs[handle] = dashboard

    def open_dashboards(self):
        # Opens Chrome tabs with all dashboards contained in the dashboards dict and sets open_tabs attribute.
        counter=0
        for dashboard in self.dashboards:
            if counter == 0:
                self.driver.get(dashboard.get('url'))
                self.driver.switch_to.window(self.driver.window_handles[counter])
                self.open_tabs[self.driver.window_handles[counter]] = dashboard
                counter += 1
            else:
                self.driver.execute_script(f"window.open('{dashboard.get('url')}');")
                self.driver.switch_to.window(self.driver.window_handles[counter])
                self.open_tabs[self.driver.window_handles[counter]] = dashboard
                counter += 1
        time.sleep(5)
        self.set_open_tabs()

    def login(self, tool, username=None, password=None, login_url=None):    
        # Log in to the BI Tool selected using the classes of that tool. 
        # Also assigns an instance of the tool class to the attributes of this class.
        if tool == 'Tableau':
            self.tableau = Tableau(driver=self.driver, username=username, password=password, login_url=login_url)
            self.tableau.login()
        elif tool == 'Looker':
            self.looker = Looker(driver=self.driver, username=username, password=password, login_url=login_url)
            self.looker.login()

    def start_mirroring(self, tv_name):
        # Start mirroring your Chorme tab to the device informed. *The device must have chromecast or similar technology
        try:
            self.driver.get_sinks()
            self.driver.start_desktop_mirroring(sink_name=tv_name)
        except:
            print("The TV is not ready yet or is not available.")

    def loop_through_tabs(self, refresh=True):
        # Loops through Chrome tabs applying refresh and wait rules for each Tool.
        for handle in itertools.cycle(self.open_tabs):
            self.driver.switch_to.window(handle)
            tab = self.open_tabs[handle]

            if tab['type'] == 'Tableau':
                self.tableau.check_reconnect()
                if refresh and tab['update_every'] > 0:
                    if not tab.get('updated_at') or (datetime.now() - tab.get('updated_at')).total_seconds() >= tab.get('update_every'):
                        self.tableau.refresh()
                        tab['updated_at'] = datetime.now()

            if tab['type'] == 'Looker':
                self.looker.close_navigation_menu()
                if refresh and tab['update_every'] > 0:
                    if not tab.get('updated_at') or (datetime.now() - tab.get('updated_at')).total_seconds() >= tab.get('update_every'):
                            self.looker.refresh()
                            tab['updated_at'] = datetime.now()
                            time.sleep(5)
                
            time.sleep(tab.get('how_long_to_stay'))


class ToolHandler:

    def __init__(self, driver, username=None, password=None, login_url=None):
        self.username = username
        self.password = password
        self.login_url = login_url
        self.driver = driver

class Looker(ToolHandler):

    def __init__(self, driver, username=None, password=None, login_url=None):
        super().__init__(driver, username, password, login_url)
    
    def login(self, sleep=2):
        # Login on the Tableau instance.
        if self.username and self.password and self.login_url:
            self.driver.get(self.login_url)
            time.sleep(sleep)
            self.driver.find_element(By.XPATH,'//*[@id="identifierId"]').send_keys(self.username)
            self.driver.find_element(By.XPATH,'//*[@id="identifierId"]').send_keys(Keys.ENTER)
            time.sleep(sleep)
            self.driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(self.password)
            self.driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(Keys.ENTER)
            time.sleep(sleep)
        else:
            print('You need to add username, password and tableau_login_url to the constructor for that!')

    def refresh(self):
        self.driver.refresh()

    def close_navigation_menu(self):
        try:
            arrow = self.driver.find_element(By.XPATH, '//*[@id="body"]/div[2]/div/ng2-reporting-plate/plate/div/div/div/div[1]/div[1]/div[1]/report-navigation-drawer/div/div/button/mat-icon')
            if arrow.text == 'keyboard_arrow_left':
                self.driver.find_element(By.XPATH, '//*[@id="body"]/div[2]/div/ng2-reporting-plate/plate/div/div/div/div[1]/div[1]/div[1]/report-navigation-drawer/div/div/button').click()
            else: 
                print('Menu already closed')
        except Exception as e:
            pass

        
class Tableau(ToolHandler):

    def __init__(self, driver, username=None, password=None, login_url=None):
        super().__init__(driver, username, password, login_url)

    def login(self, sleep=2):
        # Login on the Tableau instance.
        if self.username and self.password and self.login_url:
            self.driver.get(self.login_url)
            time.sleep(sleep)
            self.driver.find_element(By.NAME,'email').send_keys(self.username)
            self.driver.find_element(By.NAME,'email').send_keys(Keys.ENTER)
            self.driver.find_element(By.NAME,'password').send_keys(self.password)
            self.driver.find_element(By.NAME,'password').send_keys(Keys.ENTER)
            time.sleep(sleep)
        else:
            print('You need to add username, password and tableau_login_url to the constructor for that!')
        
    def refresh(self):
        self.driver.find_element(By.XPATH, '//*[@id="refresh"]').click()

    def check_reconnect(self):
        try: 
            reconnect = self.driver.find_element(By.XPATH, '//*[@id="tab-shared-widget-1684759747140"]/div/div/div[2]/a')
            if reconnect.text:
                self.driver.find_element(By.XPATH, '//*[@id="tab-shared-widget-1684759747140"]/div/div/div[2]/a').click()
        except Exception as e:
            pass