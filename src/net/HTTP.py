#!/usr/bin/env python
import lswww,urllib,urllib2,urlparse,socket,os
import cgi
import httplib2

class HTTPResponse:
  data=""
  code=200
  headers={}

  def __init__(self,data,code,headers):
    self.data=data
    self.code=code
    self.headers=headers

  def getPage(self):
    return self.data

  def getCode(self):
    return self.code

  def getInfo(self):
    return self.headers

  def getPageCode(self):
    return (self.data,self.code)

class HTTP:
  root=""
  myls=""
  server=""
  cookie=""
  proxy={}
  auth_basic=[]
  timeout=6
  h=None

  def __init__(self,root):
    self.root=root
    self.server=urlparse.urlparse(root)[1]
    self.myls=lswww.lswww(root)
    self.myls.verbosity(1)
    socket.setdefaulttimeout(self.timeout)

  def browse(self):
    self.myls.go()
    urls  = self.myls.getLinks()
    forms = self.myls.getForms()
    director = urllib2.OpenerDirector()

    cookieHandler  = urllib2.BaseHandler()
    proxyHandler = urllib2.BaseHandler()
    basicAuthHandler = urllib2.BaseHandler()
    digestAuthHandler = urllib2.BaseHandler()

    # HttpLib2 vars
    proxy=None

    if self.proxy!={}:
      proxyHandler=urllib2.ProxyHandler(self.proxy)
      proxy=httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, 'localhost', 8000)

    if self.auth_basic!=[]:
      passwordMgr=urllib2.HTTPPasswordMgrWithDefaultRealm()
      passwordMgr.add_password(None, self.root[:-1], self.auth_basic[0], self.auth_basic[1])

      basicAuthHandler =urllib2.HTTPBasicAuthHandler(passwordMgr)
      digestAuthHandler=urllib2.HTTPDigestAuthHandler(passwordMgr)

    try:
      import cookielib
    except ImportError:
      pass
    else:
      if self.cookie!="":
        cj = cookielib.LWPCookieJar()
        if os.path.isfile(self.cookie):
          cj.load(self.cookie,ignore_discard=True)
          cookieHandler=urllib2.HTTPCookieProcessor(cj)

    opener  = urllib2.build_opener(urllib2.HTTPHandler(), urllib2.HTTPSHandler(), proxyHandler, basicAuthHandler, digestAuthHandler, cookieHandler)
    urllib2.install_opener(opener)

    director.add_handler(urllib2.HTTPHandler())
    director.add_handler(urllib2.HTTPSHandler())

    self.h=httplib2.Http(cache=None,timeout=self.timeout,proxy_info=proxy)
    if self.auth_basic!=[]:
      self.h.add_credentials(self.auth_basic[0], self.auth_basic[1])


    return urls, forms

  def getUploads(self):
    return self.myls.getUploads()

  def send(self,target,post_data=None,http_headers={}):
    data=""
    code=0
    info={}
    #
    #try:
    #  req = urllib2.Request(target,post_data,http_headers)
    #  u = urllib2.urlopen(req)
    #  data=u.read()
    #  code=u.code
    #  info=u.info()
    #except (urllib2.URLError,socket.timeout),e:
    #  if hasattr(e,'code'):
    #    data=""
    if post_data==None:
      info,data=self.h.request(target, headers=http_headers)
    else:
      http_headers.update({'Content-type': 'application/x-www-form-urlencoded'})
      info,data=self.h.request(target, "POST", headers=http_headers, body=post_data)
    code=info['status']
    return HTTPResponse(data,code,info)

  def quote(self,url):
    return urllib.quote(url)

  def encode(self,url):
    return urllib.urlencode(url)

  def uqe(self,url):
    return urllib.unquote(urllib.urlencode(url))

  def escape(self,url):
    return cgi.escape(url)

  def setTimeOut(self,timeout=6):
    self.timeout=timeout
    self.myls.setTimeOut(timeout)

  def setProxy(self,proxy={}):
    self.proxy=proxy
    self.myls.setProxy(proxy)

  def addStartURL(self,url):
    self.myls.addStartURL(url)

  def addExcludedURL(self,url):
    self.myls.addExcludedURL(url)

  def setCookieFile(self,cookie):
    self.cookie=cookie
    self.myls.setCookieFile(cookie)

  def setAuthCredentials(self,auth_basic):
    self.auth_basic=auth_basic
    self.myls.setAuthCredentials(auth_basic)

  def addBadParam(self,bad_param):
    self.myls.addBadParam(bad_param)

  def setNice(self,nice=0):
    self.myls.setNice(nice)

  def verbosity(self,vb):
    self.myls.verbosity(vb)

