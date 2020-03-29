import cherrypy                 # webserver framework
import tldextract
import json  
from cherrypy import _cperror
import os
import page_content             #screenshot library
import time
import hashlib      
from tokens import get_tokens   #list of valid tokens
from PIL import Image           #screenshot image file
import base64                   # encode the output result


# debug_level (False->production,True->development)
debug_level = False

def error_page_default(status, message, traceback, version):
    print("**********************")
    print(cherrypy.request.headers)
    print('**********************')
   # return "maintenance,{}".format(status)
    try:
        dbg_info = ''
        global debug_level
        if (debug_level):
            dbg_info = "{},{},{},{}".format(status,message,traceback.replace("\n","<br />"),version)
            return "<html><body>FORBIDDEN AREA - NOT FOUND<br />{}</body></html>".format(dbg_info)
        else:
            if status.startswith('404'):
                return not_found_html()
            #end if
            return "VIVA :-)"
        #end if
    except:
        return "<html><body>FORBIDDEN AREA / NOT FOUND AREA</body></html>"
    #end try
#end def

def get_client_ip(headers):
    result = dict()
    result['remote_ip'] = None
    result['cf_user_ip'] = None
    result['client_ip'] = None
    result['visit_via_cf'] = False
    if headers == None or isinstance(headers,dict) == False:
        return result;
    #end if
    if headers.get('Remote-Addr',None) == None:
        return result
    #end if
    remote_ip = headers.get('Remote-Addr');
    result['remote_ip'] = remote_ip
    result['client_ip'] = remote_ip
    if headers.get("CF-Connecting-IP",None) != None:
        cf_user_ip = headers.get("CF-Connecting-IP")
        result['cf_user_ip'] = cf_user_ip
        result['client_ip'] = cf_user_ip
    #end if
    return result
#end def



def not_found_html():
    return open('custom_page/404.html').read()
# end def


def suspend_page():
    return open("custom_page/500.html").read()
#end def


