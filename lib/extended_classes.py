#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkCookieJar

from lib.containers import TransformedDict
from lib.fingerprint import fake


class Header(TransformedDict):
    def __init__(self, **kwargs):
        super(Header, self).__init__()
        self.h = self.store
        if 'fingerprint_cookiejar' in kwargs.keys():
            self.fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            self.fingerprint_cookiejar = None
   
    def randamize(self, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            fingerprint_cookiejar = self.fingerprint_cookiejar
        headers = fake.headers(fingerprint_cookiejar = fingerprint_cookiejar)
        for key in headers:
            self.h[key] = headers[key]
    


class NetworkManager(QNetworkAccessManager):
    def __init__(self, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            self.fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            self.fingerprint_cookiejar = None
        if 'webpage' in kwargs.keys():
            self.webpage = kwargs['webpage']
        else:
            self.webpage = None
        self.referer = None
        QNetworkAccessManager.__init__(self)
        self.header = Header(fingerprint_cookiejar = self.fingerprint_cookiejar)
        #request = QNetworkRequest(QUrl(url))
        #self.reply = self.get(request)


    def createRequest(self, operation, request, data):
        #print("mymanager handles ", request.url())
        if self.referer and self.webpage.history().canGoBack():
            request.setRawHeader('Referer', self.referer)
        for key in self.header.keys():
            request.setRawHeader(key, self.header[key])
        return QNetworkAccessManager.createRequest( self, operation, request, data )


class ExtendedNetworkCookieJar(QNetworkCookieJar):
    def mozillaCookies(self):
        """
        Return all cookies in Mozilla text format:

        # domain domain_flag path secure_connection expiration name value

        .firefox.com     TRUE   /  FALSE  946684799   MOZILLA_ID  100103
        """
        header = ["# Netscape HTTP Cookie File", ""]
        lines = [get_cookie_line(cookie)
                 for cookie in self.allCookies()]
        return "\n".join(header + lines)

    def cookies_map(self):
        maps = {}
        for i in self.allCookies():
            maps[i] = get_cookie_line(i)
        return maps

    def setMozillaCookies(self, string_cookies):
        """Set all cookies from Mozilla test format string.
        .firefox.com     TRUE   /  FALSE  946684799   MOZILLA_ID  100103
        """
        def str2bool(value):
            return {"TRUE": True, "FALSE": False}[value]
        def get_cookie(line):
            fields = map(str.strip, line.split("\t"))
            if len(fields) != 7:
                return
            domain, domain_flag, path, is_secure, expiration, name, value = fields
            cookie = QNetworkCookie(name, value)
            cookie.setDomain(domain)
            cookie.setPath(path)
            cookie.setSecure(str2bool(is_secure))
            cookie.setExpirationDate(QDateTime.fromTime_t(int(expiration)))
            return cookie
        cookies = [get_cookie(line) for line in string_cookies.splitlines()
          if line.strip() and not line.strip().startswith("#")]
        self.setAllCookies(filter(bool, cookies))

    def cookiesForUrl(self, qurl):
        cookies = QNetworkCookieJar.cookiesForUrl(self, qurl)
        #for i in cookies:
        #    info = get_cookie_info(i)
        #    print "------------>> %(domain)s " % info
        return cookies

