# byhy performance testing lib: ByClient
# Author : byhy

import time, http.client, socket, gzip
from urllib.parse import urlencode
from hyload.stats import Stats,bcolors
from hyload.util import getCurTime
from hyload.logger import TestLogger
import json as jsonlib
from http.cookies import SimpleCookie
from typing import Union, Dict

_common_headers = {
    # 'User-Agent' : "hyload tester"
}



# begin ** for patch http built-in funcs

_http_req_msg_buf_cpy = b''

_ori_http_send = http.client.HTTPConnection.send

def _patch_httplib_funcs():
    def new_send(self, data):
        global _http_req_msg_buf_cpy
        if hasattr(data, "read"):
            return
        _http_req_msg_buf_cpy += data        
        return _ori_http_send(self, data)
    http.client.HTTPConnection.send = new_send


def _unpatch_httplib_funcs():
    http.client.HTTPConnection.send = _ori_http_send


# end  ** for patch http built-in funcs



class ErrReponse():
    def __init__(self,errortype):        
        self.errortype = errortype 


# HTTPResponse Wrapper obj
# refer to https://docs.python.org/3/library/http.client.html#httpresponse-objects
class HttpResponse():
    def __init__(self,
                 http_response:http.client.HTTPResponse,
                 raw_body,
                 response_time,
                 url): # 响应时长毫秒为单位
        self._http_response = http_response
        self.raw = raw_body
        self._string_body = None
        self._json_obj = None
        self.response_time = response_time
        self.url = url

        # 为了兼容错误相应对象 ErrReponse
        # 方便返回判断
        self.errortype = None # 没有错误
        self.status_code = http_response.status
    
    def __getattr__(self, attr):
        return getattr(self._http_response, attr) 



    # return decoded string body 
    def string(self,encoding='utf8'):
        try:
            self._string_body = self.raw.decode(encoding)
                
            return self._string_body
        except:
            print(f'message body decode with {encoding} failed!!')
            return None

    def text(self,encoding='utf8'):
        return self.string(encoding)
    
    def json(self,encoding:str='utf8'): 
        """Parse response body as json

        Parameters
        ----------
        encoding : str, optional
            _description_, by default 'utf8'

        Returns
        -------
        Any
            Return Python object if parsing successfully, Or raise Exception if parsing failed.
        """
        if self._json_obj is None:
            self._json_obj = jsonlib.loads(self.string(encoding))

        return self._json_obj
       

    
    def get_all_cookies(self):
        cookiesStr = self._http_response.getheader('Set-Cookie')
        if not cookiesStr:
            return {}
            
        cookieList = self._http_response.getheader('Set-Cookie').split(',')

        cookieDict = {}
        for c in cookieList:
            kv = c.split(';')[0].split('=')
            cookieDict[kv[0]] = kv[1]
        return cookieDict

    def get_cookie(self,cookieName):
        cookieDict = self.get_all_cookies()
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

        self._httplibPathced = False

    def create_connection(self, protocol, host, port):
        
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

        Stats.connection_num_increace()

    @staticmethod
    def _print_msg(msg :bytes, encoding: str, color=bcolors.OKGREEN, limit=4096):
        toolong = False
        if len(msg) > limit:
            msg = msg[:limit]
            toolong = True

        if encoding == 'hex':
            ostr = msg.hex('\n',-32).upper()           
        else:
            if encoding is None: encoding = 'utf8'
            ostr = msg.decode(encoding, errors="replace")
        
        if toolong:
            ostr += '\n.................'

        print(color + ostr + bcolors.ENDC, end='')

    

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
            params:Union[None,Dict[str,str]]=None,
            headers:Union[None,Dict[str,str]]=None, 
            data:Union[None,Dict[str,str],str,bytes]=None, 
            json=None,
            debug:bool=False,
            debug_body_print_max_len:int=4096,
            request_body_encoding:Union[None,str]=None,
            response_body_encoding:Union[None,str]=None,            
            # duration:int=None,
        ):
        """send HTTP request to server and receive response from server.

        Parameters
        ----------
        method : str
            HTTP method name, like 'GET', 'POST','PUT', 'DELETE','PATCH' ... 
        url : str
            HTTP URL for the HTTP request. 
            The first call must specify protocol/host/port prefix, like 'http://www.abc.com/a/b/c'.
            The following call could omit that, implying to use previous used protocol/host/port
        params : 
            (optional) Dictionary to send in the query string for the HTTP requests.
        headers : 
            (optional) Dictionary of HTTP Headers to send with the HTTP requests.
        data : 
            (optional) Dictionary, bytes, strings to send in the body of the HTTP requests.
        json : 
            (optional) A JSON serializable Python object to send in the body of the HTTP requests.    
        debug : bool, optional
            (optional) Whether print whole HTTP request and response, by default False.
            False : not print
            True  : print        
        debug_body_print_max_len : int , optional        
            (optional) If debug set to True, at most how many chars of HTTP body will be printed. 
            By default 4096.
            If body length is larger, the remaining will be replaced with "....."
        request_body_encoding : str, optional
            (optional) HTTP request body bytes encoding, all Python char-encoding are supported. 
            if not specified, hyload will use 'utf8' as text-encoding. 
        response_body_encoding : str, optional
            (optional) HTTP response body bytes encoding used for debug print, all Python char-encoding are supported. 
            if not specified, hyload will try to guess it from `Content-Type`.
            if no clue in `Content-Type`, it will use 'utf8' as text-encoding.   
            if set to 'hex', print bytes in hex string format.

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        Exception
            _description_
        """
        
        global _http_req_msg_buf_cpy

        if debug:
            if not self._httplibPathced:
                _patch_httplib_funcs()
                self._httplibPathced = True

        
        protocol, host, port, path = self._urlAnalyze(url)

        if not self._conn_table:  # no existing connections
            if protocol is None:
                raise Exception(f'url error:{url}, should have "http" or "https" as prefix')
            
            self.create_connection(protocol, host, port)
            # print('no existing connections, create new connection')

        else:                     # there are existing connections

            if protocol is not None:
                # print('protocol/host/port specified')
                self._conn = self._conn_table.get((protocol, host, port))
                if not self._conn:
                    # print('protocol/host/port not used before, create new connection')
                    self.create_connection(protocol, host, port)
                else:
                    # print('protocol/host/port used before , use old connection')
                    pass

            else:
                # print('protocol/host/port not specified, use default connection self._conn')
                pass   
             
            
        beforeSendTime = getCurTime()

        # headers 
        if headers is None: 
            headers = {}
        for k,v in _common_headers.items():
            if k not in headers:
                headers[k] = v

        # cookies
        if len(self._conn.cookie) > 0:
            headers.update({'Cookie':self._conn.cookie.output(header="",attrs=[],sep=';')})

        # url params
        if params is not None:
            queryStr = urlencode(params)
            if '?' in path:
                path += '&' + queryStr
            else:
                path += '?' + queryStr


        # body        
        body = None
        # msg body is in format of JSON
        if json is not None:
            if (request_body_encoding is None): request_body_encoding='utf-8'
            headers['Content-Type'] = 'application/json; charset=' + request_body_encoding
            body = jsonlib.dumps(json,ensure_ascii=False).encode(request_body_encoding)

        
        # msg body is in format of urlencoded
        elif data is not None:                        
            if type(data) == dict:
                if (request_body_encoding is None): request_body_encoding='utf-8'
                headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=' + request_body_encoding
                body = urlencode(data).encode(request_body_encoding)
            # str类型，编码后放入消息体
            elif type(data) == str:
                if (request_body_encoding is None): request_body_encoding='utf-8'
                body = data.encode(request_body_encoding)
            # bytes类型，直接放入消息体
            elif type(data) == bytes:
                body = data

        try:
            self._conn.request(method, path, body, headers)
            if debug:
                print('\n---------------------------')   
                self._print_msg(
                    _http_req_msg_buf_cpy, 
                    request_body_encoding, 
                    bcolors.OKGREEN, 
                    debug_body_print_max_len)  
                _http_req_msg_buf_cpy = b''
                print('\n---------------------------')    

        except ConnectionRefusedError:
            errInfo = 'connection refused, maybe server not started'
            print('!!! ConnectionRefusedError\n' + errInfo)
            TestLogger.write(f'80|{errInfo}')
            
            self._conn.close()
            
            raise
        
        except socket.timeout as e:
            print('!!! socket timeout', e)
            Stats.one_timeout()

            self._conn.close()
            Stats.connection_num_decreace()
            # self.create_connection(*self.args, **self.kargs)

            TestLogger.write(f'100|time out|{url}')

            return ErrReponse(100)
        
        except ConnectionAbortedError as e:
            print('!!! Connection Aborted during sending',e)
            Stats.one_error()

            self._conn.close()
            Stats.connection_num_decreace()
            # self.create_connection(*self.args, **self.kargs)
            
            TestLogger.write(f'101|Connection Aborted during sending|{url}')

            return ErrReponse(101)

        afterSendTime = Stats.one_sent()


        # recv response
        try:
            # getresponse() of http.client.Connection only get reponse status line and headers.
            http_response = self._conn.getresponse()
            
            if debug:
                print(bcolors.OKBLUE + f"HTTP/{'1.1' if http_response.version==11 else '1.0'} {http_response.status} {http_response.reason}" + bcolors.ENDC)
                print(bcolors.OKBLUE + http_response.msg.as_string() + bcolors.ENDC,end='')
        except socket.timeout as e:
            print('!!! response timeout')

            Stats.one_timeout()

            self._conn.close()
            Stats.connection_num_decreace()

            # self.create_connection(*self.args, **self.kargs)
            
            TestLogger.write(f'110|response time out|{url}')
            return ErrReponse(110)
            
        except ConnectionAbortedError as e:
            print('!!! Connection Aborted during receiving response',e)
            Stats.one_error()

            self._conn.close()
            Stats.connection_num_decreace()
            # self.create_connection(*self.args, **self.kargs)
            
            TestLogger.write(f'120|Connection Aborted during receiving response|{url}')
            return ErrReponse(120)

        except http.client.RemoteDisconnected as e:
            # 这种情况很可能是 http连接闲置时间过长，服务端断开了连接，尝试重发            
            self._conn.close()
            Stats.connection_num_decreace()

            # self.create_connection(*self.args, **self.kargs)

            try:
                self._conn.request(method, path, body, headers)
                afterSendTime = Stats.one_sent()
                http_response = self._conn.getresponse()

                info = f'* after sending, server closed connection, reconnect and resending succeed|{url}'
                print(info)
                TestLogger.write(info)
            except:
                Stats.one_error()
                self._conn.close()
                Stats.connection_num_decreace()
                # self.create_connection(*self.args, **self.kargs)
                            
                err = f'130|after sending, server closed connection, reconnect and resending failed|{url}'
                print(err)
                TestLogger.write(err)
                return ErrReponse(130)
                

        # 下面是 可以正常接收响应 情况下 的代码

        recvTime = Stats.one_recv(afterSendTime)

        # check cookie
        cookieHdrs = http_response.getheader('set-cookie')
        if cookieHdrs:
            # print (cookieHdrs)
            self._conn.cookie.load(cookieHdrs)

        # # 如果 有 duration，需要接收完消息后sleep一点时间，确保整体时间为duration
        # if duration:
            
        #     # print(f'send {beforeSendTime} -- recv {recvTime}')
        #     extraWait = duration-(recvTime-beforeSendTime)
        #     if extraWait >0:  # 因为小于1ms的sleep通常就是不准确的
        #         # print(f'sleep {extraWait}')
        #         time.sleep(extraWait)

        
        raw_body = http_response.read()
        
        if debug:
            contentEncoding = http_response.getheader('Content-Encoding')
            if contentEncoding == 'gzip':
                try: raw_body = gzip.decompress(raw_body)
                except OSError: pass      

            if response_body_encoding is None:
                contentType = http_response.getheader('Content-Type')
                response_body_encoding = self._guessEncodingFromContentType(contentType)

            self._print_msg(
                raw_body,
                response_body_encoding, 
                bcolors.OKBLUE,
                debug_body_print_max_len)           
            print('\n')


        self.response = HttpResponse(http_response,
                                   raw_body,
                                   int((recvTime-afterSendTime)*1000),
                                   path)
        
     
            
            
        return self.response
    
    @staticmethod
    def _guessEncodingFromContentType(contentType):
        if contentType is not None:
            for one in contentType.replace(' ','').split(';'):
                if one.startswith('charset='):
                    return one[8:]
        return 'utf-8'


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