class Screenshots(object):
    @cherrypy.expose
    def index(self,cat = None,username = None,password = None,submit = None,*args, **kwargs):
        print("**********************")
        print(cherrypy.request.headers)
        print('**********************')
        ips = get_client_ip(cherrypy.request.headers)
        #cherrypy.response.status = 404
        #return cherrypy.request.headers["Remote-Addr"]
        return open('index.html')
    #end if

    @cherrypy.expose
    def api(self,url=None,token=None,user_agent = None, *args, **kwargs):

        print("**********************")
        print(cherrypy.request.headers)
        print('**********************')
        # check if token is valid
        if not self.check_token_param(token):
            return json.dumps({
                        'success':False,
                        'code':403,
                        'msg':'Not authorized',
                        'attr':None}).encode('utf-8')
        # check validity of User-Agent
        user_agent = self.sanitize_user_agent(user_agent)
        # check validity of the URL
        if not self.sanitize_url(url):
            return json.dumps({
                        'success':False,
                        'code':502,
                        'msg':'Wrong URL format (must start with http:// or https:// and no IP address',
                        'attr':None}).encode('utf-8')
        # everything's fine...let's get screenshot
        return self.fetch_screenshot(url,user_agent).encode('utf-8')
    #end def

    def sanitize_url(self,url):
        """
            Check if URL:
            1. is string and -ne ''
            2. starts with 'http' or 'https'
            3. is not 'localhost' or '127.0.0.1'
            4. len(url) < 1000
        """
        result =  [False]
        if not isinstance(url,str) or url.strip() == '' or url == None:result.append(True)
        if not url.startswith("http://") and not url.startswith("https://"):result.append(True)
        if len(url)>1000:result.append(True)
        tldparser = tldextract.extract(url)
        if tldparser.domain == '127.0.0.1':result.append(True)
        if tldparser.domain == 'localhost':result.append(True)
        if tldparser.suffix == '':result.append(True) # we do not scan IP addresses
        if any(result):return False
        return True
    #end def
            
    def fetch_screenshot(self,url,user_agent):
        try:
            bmp = page_content.BMP()
            prx = bmp.create_proxy()
            if prx != None:
                bmp.create_har(prx.get("port"))
            pc = page_content.page_content(user_agent)
            result = pc.selenium_get(url,return_content=False,return_handle=True,headless=True,return_title=False,proxy = prx)
            if result != None and isinstance(result,dict) and result.get("handle",None)!=None:
                handle = result.get('handle')
                #wait 6 seconds before taking screenshots
                #time.sleep(6)
                f_name = hashlib.md5(str(time.time()).encode()).hexdigest()
                result = handle.save_screenshot(f_name + '.png')
                html = handle.page_source
                title = handle.title
                har = bmp.get_har(prx.get("port")) if isinstance(prx,dict) else dict()
                if prx != None:
                    bmp.close_proxy(prx.get("port"))
                destination = handle.current_url
                if result != False:
                    im = Image.open(f_name + '.png')
                    bg = Image.new("RGB", im.size, (255,255,255))
                    bg.paste(im,im)
                    bg.save(f_name + '.jpg')
                    try:
                        os.remove(f_name + '.png')
                        f = open(f_name + '.jpg','rb')
                        data = f.read()
                        f.close()
                        os.remove(f_name + '.jpg')
                        data = base64.encodebytes(data).decode()
                        handle.quit()
                        return json.dumps({'success':True,'code':200,'msg':'success','attr':{
                                                                    "shot":{'success':True,'data':data},
                                                                    'title':title,
                                                                    'html':html,
                                                                    'har':har,
                                                                    'destination':destination}})
                    except Exception as e:
                        print(e)
                        handle.quit()
                        return json.dumps({'success':True,'code':200,'msg':'success','attr':{
                                                                    'shot':{'success':False,'data':None},
                                                                    'title':title,
                                                                    'html':html,
                                                                    'har':har,
                                                                    'destination':destination}})
                    #end
                else:
                    handle.quit()
                    return json.dumps({'success':True,'code':200,'msg':'success','attr':{
                                                                    'shot':{'success':False,'data':None},
                                                                    'title':title,
                                                                    'html':html,
                                                                    'har':har,
                                                                    'destination':destination}})
            else:
                return json.dumps({'success':False,'code':503,'msg':'Unknown error1','attr':None})
        except Exception as e:
            print(e)
            return json.dumps({'success':False,'code':503,'msg':'Unknown error','attr':None})
        #end except
    #end def


    def sanitize_user_agent(self,user_agent):
        """
            Checks if user-agent:
            1. is instance of string
            2. len(useragent) < 150
        """
        if user_agent == None:return ''
        if isinstance(user_agent,str):
            if len(user_agent) > 150:
                return user_agent[:150]
            else:
                return user_agent
            #end if
        else:
            return ''
    #end def
    
    def check_token_param(self,token):
        """
            Checks if token:
            1. is istring (and not None)
            2. is not empty
            3. len(token) == 64
            4. exists in authorized token list
        """
        if not isinstance(token,str) or token == '' or len(token) != 64 :return False
        tokens = get_tokens()
        if not isinstance(tokens,list):return False
        if token not in tokens:return False
        return True
    #end def
#end class


if __name__ == '__main__':
    # Run the server with the following configuration
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8086,
                            'error_page.default': error_page_default
    })
    conf = {
        '/': {
            'tools.encode.on': True,
            'tools.encode.encoding': 'utf-8',
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [
                ('Server', 'nginx'),
                ('X-XSS-Protection','1; mode=block')
            ],
            'tools.sessions.on': True,
            'tools.sessions.name' : "PHPSESSID",
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/api':{
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type','application/json')]
        },
        '/assets': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath(os.getcwd()) + '/assets',
            'tools.staticfile.root' : os.path.abspath(os.getcwd()) + "/assets"
        }
    }
    cherrypy.quickstart(Screenshots(),'',conf)
