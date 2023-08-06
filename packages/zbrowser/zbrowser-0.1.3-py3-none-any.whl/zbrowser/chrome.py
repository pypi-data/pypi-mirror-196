
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from zbrowser.utility import browser_utility
import platform


PROXY = "socks5://127.0.0.1:1080"


class Chrome(browser_utility):
    def __init__(self, headless = False, proxy = False, javascript= True):
        self.headless = headless
        self.proxy = proxy
        self.javascript = javascript
        self.start()
    
    def make_chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox") # DevTools相关,防启动崩溃
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36")
        chrome_options.add_argument("--disable-gpu") 
        chrome_options.add_argument('--window-size=2560,1600')
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
                'javascript': 1 if self.javascript else 2,
            }
        }
        chrome_options.add_experimental_option("prefs", prefs)
        if(self.headless):
            chrome_options.add_argument('--headless')
        if(self.proxy):
            chrome_options.add_argument('--proxy-server=%s' % PROXY)
        return chrome_options
    
    def start(self):
        chrome_options = self.make_chrome_options()
        chrome = webdriver.Chrome(options=chrome_options)
        stealth(chrome,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        self.instance = chrome

    def stop(self):
        self.instance.exit()
