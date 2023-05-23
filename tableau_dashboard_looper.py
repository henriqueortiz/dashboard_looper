from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import itertools
import time
from datetime import datetime

class TableauDashboardLooper():
    '''
    A class that iteratively displays dashbords using Chrome in kiosk mode.

    ---
    Attributes
    ---
    username: str
        A active Username of Tableau instance. *Must not have active MFA.
    password: str
        Password of give user for login to Tableau instance.
    tableau_login_url: str
        The login url of your Tableau instance.
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

    def __init__(self, driver, username=None, password=None, tableau_login_url=None, dashboards=dict):
        self.username = username
        self.password = password
        self.tableau_login_url = tableau_login_url
        self.dashboards = dashboards.get('dashboards')
        self.open_tabs = {}
        self.driver = driver
    
    # def start_browser(self, sleep=10, kiosk=True):
    #     # Open Chrome webdrive and navigates to the login of your Tableau instance.
    #     self.chrome_options = Options()
    #     if kiosk:
    #         self.chrome_options.add_argument("--kiosk")
    #     self.chrome_options.add_argument('start-maximized')
    #     self.chrome_options.add_argument('disable-infobars')
    #     self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    #     self.driver = webdriver.Chrome(options=self.chrome_options)
    #     time.sleep(sleep)

    def login_tableau(self, sleep=10):
        # Login on the Tableau instance.
        if self.username and self.password and self.tableau_login_url:
            self.driver.get(self.tableau_login_url)
            time.sleep(sleep)
            self.driver.find_element(By.NAME,'email').send_keys(self.username)
            self.driver.find_element(By.NAME,'email').send_keys(Keys.ENTER)
            self.driver.find_element(By.NAME,'password').send_keys(self.password)
            self.driver.find_element(By.NAME,'password').send_keys(Keys.ENTER)
            time.sleep(sleep)
        else:
            print('You need to add username, password and tableau_login_url to the constructor for that!')

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
        time.sleep(10)
        self.set_open_tabs()

    def set_open_tabs(self):
        # Assign values ​​to the attribute with configuration data
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            for dashboard in self.dashboards:
                if self.driver.current_url == dashboard.get('url'):
                    self.open_tabs[handle] = dashboard
    
    def start_mirroring(self, tv_name):
        # Start mirroring your Chorme tab to the device informed. *The device must have chromecast or similar technology
        try:
            while True:
                if self.driver.get_sinks():
                    print(self.driver.get_sinks())
                    self.driver.start_desktop_mirroring(sink_name=tv_name)
                    break
        except:
            print("The TV is not ready yet or is not available.")

    def loop_through_tabs(self, refresh=True):
        # Loops through Chrome tabs applying refresh and wait rules.
        for handle in itertools.cycle(self.open_tabs):
            print(handle)
            self.driver.switch_to.window(handle)
            tab = self.open_tabs[handle]
            if refresh:
                if not tab.get('updated_at'):
                    self.driver.find_element(By.XPATH, '//*[@id="refresh"]').click()
                    tab['updated_at'] = datetime.now()
                else:
                    if tab.get('update_every') and tab.get('update_every') != 0  and (datetime.now() - tab.get('updated_at')).total_seconds() >= tab.get('update_every'):
                        self.driver.find_element(By.XPATH, '//*[@id="refresh"]').click()
                        tab['updated_at'] = datetime.now()
            
            print(handle)
            time.sleep(tab.get('how_long_to_stay'))