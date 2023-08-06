# byhy performance testing lib: ByClient
# Author : byhy

import time,http.client,traceback,socket
from urllib.parse import urlparse,urlencode
from hyload.stats import Stats,bcolors
from hyload.util import getCurTime
from hyload.logger import TestLogger
import json as jsonlib
from http.cookies import SimpleCookie


CommonHeaders = {
    # 'User-Agent' : "hyload tester"
}

_sending_http_msg = ''

_ori_http_send = http.client.HTTPConnection.send
def _patch_httplib_funcs(encoding='utf8'):
    def new_send(self, data):
        global _sending_http_msg
        if hasattr(data, "read"):
            return
        _sending_http_msg += data.decode(encoding)
        # print(bcolors.OKGREEN + data.decode(encoding) + bcolors.ENDC, end='')
        return _ori_http_send(self, data)
    http.client.HTTPConnection.send = new_send


def _unpatch_httplib_funcs():
    http.client.HTTPConnection.send = _ori_http_send




class ErrReponse():
    def __init__(self,errortype):        
        self.errortype = errortype 


# HTTPResponse Wraper obj
# refer to  
# https://docs.python.org/3/library/http.client.html#httpresponse-objects
class HttpResponse():
    def __init__(self,
                 httpResponse:http.client.HTTPResponse,
                 rawBody,
                 responseTime,
                 url): # 响应时长毫秒为单位
        self.httpResponse = httpResponse
        self.raw = rawBody
        self.stringBody = None
        self.jsonObj = None
        self.responseTime = responseTime
        self.url = url

        # 为了兼容错误相应对象 ErrReponse
        # 方便返回判断
        self.errortype = None # 没有错误
        self.status_code = httpResponse.status
    
    def __getattr__(self, attr):
        return getattr(self.httpResponse, attr) 



    # return decoded string body 
    def string(self,encoding='utf8'):
        try:
            self.stringBody = self.raw.decode(encoding)
                
            return self.stringBody
        except:
            print(f'message body decode with {encoding} failed!!')
            return None

    def text(self,encoding='utf8'):
        return self.string(encoding)
    
    def json(self,encoding='utf8'):
        try:
            if self.jsonObj is None:
                self.jsonObj = jsonlib.loads(self.string(encoding))

            return self.jsonObj
        except Exception as e:
            print('消息体json解码失败!!')
            print(e)
            return None

    
    def getAllCookies(self):
        cookiesStr = self.httpResponse.getheader('Set-Cookie')
        if not cookiesStr:
            return {}
            
        cookieList = self.httpResponse.getheader('Set-Cookie').split(',')

        cookieDict = {}
        for c in cookieList:
            kv = c.split(';')[0].split('=')
            cookieDict[kv[0]] = kv[1]
        return cookieDict

    def getCookie(self,cookieName):
        cookieDict = self.getAllCookies()
        return cookieDict.get(cookieName)



