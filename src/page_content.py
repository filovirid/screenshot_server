from selenium import webdriver                          # selenium webdriver for firefox
from selenium.webdriver.chrome.options import Options   # just for extra options like headless browser
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities # for performance log
import tldextract                                       #extract different parts of URLs
import time                                             # use time.sleep
import json                                             # parse json
import logging                                          # to log exceptions
import selenium
import requests



class page_content():
    """
    This class uses selenium browser with Chrome webdriver to surf the pages.
    This is tuned for phishing and dangerous pages since we have disabled all the warning for
    phishing attacks, malware attacks and untrusted CAs.
    So don't use it for other tasks.
    """

    def __init__(self,user_agent = ''):
        # set the default User-Agent
        if user_agent == '':
            self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
        else:
            self.user_agent = user_agent
    # end def
    
    def selenium_get(self,url,
                return_handle = False, 
                return_content =  True,
                headless = False,
                return_title = False,
                screenshot = "",
                proxy = None,
                return_har = False):
        """
        Get a URL using selenium library. Probably you need to wait a
        few second for any possible redirection or load of data.
        
        Params:
            url: required. the URL in the browser's address bar
            return_handle: returns the selenium browser handle (default: False).
                after using the handle you have to call handle.quit() to quit the browser.
            return_content: returns the content of the page in browser (default True).
            return_title: returns the title of the browser (default False)
            headless: If you want to run the browser in the background,
                set this parameter to True (default False).
            screenshot: it could be a filename or path/filename to save the
                screenshot (default no screenshot).
        Usage:
            data = selenium_get('http://google.com',headless=True,return_title=True,return_handle=True)
            data.keys()
            print(data.get('title'))
            print(data.get('content'))
            print(data.get('handle').title)
        """
        browser = None
        try:
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-client-side-phishing-detection")
            options.add_argument("--disable-component-update")
            options.add_argument("--disable-default-apps")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars");
            options.add_argument("--disable-gpu");
            options.add_argument("--disable-print-preview")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--user-agent={}".format(self.user_agent))
            caps = None
            if return_har:
                caps = DesiredCapabilities.CHROME
                caps['goog:loggingPrefs'] = {'performance': 'ALL'}
            if isinstance(proxy,str):
                proxy_ip = proxy.split(":")[0].strip()
                proxy_port = proxy.split(":")[1].strip()
                options.add_argument("--proxy-server={}:{}".format(proxy_ip,proxy_port))
            if  (not url.startswith("http://")) and (not url.startswith("https://")):
                url = "http://" + url
            result = dict()
            if (headless):
                options.add_argument("--headless")
            if return_har:
                browser = webdriver.Chrome('chromedriver',chrome_options=options,desired_capabilities=caps)
            else:
                browser = webdriver.Chrome('chromedriver',chrome_options=options)
            browser.delete_all_cookies() # delete all cookies everytime
            browser.set_window_size(1080,720) # set the screen size
            browser.set_page_load_timeout(60)  # maximum load time to 60 secs
            browser.get(url)
            time.sleep(10) # sleep for 10 seconds for AJAX shit.
            if return_content:
                result['content'] = browser.execute_script("return document.documentElement.innerHTML")
            if return_handle:
                result['handle'] = browser
            if return_title:
                result['title'] = browser.title #don't forget to quit the handle after you are done with it!!!
            if screenshot != '':
                browser.save_screenshot(screenshot)
            if not return_handle:
                browser.quit()
            return result
            # TODO: don't forget to handle alert attack
            # This is the way to handle it
            #try:
            #    h.switch_to.alert.accept()
            #except Exception as e:
            #    pass
        except selenium.common.exceptions.TimeoutException as e:
            logging.critical("ERROR:SELENIUM:TIMEOUT FOR {}".format(url))
            #print(e)
            if browser:
                browser.quit()
            return None
        except Exception as e:
            logging.critical("ERROR:SELENIUM:" + time.strftime("%Y-%m-%d %H:%M:%S") + "," + str(e))
            if browser:
                browser.quit()
            return None
    # end def

    def catch_content(self,url):
        pass
    # end def

# We are not using browser-mob shit since it's deprecated and memory-hungry
class BMP():
    """
        Wrapper class for Browsermob-proxy API.
        Read BMP documentation for mor info.
        https://github.com/lightbody/browsermob-proxy#rest-api
    """
    def __init__(self,addr='localhost',port = 8046):
        self.addr = addr
        self.port = port
        self.url = 'http://{}:{}'.format(self.addr,self.port)
    def create_proxy(self):
        try:
            r = requests.post(self.url + '/proxy',timeout = 10)
            r = json.loads(r.text)
            if r.get('port',None) != None:
                print(r)
                return {'port':r.get("port"),'address':self.addr}
            return None
        except:
            return None

    def create_har(self,port):
        try:
            r = requests.put(self.url + '/proxy/{}/har'.format(port),timeout = 10)
            return True
        except:
            return False
    def get_har(self,port):
        try:
            r = requests.get(self.url + '/proxy/{}/har'.format(port),timeout = 10)
            return r.text
        except:
            return None

    def close_proxy(self,port):
        try:
            r = requests.delete(self.url + '/proxy/{}'.format(port),timeout = 10)
            return True
        except:
            return False



if __name__=="__main__":
    # run some test to check the browser
    inst1 = page_content()
    brws = inst1.selenium_get('http://google.com',headless = False, return_handle = True,return_content = False)
    print(brws.keys())
