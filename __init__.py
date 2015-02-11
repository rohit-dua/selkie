#!/usr/bin/env python
# -*- coding: utf-8 -*-
# _______ _______        _     _ _____ _______
# |______ |______ |      |____/    |   |______
# ______| |______ |_____ |    \_ __|__ |______


from datetime import datetime
import os
import signal
import sys
import time
import json
 
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage, QWebSettings
from PyQt4.QtNetwork import QNetworkCookie, QNetworkCookieJar
from PyQt4.QtNetwork import QNetworkProxy
from spynner import Browser

import constants
from lib.dom import Navigator, Window, Screen, Document, Date, Plugins, MimeTypes
from lib.extended_classes import ExtendedNetworkCookieJar, Header, NetworkManager
from lib.fingerprint import fake


class Driver(Browser):
    def __init__(self, **kwargs):
        super(Driver, self).__init__( self )
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            fingerprint_cookiejar = FingerprintCookiejar()
        self.fingerprint_cookiejar = fingerprint_cookiejar
        self.manager = NetworkManager(fingerprint_cookiejar = fingerprint_cookiejar, webpage = self.webpage)
        self.webpage.setNetworkAccessManager(self.manager)
        self.create_webview()
        #self.headers = None
        self.header = self.manager.header
        self.cookies_jar = ExtendedNetworkCookieJar()
        self.manager.setCookieJar(self.cookies_jar)
        self.navigator = Navigator(fingerprint_cookiejar = fingerprint_cookiejar)
        self.screen = Screen(fingerprint_cookiejar = fingerprint_cookiejar)
        self.window = Window(fingerprint_cookiejar = fingerprint_cookiejar)
        self.document = Document(fingerprint_cookiejar = fingerprint_cookiejar)
        self.date = Date(fingerprint_cookiejar = fingerprint_cookiejar)
        self.plugins = Plugins(fingerprint_cookiejar = fingerprint_cookiejar)
        self.mime_types =MimeTypes(fingerprint_cookiejar = fingerprint_cookiejar)
        self.webpage.mainFrame().javaScriptWindowObjectCleared.connect(self.setup_dom)
        self.webpage.mainFrame().loadFinished.connect(self.finished_loading)
        self.developers_extra_enabled()
        #self.webpage.mainFrame().setFocus()

    def get(self, *args, **kwargs):
        """Load webpage"""
        signal.alarm(0)
        if 'referer' in kwargs.keys() or 'referrer' in kwargs.keys():
            self.manager.referer = kwargs['referer']
            self.document['referrer'] = kwargs['referer']
            self.document.setup()
            del kwargs['referer']
        else:
            self.manager.referer = None
        if 'wait_js_load' in kwargs.keys():
            wait_js_load = kwargs['wait_js_load']
            del kwargs['wait_js_load']
        else:
            wait_js_load = True
        self.load(*args, **kwargs)
        if wait_js_load:
            self.wait_js_load()
        signal.signal(signal.SIGALRM, self.process_events)
        signal.setitimer(signal.ITIMER_REAL, 2, 2)

    def load_images(self, value = True):
        QWebSettings.globalSettings().setAttribute(QWebSettings.AutoLoadImages, value)

    def javascript_enabled(self, value = True):
        QWebSettings.globalSettings().setAttribute(QWebSettings.JavascriptEnabled, value)

    def java_enabled(self, value = True):
        QWebSettings.globalSettings().setAttribute(QWebSettings.JavaEnabled, value)

    def plugins_enabled(self, value = False):    
        QWebSettings.globalSettings().setAttribute(QWebSettings.PluginsEnabled, value)

    def private_browsing(self, value = False):
        QWebSettings.globalSettings().setAttribute(QWebSettings.PrivateBrowsingEnabled, value)

    def clear_cache(self):
        QWebSettings.globalSettings().clearMemoryCaches()
        QWebSettings.globalSettings().clearIconDatabase()

    def enable_persistant_storage(self, path):
        QWebSettings.globalSettings().enablePersistentStorage(path)

    def developers_extra_enabled(self, value = True):
        QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, value)

    def randamize_dom(self, **kwargs):
        """Randomize the values of dom objects."""
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            fingerprint_cookiejar = FingerprintCookiejar()
        self.fingerprint_cookiejar = fingerprint_cookiejar
        self.navigator.randamize(fingerprint_cookiejar = fingerprint_cookiejar)
        self.screen.randamize(fingerprint_cookiejar = fingerprint_cookiejar)
        self.window.randamize(fingerprint_cookiejar = fingerprint_cookiejar)
        #self.document.randamize(fingerprint_cookiejar = fingerprint_cookiejar)
        self.date.randamize(fingerprint_cookiejar = fingerprint_cookiejar)
        self.plugins.randamize(fingerprint_cookiejar = fingerprint_cookiejar)
        self.mime_types.randamize(fingerprint_cookiejar = fingerprint_cookiejar)

    def randamize_headers(self, **kwargs):
        """Randomize HTTP Header values"""
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            fingerprint_cookiejar = FingerprintCookiejar()
        self.fingerprint_cookiejar = fingerprint_cookiejar
        self.header.randamize(fingerprint_cookiejar = fingerprint_cookiejar)

    def randamize_fingerprint(self, **kwargs):
        """Randomize Headers + Dom"""
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            fingerprint_cookiejar = FingerprintCookiejar()
        self.fingerprint_cookiejar = fingerprint_cookiejar
        self.randamize_dom(fingerprint_cookiejar = fingerprint_cookiejar)
        self.randamize_headers(fingerprint_cookiejar = fingerprint_cookiejar)

    def setup_fingerprint(self):
        self.setup_dom()
        if self.page_level == 0 and self.referer:
            self.header['Referer'] = self.referer
            self.referer = None
        self.page_level += 1

    def setup_dom(self):
        #return
        self.setup_navigator()
        self.setup_screen()
        self.setup_window()
        #self.setup_document()
        self.setup_date()
        #self.setup_plugins()
        self.setup_mime_types()

    def setup_navigator( self):
        script = self.navigator.setup()
        for s in script:
            self.webpage.mainFrame().evaluateJavaScript(s)

    def setup_screen(self):
        script = self.screen.setup()
        for s in script:
            self.webpage.mainFrame().evaluateJavaScript(s)

    def setup_window(self):
        script = self.window.setup()
        for s in script:
            self.webpage.mainFrame().evaluateJavaScript(s)
        if self.fingerprint_cookiejar != None:
            fingerprint_cookie = self.fingerprint_cookiejar.data
            self.webpage.setViewportSize(QSize(fingerprint_cookie['innerWidth'],fingerprint_cookie['innerHeight']))

    def setup_document(self):
        script = self.document.setup()
        for s in script:
            self.webpage.mainFrame().evaluateJavaScript(s)

    def setup_date(self):
        script = self.date.setup()
        for s in script:
            self.webpage.mainFrame().evaluateJavaScript(s)

    def setup_plugins(self):
        script = self.plugins.setup()
        self.webpage.mainFrame().evaluateJavaScript(script)

    def setup_mime_types(self):
        script = self.mime_types.setup()
        self.webpage.mainFrame().evaluateJavaScript(script)

    def set_user_agent(self, user_agent):
        self.navigator['userAgent'] = user_agent
        self.manager.header['User-Agent'] = user_agent

    def screenshot(self, filename = None, path = constants.screenshot_path, box = None):
        if filename == None:
            filename = str(datetime.now()).replace(' ', '')
        if not os.path.isabs(filename):
            filename = os.path.join(path, filename)
        if filename[-3:] != 'png' and filename[-4:] != 'jpeg':
            filename = filename + ".png"
        self.snapshot(box = box).save(filename)
 
    def finished_loading( self, result ):
        """
        time.sleep(20)
        print "loading finished"
        #self.moveMouse(QPoint(600,600))
        #self.moveMouse(QPoint(600,601))
        time.sleep(5)
        file = open( "test_file.html", 'w' )
        file.write( self.webpage.currentFrame().documentElement().toInnerXml() )
        file.close()
        print "1 down.."
        #self.browse()
        """ 

    def stop_loading(self):
        """Stop the js execution timer signal"""
        signal.alarm(0)

    def wait_js_load(self, delay=0.1, timeout = 5.0):
        """Wait for javascript to load untill timeout"""
        # process app events until page loaded
        t = time.time()
        while self.application.hasPendingEvents() and time.time() - t < timeout:
            self.application.processEvents()
            time.sleep(delay)
        self._loaded = False

    def process_events(self, signum, _):
        """Process javascript events and update dom"""
        print "process"
        for i in range(2):
            if self.application.hasPendingEvents():
                self.application.processEvents()

    def get_cookies(self):
        """Return string containing the current cookies in Mozilla format."""
        return self.cookies_jar.mozillaCookies()

    def set_cookies(self, string_cookies):
        """Set cookies from a string with Mozilla-format cookies."""
        return self.cookies_jar.setMozillaCookies(string_cookies)

    def clear_cookies(self):
        self.set_cookies("")

    def gather_info(self, elem, i=0):
        if i > 200: return
        cnt = 0
        output = []
        while cnt < 100:
            s = elem.toPlainText()
            rect = elem.geometry()
            name = elem.tagName()
            dim = [rect.x(), rect.y(), 
                rect.x() + rect.width(), rect.y() + rect.height()]
            if s: output.append(dict(pos=(i, cnt), dim=dim, tag=name, text=s))
            child = elem.firstChild()
            if not child.isNull():
                self.gather_info(child, i+1)
            elem = elem.nextSibling()
            if elem.isNull(): 
                break
            cnt += 1
        return output



class FingerprintCookiejar(object):
    def __init__(self):
        self.data = dict()

    def to_string(self):
        return json.dumps(self.data)

    def from_string(self, string):
        self.data = json.loads(string)



def main():
    b = Driver()
    #b.enable_persistant_storage(constants.cache_path)
    #b.javascript_enabled(False)
    #b.plugins_enabled(False)
    #b.private_browsing(True)
    #b.load("http://www.alanwood.net/demos/browserinfo.html")
    #b.load("http://www.lalit.org/lab/javascript-css-font-detect/")
    #b.load("http://www.google.com/fonts", load_timeout=50)
    #b.load('http://flippingtypical.com/', load_timeout=50)
    #b.load("http://browserspy.dk/window.php", load_timeout=50)
    #b.load("http://www.pinlady.net/PluginDetect/All/navarray.php", load_timeout=50)
    #b.load('http://gs.statcounter.com/')
    #b.get('http://myhttp.info/', referer = "rohit")
    #b.get("http://dafont.com", load_timeout = 20)
    b.get("https://www.google.com/fonts", load_timeout=50)
    print b.gather_info(elem = b.webpage.mainFrame().documentElement())


if __name__ == '__main__':
    sys.exit(main())

    