# refer to https://docs.python.org/3/library/http.client.html#http.client.HTTPConnection
class HttpClient:
    
    def __init__(self,timeout=10, proxy=None): 
        """
        An HyHTTPConnection instance represents one transaction with an HTTP server.
        """        
        self.timeout     = timeout
        self.proxy       = proxy    # in form of 127.0.0.1:8888
        self._conn       = None     # default HTTPConnection or  HTTPSConnection
        self._conn_table = {}

        self._showAllRawMsg = False
        self._msgEncodeing = 'utf-8'
        self._httplibPathced = False

    def createConnection(self, protocol, host, port):
        
        if protocol == 'http':
            connection_class = http.client.HTTPConnection
        elif protocol == 'https':
            connection_class = http.client.HTTPSConnection
        else:
            raise Exception(f'unsupported protocol: {protocol}')
        
        # set default connection
        if self.proxy is None:
            self._conn = connection_class(host, port, timeout=self.timeout)
        else:
            self._conn = connection_class(self.proxy, timeout=self.timeout)
            self._conn.set_tunnel(host, port)
            
        self._conn.protocol = protocol
        self._conn.cookie = SimpleCookie()


        self._conn_table[(protocol, host, port)] = self._conn
        
        self.host, self.port = self._conn.host, self._conn.port

        try:
            self._conn.connect()
        except ConnectionRefusedError:
            errInfo = 'connection refused, maybe server not started'
            print('!!! ConnectionRefusedError\n' + errInfo)
            TestLogger.write(f'80|{errInfo}')
            
            raise

        Stats.connectionNumIncreace()


    def showRawMsg(self, isShow:bool=True, encoding='utf8'):
        """
        show or hide raw http messages

        Parameters
        ----------
        isShow : bool, optional
            True: show 
            False: not show
            
        encoding : string, optional
            Message Encoding, default is 'utf8'
            
        """
        self._showAllRawMsg = isShow
        self._msgEncodeing = encoding
        if isShow:
            _patch_httplib_funcs(encoding)
            self._httplibPathced = True
        else:
            _unpatch_httplib_funcs()
    

    @staticmethod
    def _urlAnalyze(url):
        protocol, host, port, path = None, None, None, None

        def handleUrlAfterHttpPrefix(url, urlPart, isSecure):
            if len(urlPart) == 0:
                raise Exception(f'url error:{url}')
            
            parts = urlPart.split('/',1)
            host = parts[0]
            path = '/' if len(parts)==1 else '/' + parts[1]

            if ':' not in host:
                port = 443 if isSecure else 80
            else:
                host, port = host.split(':')
                port = int(port)

            return host, port, path


        if url.startswith('http://'):
            protocol = 'http'
            host, port, path = handleUrlAfterHttpPrefix(url, url[7:], False)

        elif url.startswith('https://'):
            protocol = 'https'
            host, port, path = handleUrlAfterHttpPrefix(url, url[8:], True)

        else: # url only contain path
            path = url

        return protocol, host, port, path



    # send request, https://docs.python.org/3/library/http.client.html#http.client.HTTPConnection.request
    # return HyResponse which is a HTTPResponse Wraper obj
    # args are method, url, body=None, headers=None, 
    def send(self,
            method:str,
            url:str,
            params=None,
            data=None, 
            json=None,
            encoding='utf8',
            headers=None, 
            duration=None,
            showRawMsg=False):
        
        global _sending_http_msg

        if showRawMsg:
            if not self._httplibPathced:
                _patch_httplib_funcs(encoding)
                self._httplibPathced = True

        
        protocol, host, port, path = self._urlAnalyze(url)

        if not self._conn_table:  # no existing connections
            if protocol is None:
                raise Exception(f'url error:{url}, should have "http" or "https" as prefix')
            
            self.createConnection(protocol, host, port)
            # print('no existing connections, create new connection')

        else:                     # there are existing connections

            if protocol is not None:
                # print('protocol/host/port specified')
                self._conn = self._conn_table.get((protocol, host, port))
                if not self._conn:
                    # print('protocol/host/port not used before, create new connection')
                    self.createConnection(protocol, host, port)
                else:
                    # print('protocol/host/port used before , use old connection')
                    pass

            else:
                # print('protocol/host/port not specified, use default connection self._conn')
                pass   
             
            
        beforeSendTime = getCurTime()

        
        if headers is None: 
            headers = {}
        for k,v in CommonHeaders.items():
            if k not in headers:
                headers[k] = v

        # add cookies
        if len(self._conn.cookie) > 0:
            headers.update({'Cookie':self._conn.cookie.output(header="",attrs=[],sep=';')})

        # url params handle
        if params is not None:
            queryStr = urlencode(params)
            if '?' in path:
                path += '&' + queryStr
            else:
                path += '?' + queryStr



        body = None
        # msg body is in format of JSON
        if json is not None:
            headers['Content-Type'] = 'application/json'
            body = jsonlib.dumps(json,ensure_ascii=False).encode(encoding)

        
        # msg body is in format of urlencoded
        elif data is not None:
            if type(data) == dict:
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                body = urlencode(data).encode(encoding)
            # str类型，编码后放入消息体
            elif type(data) == str:
                body = data.encode(encoding)
            # bytes类型，直接放入消息体
            elif type(data) == bytes:
                body = data

        try:
            self._conn.request(method, path, body, headers)
            if self._showAllRawMsg or showRawMsg:
                print('\n---------------------------')       
                print(bcolors.OKGREEN + _sending_http_msg + bcolors.ENDC, end='')
                _sending_http_msg = ''
                print('\n---------------------------')    

        except ConnectionRefusedError:
            errInfo = 'connection refused, maybe server not started'
            print('!!! ConnectionRefusedError\n' + errInfo)
            TestLogger.write(f'80|{errInfo}')
            
            self._conn.close()
            
            raise
        
        except socket.timeout as e:
            print('!!! socket timeout', e)
            Stats.oneTimeout()

            self._conn.close()
            Stats.connectionNumDecreace()
            # self.createConnection(*self.args, **self.kargs)

            TestLogger.write(f'100|time out|{url}')

            return ErrReponse(100)
        
        except ConnectionAbortedError as e:
            print('!!! Connection Aborted during sending',e)
            Stats.oneError()

            self._conn.close()
            Stats.connectionNumDecreace()
            # self.createConnection(*self.args, **self.kargs)
            
            TestLogger.write(f'101|Connection Aborted during sending|{url}')

            return ErrReponse(101)

        afterSendTime = Stats.oneSent()


        # recv response
        try:
            httpResponse = self._conn.getresponse()
            
            if self._showAllRawMsg or showRawMsg:
                print(bcolors.OKBLUE + f"HTTP/{'1.1' if httpResponse.version==11 else '1.0'} {httpResponse.status} {httpResponse.reason}" + bcolors.ENDC)
                print(bcolors.OKBLUE + httpResponse.msg.as_string() + bcolors.ENDC,end='')
        except socket.timeout as e:
            print('!!! response timeout')

            Stats.oneTimeout()

            self._conn.close()
            Stats.connectionNumDecreace()

            # self.createConnection(*self.args, **self.kargs)
            
            TestLogger.write(f'110|response time out|{url}')
            return ErrReponse(110)
            
        except ConnectionAbortedError as e:
            print('!!! Connection Aborted during receiving response',e)
            Stats.oneError()

            self._conn.close()
            Stats.connectionNumDecreace()
            # self.createConnection(*self.args, **self.kargs)
            
            TestLogger.write(f'120|Connection Aborted during receiving response|{url}')
            return ErrReponse(120)

        except http.client.RemoteDisconnected as e:
            # 这种情况很可能是 http连接闲置时间过长，服务端断开了连接，尝试重发            
            self._conn.close()
            Stats.connectionNumDecreace()

            # self.createConnection(*self.args, **self.kargs)

            try:
                self._conn.request(method, path, body, headers)
                afterSendTime = Stats.oneSent()
                httpResponse = self._conn.getresponse()

                info = f'* after sending, server closed connection, reconnect and resending succeed|{url}'
                print(info)
                TestLogger.write(info)
            except:
                Stats.oneError()
                self._conn.close()
                Stats.connectionNumDecreace()
                # self.createConnection(*self.args, **self.kargs)
                            
                err = f'130|after sending, server closed connection, reconnect and resending failed|{url}'
                print(err)
                TestLogger.write(err)
                return ErrReponse(130)
                

        # 下面是 可以正常接收响应 情况下 的代码

        recvTime = Stats.oneRecv(afterSendTime)

        # check cookie
        cookieHdrs = httpResponse.getheader('set-cookie')
        if cookieHdrs:
            # print (cookieHdrs)
            self._conn.cookie.load(cookieHdrs)

        # 如果 有 duration，需要接收完消息后sleep一点时间，确保整体时间为duration
        if duration:
            
            # print(f'send {beforeSendTime} -- recv {recvTime}')
            extraWait = duration-(recvTime-beforeSendTime)
            if extraWait >0:  # 因为小于1ms的sleep通常就是不准确的
                # print(f'sleep {extraWait}')
                time.sleep(extraWait)

        
        rawBody = httpResponse.read()
        
        if self._showAllRawMsg or showRawMsg:
            outputStr = rawBody.decode(self._msgEncodeing)
            if len(outputStr) > 2048:
                outputStr = outputStr[:2000] + '\n.................'
            print(bcolors.OKBLUE + outputStr+ bcolors.ENDC)
            print('\n')


        self.response = HttpResponse(httpResponse,
                                   rawBody,
                                   int((recvTime-afterSendTime)*1000),
                                   path)
        
     
            
            
        return self.response
    

    def  get(self,*args,**kargs):
        return self.send('GET',*args,**kargs)
        
    def  post(self,*args,**kargs):
        return self.send('POST',*args,**kargs)
        
    def  put(self,*args,**kargs):
        return self.send('PUT',*args,**kargs)
        
    def  delete(self,*args,**kargs):
        return self.send('DELETE',*args,**kargs)
        
    def  patch(self,*args,**kargs):
        return self.send('PATCH',*args,**kargs)

    def  head(self,*args,**kargs):
        return self.send('HEAD',*args,**kargs)


