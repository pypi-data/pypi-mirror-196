from selenium.webdriver.common.by import By


class browser_utility:
    def go(self, url):
        """页面跳转
        chrome.to('http://baidu.com')"""
        self.instance.get(url)

    def set_cookies(self, cookies):
        """设置session cookie, 登录验证
        chrome.to('http://www.bilibili.com')
        cookies = [
            'SESSDATA=a959f392%2C1599117854%2C49e4c*31; Domain=.bilibili.com; Expires=Thu, 03-Sep-2020 07:07:34 GMT;',
            'DedeUserID=31890217; Domain=.bilibili.com; Expires=Thu, 03-Sep-2020 07:07:34 GMT;', 
            'DedeUserID__ckMd5=04e309be22e2c59e; Domain=.bilibili.com; Expires=Thu, 03-Sep-2020 07:07:34 GMT;',
            'bili_jct=d227001282644a628f6b5cbc282085b2; Domain=.bilibili.com; Expires=Thu, 03-Sep-2020 07:07:34 GMT;'
        ]"""
        for cookie in cookies:
            self.instance.eval('document.cookie="%s"'%cookie)
    
    @property
    def url(self):
        """返回当前地址
        print(chrome.url)"""
        return self.instance.current_url
    
    def click(self,selector):
        """点击页面元素
        chrome.to('http://baidu.com')
        chrome.click('.s-top-left .mnav:nth-of-type(1)')
        """
        self.find(selector).click()
    
    def exit(self):
        """关闭浏览器
        chrome.exit()"""
        self.instance.quit()
    
    def eval(self,js_code_str):
        """执行js代码
        chrome.eval('console.log("hello")')
        """
        self.instance.execute_script(js_code_str)
    
    @property
    def html(self):
        """返回网页html
        print(chrome.html）
        """
        return self.instance.page_source
    
    def find(self,selector,root=None):
        """查找节点元素
        browser.find('div.coin.view-stat .icon-text',item).text
        """
        root = root if root else self.instance
        return root.find_element(By.CSS_SELECTOR, selector)
    
    def find_all(self,selector,root=None):
        """查找所有节点元素
        browser.find_all('div.article-card')
        """
        root = root if root else self.instance
        return root.find_elements(By.CSS_SELECTOR, selector)
    
    def new_tab(self,url):
        """新标签页打开
        chrome.new_tab('http://sohu.com')"""
        self.instance.execute_script("""window.open('"""+ url+ """','_blank');""")
    
    def screenshot(self):
        """网页截图
        chrome.screenshot()"""
        self.instance.save_screenshot('%s.png' % t.timestamp())


