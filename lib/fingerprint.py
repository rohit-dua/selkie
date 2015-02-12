#!/usr/bin/python
# -*- coding: utf-8 -*-


from faker import Faker
from faker.providers import BaseProvider
import random
from datetime import datetime, timedelta
import re
import sqlite3
import json

try:
    import constants
except ImportError:
    import selkie.constants as constants


class Dom(BaseProvider):
    """
    def __init__(self):
        #super(Dom, self).__init__( self )
        self.cookie = dict()
    """
    def navigator(self, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
            if fingerprint_cookiejar:
                fingerprint_cookie = fingerprint_cookiejar.data
            else:
                fingerprint_cookie = None
        else:
            fingerprint_cookiejar = None
            fingerprint_cookie = None
        navigator = dict()
        keys = ( 'platform', 'userAgent', 'vendorSub', 'vendor', 'productSub',
            'product', 'platform', 'oscpu', 'language', 'doNotTrack',
            'buildID', 'battery', 'appVersion', 'appName', 'appCodeName'
            )
        linux_platforms = (
            'Linux i686', 'Linux i686 X11', 'Linux x86_64 X11'
            )
        window_platforms = ('Win32',)
        n = dict.fromkeys(keys, 0)
        if fingerprint_cookie and 'userAgent' in fingerprint_cookie.keys():
            n['userAgent'] = fingerprint_cookie['userAgent']
        else:
            n['userAgent'] = fake.user_agent(fingerprint_cookiejar = fingerprint_cookiejar)
        prop = detect_user_agent_properties(n['userAgent'])
        if prop['platform']:
            platform = prop['platform']
        if fingerprint_cookie and 'platform' in fingerprint_cookie.keys():
            platform = fingerprint_cookie['platform']
        if 'windows' in platform.lower():
            n['platform'] = "Win32"
        elif 'linux' in platform.lower():
            n['platform'] = random.choice(linux_platforms)
        if prop['oscpu']:
            n['oscpu'] = prop['oscpu']
        if prop['browser'] == 'firefox':
            n['vendor'] = None
        elif prop['browser'] == 'chrome':
            n['vendor'] = 'Google Inc.'
        elif prop['browser'] == 'opera':
            n['vendor'] = None
        elif prop['browser'] == 'safari':
            n['vendor'] = 'Apple Computer, Inc.'
        if prop['productSub']:
            n['productSub'] = prop['productSub']
        if prop['product']:
            n['product'] = prop['product']
        if prop['browser'] == 'firefox':
            n['language'] = "en-US" 
        else:
            n['language'] = None
        n['doNotTrack'] = "yes"
        if prop['browser'] == 'firefox' or prop['browser'] == 'opera':
            n['buildID'] = str(random_date(datetime(2003,1,1)).date()).replace('-','')
        else:
            n['buildID'] = None
        n['battery'] = random.randint(1, 1000)
        if prop['appVersion']:
            n['appVersion'] = prop['appVersion']
        else:
            n['appVersion'] = None
        n['appName'] = prop['appName']
        navigator['appCodeName'] = "Mozilla"
        for k in n.keys():
            if n[k] != 0:
                navigator[k] = n[k]
        if fingerprint_cookie != None:
            fingerprint_cookie['userAgent'] = navigator['userAgent']
            fingerprint_cookie['platform'] = prop['platform']
            fingerprint_cookie['browser'] = prop['browser']
        return navigator

    def screen(self, **kwargs):
        resolutions = [['1366', '768'], [' 1920', '1080'], [' 1024', '768'], [' 1280', '800'], [' 1440', '900'], [' 1280', '1024'], [' 1600',
        '900'], [' 1680', '1050'], [' 1360', '768'], [' 1280', '720'], [' 1024', '600'], [' 1280', '768'], [' 1920',
        '1200'], [' 1152', '864'], [' 1536', '864'], [' 800', '600'], [' 2560', '1440'], [' 1093', '614'], [' 1364', '768'],
        [' 1280', '960'], [' 1301', '731'], [' 1024', '819'], [' 360', '640'], [' 1438', '808'], [' 1600', '1200'], [
        '1152', '720'], [' 1344', '840'], [' 1242', '698'], [' 1138', '640'], [' 1518', '853'], [' 1188', '668'], [' 1024',
        '640'], [' 1067', '600'], [' 1400', '1050'], [' 320', '534'], [' 1252', '704'], [' 1120', '700'], [' 1024', '576'],
        [' 1607', '904'], [' 360', '592'], [' 1525', '858'], [' 911', '512'], [' 1051', '591'], [' 320', '480'], [' 1821',
        '1024'], [' 640', '480'], [' 1536', '960'], [' 1088', '614'], [' 1524', '857'], [' 819', '614'], [' 1311', '737'],
        [' 1333', '750'], [' 2560', '1600'], [' 960', '600'], [' 1829', '1029'], [' 1680', '945'], [' 1455', '818'], [
        '2048', '1152'], [' 1067', '800'], [' 1012', '569'], [' 1600', '1000'], [' 1097', '617'], [' 1708', '960'], [' 1707',
        '960'], [' 480', '800'], [' 1684', '947'], [' 1745', '982'], [' 320', '570'], [' 1080', '1920'], [' 1391', '783'],
        [' 720', '1280'], [' 1368', '768'], [' 1441', '810'], [' 1365', '1024'], [' 1670', '939'], [' 1249', '702'], [
        '1280', '752'], [' 1600', '1024'], [' 1024', '614'], [' 960', '540'], [' 853', '683'], [' 1760', '990'], [' 1231',
        '692'], [' 2021', '1137'], [' 2133', '1200'], [' 1229', '983'], [' 1477', '831'], [' 1778', '1000'], [' 976',
        '549'], [' 640', '360'], [' 1422', '800'], [' 1080', '810'], [' 1192', '670'], [' 1143', '858'], [' 1768', '992'],
        [' 1067', '853'], [' 1024', '552'], [' 1376', '768']]
        color_depths = (24, 32)
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
            if fingerprint_cookiejar:
                fingerprint_cookie = fingerprint_cookiejar.data
            else:
                fingerprint_cookie = None
        else:
            fingerprint_cookiejar = None
            fingerprint_cookie = None
        screen = dict()
        resolution = random.choice(resolutions)
        screen['width'] = int(resolution[0])
        screen['height'] = int(resolution[1])
        avail_height_diff = random.randint(20,40)
        screen['availHeight'] = screen['height'] - avail_height_diff
        screen['availWidth'] = screen['width']
        screen['colorDepth'] = random.choice(color_depths)
        screen['pixelDepth'] = ""
        if fingerprint_cookie:
            fingerprint_cookie['availWidth'] = screen['availWidth']
            fingerprint_cookie['availHeight'] = screen['availHeight']
        return screen

    def window(self, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
            if fingerprint_cookiejar:
                fingerprint_cookie = fingerprint_cookiejar.data
            else:
                fingerprint_cookie = None
        else:
            fingerprint_cookiejar = None
            fingerprint_cookie = None
        window = dict()
        if fingerprint_cookie and 'availHeight' in fingerprint_cookie.keys():
            window['outerHeight'] = fingerprint_cookie['availHeight'] - random.randint(20, 200)
        else:
            window['outerHeight'] = random.randint(500,900)
        if fingerprint_cookie and 'availWidth' in fingerprint_cookie.keys():
            window['outerWidth'] = fingerprint_cookie['availWidth'] - random.randint(0, 500)
        else:
            window['outerWidth'] = random.randint(800, 1366)
        height_diff = random.randint(330, 380)
        window['innerHeight'] = window['outerHeight'] - height_diff
        window['innerWidth'] = window['outerWidth']
        window['screenX'] = 0
        window['screenY'] = 0
        if fingerprint_cookie and 'platform' in fingerprint_cookie.keys():
            if fingerprint_cookie['platform'] == 'chrome':
                window['chrome'] = True
            elif fingerprint_cookie['platform'] == 'opera':
                window['opera'] = True
        window['history_length'] = random.randint(1,10)
        window['name'] = ""    #May hinder user experience
        if fingerprint_cookie:
            fingerprint_cookie['innerWidth'] = window['innerWidth']
            fingerprint_cookie['outerWidth'] = window['outerWidth']
            fingerprint_cookie['innerHeight'] = window['innerHeight']
            fingerprint_cookie['outerHeight'] = window['outerHeight']
        return window

    """
    UNABLE to override document object
    """
    #not working
    def document(self, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
            if fingerprint_cookiejar:
                fingerprint_cookie = fingerprint_cookiejar.data
            else:
                fingerprint_cookie = None
        else:
            fingerprint_cookiejar = None
            fingerprint_cookie = None
        document = dict()
        #document['referrer'] = "http://tools.wmflabs.org/bub/"   #equals normal referrer 
        #document['cookie'] = ""  #equals normal cookie
        return document

    def date(self, **kwargs):
        time = dict()
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
            if fingerprint_cookiejar:
                fingerprint_cookie = fingerprint_cookiejar.data
            else:
                fingerprint_cookie = None
        else:
            fingerprint_cookiejar = None
            fingerprint_cookie = None
        if fingerprint_cookie and 'time_zone_offset' in fingerprint_cookie.keys():
            time['time_zone_offset'] = fingerprint_cookie['time_zone_offset']
        else:
            gmt_offset = None
            conn = sqlite3.connect(constants.db_path + "/timezonedb.sqlite")
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            if fingerprint_cookie and 'zone_id' in fingerprint_cookie:
                c.execute("""select (gmt_offset/60)*(-1) from timezone where zone_id = %s limit 1;""" %zone_id)
                gmt_offset = c.fetchone()
            if gmt_offset == None:
                c.execute("""select (gmt_offset/60)*(-1) from timezone where zone_id = %s limit 1;""" %random.randint(1,416))
                gmt_offset = c.fetchone()
            gmt_offset = gmt_offset[0]
            time['time_zone_offset'] = gmt_offset
            if fingerprint_cookie:
                fingerprint_cookie['time_zone_offset'] = time['time_zone_offset']
        time['time'] = "undefined"
        return time

    def plugins(self, **kwargs):  #UNDER DEVELOPEMENT
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
            if fingerprint_cookiejar:
                fingerprint_cookie = fingerprint_cookiejar.data
            else:
                fingerprint_cookie = None
        else:
            fingerprint_cookiejar = None
            fingerprint_cookie = None
        plugins = list()
        plugin = dict()
        plugin['name'] = "IcedTea-Web Plugin (using IcedTea-Web 1.4 (1.4-3ubuntu2))"
        plugin['description'] = "The IcedTea-Web Plugin executes Java applets."
        plugin['filename'] = "IcedTeaPlugin.so"
        plugin['version'] = "1.4"
        plugin['length'] = 0
        plugins.append(plugin)
        return plugins

    def MimeTypes(self, **kwargs):  #UNDER DEVELOPEMENT
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
            if fingerprint_cookiejar:
                fingerprint_cookie = fingerprint_cookiejar.data
            else:
                fingerprint_cookie = None
        else:
            fingerprint_cookiejar = None
            fingerprint_cookie = None
        mime_types = list()
        mime = dict()
        mime['description'] = "Annodex exchange format"
        mime['type'] = "application/annodex"
        mime['suffixes'] = "anx"
        mime_types.append(mime)
        return mime_types


class HttpHeaders(BaseProvider):
    def headers(self, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
            if fingerprint_cookiejar:
                fingerprint_cookie = fingerprint_cookiejar.data
            else:
                fingerprint_cookie = None
        else:
            fingerprint_cookiejar = None
            fingerprint_cookie = None
        headers = dict()
        if fingerprint_cookie and 'userAgent' in fingerprint_cookie.keys():
            headers['User-Agent'] = fingerprint_cookie['userAgent']
        else:
            headers['User-Agent'] = fake.user_agent(fingerprint_cookiejar = fingerprint_cookiejar)
            if fingerprint_cookie != None:
                fingerprint_cookie['userAgent'] = headers['User-Agent']
        f = open(constants.db_path + "/lang_code.json")
        r = f.read()
        f.close()
        r = json.loads(r)
        if fingerprint_cookie and 'Accept-Language' in fingerprint_cookie.keys():
            headers['Accept-Language'] = fingerprint_cookie['Accept-Language']
        else:
            if fingerprint_cookie and 'location' in fingerprint_cookie:
                try:
                    region_code = r['region']['location']
                except:
                    region_code = r['region'][random.choice(r['region'].keys())]
            else:
                region_code = r['region'][random.choice(r['region'].keys())]
            headers['Accept-Language'] = "en, en-US;q=0.%s, en-%s;q=0.%s" %(random.randint(2,9), region_code,  random.randint(2,9))
            if fingerprint_cookie:
                fingerprint_cookie['Accept-Language'] = headers['Accept-Language']
        headers['DNT'] = "1"
        """
        headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"  #may break exp. as different for different file formats(image/js/)
        headers['Accept-Charset'] = ""
        headers['Accept-Encoding'] = "gzip, deflate"
        headers['Accept-Ranges'] = ""
        headers['Age'] = ""
        headers['Connection'] = "keep-alive"
        headers['Expect'] = ""
        """
        return headers


class UserAgent(BaseProvider):
    user_agents = (
        'chrome', 'firefox', 'opera', 'safari',
    )

    platforms = ('windows', 'linux', 'mac')

    windows_platform_tokens = (
        'Windows NT 4.0', 'Windows NT 5.0', 'Windows NT 5.01',
        'Windows NT 5.1', 'Windows NT 5.2', 'Windows NT 6.0', 'Windows NT 6.1',
        'Windows NT 6.2', 'Windows NT 6.3',
    )

    windows_processor_tokens = (
        'WOW64', 'Win64, x64',
    )

    linux_processors = ('i686', 'x86_64',)

    mac_processors = ('Intel', 'PPC', 'U; Intel', 'U; PPC',)

    langs = ('en-US',)

    chrome_versions = ( ('41.0.2228.0', '537.36'), ('41.0.2227.1', '537.36'), ('41.0.2227.0', '537.36'), ('41.0.2226.0', '537.36'),
    ('41.0.2225.0', '537.36'), ('41.0.2224.3', '537.36'), ('37.0.2062.124', '537.36'), ('37.0.2049.0', '537.36'),
    ('36.0.1985.125', '537.36'), ('36.0.1985.67', '537.36'), ('36.0.1944.0', '537.36'), ('35.0.3319.102', '537.36'),
    ('35.0.2309.372', '537.36'), ('35.0.2117.157', '537.36'), ('35.0.1916.47', '537.36'), ('34.0.1866.237', '537.36'),
    ('34.0.1847.137', '537.36'), ('34.0.1847.116', '537.36'), ('33.0.1750.517', '537.36'), ('32.0.1667.0', '537.36'),
    ('32.0.1664.3', '537.36'), ('31.0.1650.16', '537.36'), ('31.0.1623.0', '537.36'), ('30.0.1599.17', '537.36'),
    ('29.0.1547.62', '537.36'), ('29.0.1547.57', '537.36'), ('29.0.1547.2', '537.36'), ('28.0.1468.0', '537.36'),
    ('28.0.1467.0', '537.36'), ('28.0.1464.0', '537.36'), ('27.0.1500.55', '537.36'), ('27.0.1453.116', '537.36'),
    ('27.0.1453.93', '537.36'), ('27.0.1453.90', '537.36'), ('24.0.1312.60', '537.17'), ('24.0.1309.0', '537.17'),
    ('24.0.1295.0', '537.15'), ('24.0.1292.0', '537.14'), ('24.0.1290.1', '537.13'), ('24.0.1284.0', '537.13'),
    ('23.0.1271.26', '345667.12221'), ('23.0.1271.26', '537.11'), ('23.0.1271.17', '537.11'), ('23.0.1271.6', '537.11'),
    ('22.0.1229.94', '537.4'), ('22.0.1229.79', '537.4'), ('22.0.1216.0', '537.2'), ('22.0.1207.1', '537.1'),
    ('20.0.1132.57', '536.11'), ('20.0.1092.0', '536.6'), ('20.0.1090.0', '536.6'), ('19.77.34.5', '537.1'),
    ('19.0.1084.56', '536.5'), ('19.0.1084.36', '536.5'), ('19.0.1084.9', '536.5'), ('19.0.1063.0', '536.3'),
    ('19.0.1062.0', '536.3'), ('19.0.1061.1', '536.3'), ('19.0.1061.0', '536.3'), ('19.0.1055.1', '535.24'),
    ('19.0.1047.0', '535.22'), ('19.0.1042.0', '535.21'), ('19.0.1041.0', '535.21'), ('19.0.1036.7', '535.20'),
    ('18.6.872.0', '535.2'), ('18.0.1025.166', '535.19'), ('18.0.1025.151', '535.19'), ('18.0.1025.142', '535.19'),
    ('18.0.1025.46', '535.19'), ('18.0.1025.45', '535.19'), ('18.0.1025.11', '535.19'), ('17.0.963.66', '535.11'),
    ('17.0.963.65', '535.11'), ('17.0.963.56', '535.11'), ('17.0.963.12', '535.11'), ('17.0.940.0', '535.8'),
    ('16.0.912.77', '535.7'), ('16.0.912.75', '535.7'), ('16.0.912.63', '535.8'), ('16.0.912.63', '535.7'),
    ('16.0.912.36', '535.7'), ('16.0.897.0', '535.6'), ('15.0.874.121', '535.2'), ('15.0.874.120', '535.2'),
    ('15.0.874.54', '535.2'), ('15.0.872.0', '535.2'), ('15.0.871.0', '535.2'), ('15.0.864.0', '535.2'), ('15.0.861.0',
    '535.2'), ('15.0.860.0', '535.2'), ('14.0.835.186', '535.1'), ('14.0.834.0', '535.1'), ('14.0.825.0', '535.1'),
    ('14.0.824.0', '535.1'), ('14.0.815.10913', '535.1'), ('14.0.815.0', '535.1'), ('14.0.814.0', '535.1'),
    ('14.0.813.0', '535.1'), ('14.0.812.0', '535.1'), ('14.0.811.0', '535.1'), ('14.0.810.0', '535.1'), ('14.0.809.0',
    '535.1'), ('14.0.808.0', '535.1'), ('14.0.804.0', '535.1'), ('14.0.803.0', '535.1'), ('14.0.801.0', '535.1'),
    ('14.0.794.0', '535.1'), ('14.0.792.0', '535.1'), ('14.0.790.0', '535.1'), ('14.0.564.21', '526.3'), ('13.0.782.220',
    '535.1'), ('13.0.782.215', '535.1'), ('13.0.782.107', '535.1'), ('13.0.782.43', '535.1'), ('13.0.782.41', '535.1'),
    ('13.0.782.32', '535.1'), ('13.0.782.24', '535.1'), ('13.0.782.20', '535.1'), ('13.0.782.14', '535.1'),
    ('13.0.782.1', '535.1'), ('13.0.766.0', '534.36'), ('13.0.764.0', '534.35'), ('13.0.763.0', '534.35'), ('13.0.752.0',
    '534.33'), ('13.0.748.0', '534.31'), ('12.0.750.0', '534.30'), ('12.0.742.113', '534.30'), ('12.0.742.112',
    '534.30'), ('12.0.742.105', '534.30'), ('12.0.742.100', '534.30'), ('12.0.742.93', '534.30'), ('12.0.742.91',
    '534.30'), ('12.0.742.68', '534.30'), ('12.0.742.60', '534.30'), ('12.0.742.53', '534.30'), ('12.0.724.100',
    '534.30'), ('12.0.706.0', '534.25'), ('12.0.704.0', '534.25'), ('12.0.703.0', '534.24'), ('12.0.702.0', '534.24'),
    ('11.0.1245.0', '537.36'), ('11.0.700.3', '534.24'), ('11.0.699.0', '534.24'), ('11.0.698.0', '534.24'),
    ('11.0.697.0', '534.24'), ('11.0.696.71', '534.24'), ('11.0.696.68', '534.24'), ('11.0.696.43', '534.24'),
    ('11.0.696.34', '534.24'), ('11.0.696.14', '534.24'), ('11.0.696.12', '534.24'), ('11.0.696.3', '534.24'),
    ('11.0.696.0', '534.24'), ('11.0.694.0', '534.24'), ('11.0.686.3', '534.23'), ('11.0.682.0', '534.21'),
    ('11.0.678.0', '534.21'), ('11.0.672.2', '534.20'), ('11.0.669.0', '534.20'), ('11.0.661.0', '534.18'),
    ('11.0.661.0', '534.19'), ('11.0.660.0', '534.18'), ('11.0.655.0', '534.17'), ('11.0.654.0', '534.17'),
    ('11.0.652.0', '534.17'), ('10.0.649.0', '534.17'), ('10.0.648.204', '534.16'), ('10.0.648.134', '534.16'),
    ('10.0.648.133', '534.16'), ('10.0.648.127', '534.16'), ('10.0.648.82', '534.16'), ('10.0.648.11', '534.16'),
    ('10.0.648.0', '534.16'), ('10.0.642.0', '534.16'), ('10.0.639.0', '534.16'), ('10.0.638.0', '534.16'),
    ('10.0.634.0', '534.16'), ('10.0.626.0', '534.16'), ('10.0.613.0', '534.15'), ('10.0.612.3', '534.15'),
    ('10.0.612.1', '534.15'), ('10.0.611.0', '534.15'), ('10.0.602.0', '534.14'), ('10.0.601.0', '534.14'), ('9.1.0.0',
    '540.0'), ('9.0.601.0', '534.14'), ('9.0.600.0', '534.14'), ('9.0.599.0', '534.13'), ('9.0.597.107', '534.13'),
    ('9.0.597.98', '534.13'), ('9.0.597.84', '534.13'), ('9.0.597.44', '534.13'), ('9.0.597.19', '534.13'),
    ('9.0.597.15', '534.13'), ('9.0.597.0', '534.13'), ('9.0.596.0', '534.13'), ('9.0.595.0', '534.13'), ('9.0.592.0',
    '534.13'), ('9.0.587.0', '534.12'), ('9.0.583.0', '534.12'), ('9.0.579.0', '534.12'), ('9.0.576.0', '534.12'),
    ('8.1.0.0', '540.0'), ('8.0.558.0', '534.10'), ('8.0.552.344', '534.10'), ('8.0.552.343', '534.10'), ('8.0.552.341',
    '534.10'), ('8.0.552.339', '534.10'), ('8.0.552.237', '534.10'), ('8.0.552.224', '534.10'), ('8.0.552.224', '533.3'),
    ('8.0.552.215', '534.10'), ('8.0.552.210', '534.10'), ('8.0.552.200', '534.10'), ('8.0.551.0', '534.10'),
    ('7.0.548.0', '534.10'), ('7.0.544.0', '534.10'), ('7.0.540.0', '534.10'), ('7.0.531.0', '534.9'), ('7.0.521.0',
    '534.8'), ('7.0.517.24', '534.7'), ('7.0.514.0', '534.7'), ('7.0.500.0', '534.6'), ('7.0.498.0', '534.6'), ('7.0.0',
    '525.13'), ('6.0.481.0', '534.4'), ('6.0.472.63', '534.3'), ('6.0.472.53', '534.3'), ('6.0.472.33', '534.3'),
    ('6.0.470.0', '534.3'), ('6.0.464.0', '534.3'), ('6.0.463.0', '534.3'), ('6.0.462.0', '534.3'), ('6.0.461.0',
    '534.3'), ('6.0.460.0', '534.3'), ('6.0.459.0', '534.3'), ('6.0.458.1', '534.3'), ('6.0.458.0', '534.3'),
    ('6.0.457.0', '534.3'), ('6.0.456.0', '534.3'), ('6.0.454.0', '534.2'), ('6.0.453.1', '534.2'), ('6.0.451.0',
    '534.2'), ('6.0.428.0', '534.1'), ('6.0.427.0', '534.1'), ('6.0.422.0', '534.1'), ('6.0.417.0', '534.1'),
    ('6.0.416.0', '534.1'), ('6.0.414.0', '534.1'), ('6.0.400.0', '533.9'), ('6.0.397.0', '533.8'), ('5.0.375.999',
    '533.4'), ('5.0.375.127', '533.4'), ('5.0.375.126', '533.4'), ('5.0.375.125', '533.4'), ('5.0.375.99', '533.4'),
    ('5.0.375.86', '533.4'), ('5.0.375.70', '533.4'), ('5.0.370.0', '533.4'), ('5.0.368.0', '533.4'), ('5.0.366.2',
    '533.4'), ('5.0.366.0', '533.4'), ('5.0.363.0', '533.3'), ('5.0.359.0', '533.3'), ('5.0.358.0', '533.3'),
    ('5.0.357.0', '533.3'), ('5.0.356.0', '533.3'), ('5.0.355.0', '533.3'), ('5.0.354.0', '533.3'), ('5.0.353.0',
    '533.3'), ('5.0.343.0', '533.2'), ('5.0.342.7', '533.2'), ('5.0.342.5', '533.2'), ('5.0.342.3', '533.2'),
    ('5.0.342.2', '533.2'), ('5.0.342.1', '533.2'), ('5.0.335.0', '533.16'), ('5.0.335.0', '533.1'), ('5.0.310.0',
    '532.9'), ('5.0.309.0', '532.9'), ('5.0.308.0', '532.9'), ('5.0.307.11', '532.9'), ('5.0.307.1', '532.9'),
    ('4.1.249.1025', '532.5'), ('4.0.302.2', '532.8'), ('4.0.288.1', '532.8'), ('4.0.277.0', '532.8'), ('4.0.249.30',
    '532.5'), ('4.0.249.25', '532.5'), ('4.0.249.0', '532.5'), ('4.0.246.0', '532.5'), ('4.0.241.0', '532.4'),
    ('4.0.237.0', '532.4'), ('4.0.227.0', '532.3'), ('4.0.224.2', '532.3'), ('4.0.223.5', '532.3'), ('4.0.223.4',
    '532.2'), ('4.0.223.3', '532.2'), ('4.0.223.2', '532.2'), ('4.0.223.1', '532.2'), ('4.0.223.0', '532.2'),
    ('4.0.222.12', '532.2'), ('4.0.222.8', '532.2'), ('4.0.222.7', '532.2'), ('4.0.222.6', '532.2'), ('4.0.222.5',
    '532.2'), ('4.0.222.4', '532.2'), ('4.0.222.3', '532.2'), ('4.0.222.2', '532.2'), ('4.0.222.1', '532.2'),
    ('4.0.222.0', '532.2'), ('4.0.221.8', '532.2'), ('4.0.221.7', '532.2'), ('4.0.221.6', '532.2'), ('4.0.221.3',
    '532.2'), ('4.0.221.0', '532.2'), ('4.0.220.1', '532.1'), ('4.0.219.6', '532.1'), ('4.0.219.5', '532.1'),
    ('4.0.219.4', '532.1'), ('4.0.219.3', '532.1'), ('4.0.219.0', '532.1'), ('4.0.213.1', '532.1'), ('4.0.213.0',
    '532.1'), ('4.0.212.1', '532.1'), ('4.0.212.0', '532.1'), ('4.0.212.0', '532.0'), ('4.0.211.7', '532.0'),
    ('4.0.211.4', '532.0'), ('4.0.211.2', '532.0'), ('4.0.211.0', '532.0'), ('4.0.210.0', '532.0'), ('4.0.209.0',
    '532.0'), ('4.0.208.0', '532.0'), ('4.0.207.0', '532.0'), ('4.0.206.1', '532.0'), ('4.0.206.0', '532.0'),
    ('4.0.205.0', '532.0'), ('4.0.204.0', '532.0'), ('4.0.203.4', '532.0'), ('4.0.203.2', '532.0'), ('4.0.203.0',
    '532.0'), ('4.0.202.2', '532.0'), ('4.0.202.0', '532.0'), ('4.0.202.0', '525.13'), ('4.0.201.1', '532.0'),
    ('3.0.201.0', '532.0'), ('3.0.198.1', '532.0'), ('3.0.198.0', '532.0'), ('3.0.198', '532.0'), ('3.0.197.11',
    '532.0'), ('3.0.197.0', '532.0'), ('3.0.197', '532.0'), ('3.0.196.2', '532.0'), ('3.0.196.0', '532.0'), ('3.0.196',
    '532.0'), ('3.0.195.33', '532.0'), ('3.0.195.27', '532.0'), ('3.0.195.24', '532.0'), ('3.0.195.21', '532.0'),
    ('3.0.195.20', '532.0'), ('3.0.195.17', '532.0'), ('3.0.195.10', '532.0'), ('3.0.195.6', '532.0'), ('3.0.195.4',
    '532.0'), ('3.0.195.3', '532.0'), ('3.0.195.1', '532.0'), ('3.0.194.0', '531.4'), ('3.0.193.2', '531.3'),
    ('3.0.193.0', '531.3'), ('3.0.192', '531.3'), ('3.0.191.3', '531.2'), ('3.0.191.0', '531.0'), ('2.0.182.0', '530.0'),
    ('2.0.182.0', '531.0'), ('2.0.178.0', '530.8'), ('2.0.177.1', '530.8'), ('2.0.177.0', '530.7'), ('2.0.177.0',
    '530.8'), ('2.0.176.0', '530.7'), ('2.0.175.0', '530.6'), ('2.0.175.0', '530.7'), ('2.0.174.0', '530.5'),
    ('2.0.174.0', '530.6'), ('2.0.173.1', '530.5'), ('2.0.173.0', '530.5'), ('2.0.172.43', '530.5'), ('2.0.172.42',
    '530.5'), ('2.0.172.40', '530.5'), ('2.0.172.39', '530.5'), ('2.0.172.23', '530.5'), ('2.0.172.8', '530.5'),
    ('2.0.172.6', '530.5'), ('2.0.172.2', '530.5'), ('2.0.172.0', '530.5'), ('2.0.172.0', '530.4'), ('2.0.171.0',
    '530.4'), ('2.0.170.0', '530.1'), ('2.0.169.0', '530.1'), ('2.0.168.0', '530.1'), ('2.0.164.0', '530.1'),
    ('2.0.162.0', '530.0'), ('2.0.160.0', '530.0'), ('2.0.157.2', '528.10'), ('2.0.157.0', '528.11'), ('2.0.157.0',
    '528.10'), ('2.0.157.0', '528.9'), ('2.0.156.1', '528.8'), ('2.0.156.0', '528.8'), ('1.0.156.0', '528.8'),
    ('1.0.154.59', '525.19'), ('1.0.154.55', '525.19'), ('1.0.154.53', '525.19'), ('1.0.154.50', '525.19'),
    ('1.0.154.48', '525.19'), ('1.0.154.46', '525.19'), ('1.0.154.43', '525.19'), ('1.0.154.42', '525.19'),
    ('1.0.154.39', '525.19'), ('0.4.154.31', '525.19'), ('0.4.154.18', '525.19'), ('0.3.155.0', '528.4'), ('0.3.155.0',
    '525.19'), ('0.3.154.9', '525.19'), ('0.3.154.6', '525.19'), ('0.2.153.1', '525.19'), ('0.2.153.0', '525.19'),
    ('0.2.152.0', '525.19'), ('0.2.151.0', '525.19'), ('0.2.149.30', '525.13'), ('0.2.149.29', '525.13'), ('0.2.149.27',
    '525.13'), ('0.2.149.6', '525.13'))

    firefox_versions = ['36.0', '33.1', '33.0', '32.0', '31.0', '30.0', '29.0', '28.0', '27.3',
    '27.0', '25.0', '24.0', '23.0', '22.0', '21.0.1', '21.0.0', '21.0', '20.0', '19.0',
    '18.0.1', '18.0', '17.0.6', '17.0', '16.0.1', '16.0', '15.0.2', '15.0.1', '14.0.1',
    '13.0.1', '12.0', '11.0', '10.0.9', '9.0.1', '9.0', '8.0', '7.0', '6.0', '5.0.1',
    '5.0', '4.0.1', '4.0', '3.8', '3.07', '3.6.28', '3.6.25', '3.6.24', '3.6.23', '3.6.22',
    '3.6.21', '3.6.20', '3.6.19', '3.6.18', '3.6.17', '3.6.16', '3.6.15', '3.6.14',
    '3.6.13', '3.6.12', '3.6.11', '3.6.10', '3.6.9', '3.6.8', '3.6.7', '3.6.6', '3.6.4',
    '3.6.3', '3.6.2', '3.6.1', '3.6', '3.5.16', '3.5.15', '3.5.13', '3.5.12', '3.5.11',
    '3.5.10', '3.5.9', '3.5.8', '3.5.7', '3.5.6', '3.5.5', '3.5.4', '3.5.3', '3.5.2',
    '3.5.1', '3.5', '3.03', '3.1.6', '3.1.4', '3.1', '3.0.19', '3.0.18', '3.0.17',
    '3.0.16', '3.0.14', '3.0.13', '3.0.12', '3.0.11', '3.0.10', '3.0.9', '3.0.8',
    '3.0.7', '3.0.6', '3.0.5', '3.0.4', '3.0.3', '3.0.2', '3.0.1', '3.0.0', '3.0',
    '2.1', '2.0.9.9', '2.0.4', '2.0.0.21', '2.0.0.20', '2.0.0.19', '2.0.0.18',
    '2.0.0.17', '2.0.0.16', '2.0.0.15', '2.0.0.14', '2.0.0.13', '2.0.0.12',
    '2.0.0.11', '2.0.0.10', '2.0.0.9', '2.0.0.8', '2.0.0.7', '2.0.0.6',
    '2.0.0.5', '2.0.0.4', '2.0.0.3', '2.0.0.2', '2.0.0.1', '2.0.0.0',
    '2.0.0', '2.0', '1.9.0.1', '1.9.0', '1.5.0.12', '1.5.0.11',
    '1.5.0.10', '1.5.0.9', '1.5.0.8', '1.5.0.7', '1.5.0.6', '1.5.0.5', '1.5.0.4',
    '1.5.0.3', '1.5.0.2', '1.5.0.1', '1.5.0', '1.5', '1.4.1', '1.4', '1.1.16', '1.0.8',
    '1.0.7', '1.0.6', '1.0.5', '1.0.4', '1.0.3', '1.0.2', '1.0.1', '1.0']

    opera_versions = [('12.15', '2.12'), ('12.14', '2.12'), ('12.13', '2.12'), ('12.12', '2.12'), ('12.11', '2.12'), ('12.10', '2.12'),
    ('12.02', '2.10'), ('12.01', '2.10'), ('12.00', '2.10'), ('12.00', '2.9'), ('11.64', '2.10'), ('11.62', '2.10'),
    ('11.61', '2.10'), ('11.60', '2.10'), ('11.52', '2.9'), ('11.51', '2.9'), ('11.50', '2.8'), ('11.11', '2.8'),
    ('11.50', '2.8'), ('11.10', '2.8'), ('11.10', '2.8'), ('11.01', '2.7'), ('11.00', '2.7'), ('11.00', '2.7'), ('10.63',
    '2.6'), ('10.62', '2.6'), ('10.61', '2.6'), ('10.70', '2.6'), ('10.11', '2.2'), ('10.54', '2.5'), ('10.60', '2.5'),
    ('10.60', '2.5'), ('10.53', '2.5'), ('10.52', '2.5'), ('10.51', '2.5'), ('10.50', '2.5'), ('10.50', '2.5'), ('10.50',
    '2.5'), ('10.20', '2.2'), ('10.01', '2.2'), ('10.20', '2.2'), ('10.10', '2.2'), ('10.00', '2.2'), ('10.00', '2.2'),
    ('10.10', '2.2'), ('10.00', '2.2'), ('10.00', '2.2'), ('9.64', '2.1.1'), ('9.63', '2.1.1'), ('9.62', '2.1.1'),
    ('9.61', '2.1.1'), ('9.60', '2.1.1'), ('9.52', '2.1'), ('9.51', '2.1'), ('9.50', '2.1'), ('9.50', '2.1'), ('9.27',
    '2.0'), ('9.26', '2.0'), ('9.25', '2.0'), ('9.24', '2.0'), ('9.23', '2.0'), ('9.22', '2.0'), ('9.21', '2.0'),
    ('9.20', '2.0'), ('9.02', '2.0'), ('9.01', '2.0'), ('9.00', '2.0'), ('9.00', '2.0'), ('9.00', '2.0'), ('8.54',
    '1.0'), ('8.53', '1.0'), ('8.52', '1.0'), ('8.51', '1.0'), ('8.02', '1.0'), ('8.01', '1.0'), ('8.00', '1.0'),
    ('8.00', '1.0'), ('8.00', '1.0'), ('7.60', '1.0'), ('7.60', '1.0'), ('7.60', '1.0'), ('7.60', '1.0'), ('7.54',
    '1.0'), ('7.54', '1.0'), ('7.54', '1.0'), ('7.53', '1.0'), ('7.52', '1.0'), ('7.51', '1.0'), ('7.50', '1.0'),
    ('7.23', '1.0'), ('7.22', '1.0'), ('7.21', '1.0'), ('7.20', '1.0'), ('7.11', '1.0'), ('7.03', '1.0'), ('7.02',
    '1.0'), ('7.01', '1.0'), ('7.01', '1.0'), ('7.00', '1.0'), ('7.00', '1.0'), ('7.00', '1.0')]


    def mac_processor(cls):
        return cls.random_element(cls.mac_processors)


    def linux_processor(cls):
        return cls.random_element(cls.linux_processors)


    def user_agent(cls, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
            if fingerprint_cookiejar:
                fingerprint_cookie = fingerprint_cookiejar.data
            else:
                fingerprint_cookie = None
        else:
            fingerprint_cookiejar = None
            fingerprint_cookie = None
        if fingerprint_cookie and 'browser' in fingerprint_cookie.keys():
            if fingerprint_cookie['browser'] in cls.user_agents:
                name = fingerprint_cookie['browser']
                return getattr(cls, name)(fingerprint_cookiejar = fingerprint_cookiejar)    
        name = cls.random_element(cls.user_agents)
        return getattr(cls, name)(fingerprint_cookiejar = fingerprint_cookiejar)


    def chrome(cls, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
            if fingerprint_cookiejar:
                fingerprint_cookie = fingerprint_cookiejar.data
            else:
                fingerprint_cookie = None
        else:
            fingerprint_cookiejar = None
            fingerprint_cookie = None
        saf = str(random.randint(531, 537)) + "." + str(random.randint(1, 30))
        tmplt = '({0}) AppleWebKit/{1} (KHTML, like Gecko)' \
                ' Chrome/{2} Safari/{3}'
        version = random.choice(cls.chrome_versions)[0]
        platforms = {
            'linux' : tmplt.format(cls.linux_platform_token(),
                         saf,
                         version,
                         saf),
            'windows' : tmplt.format(cls.windows_platform_token(),
                         saf,
                         version,
                         saf),
            'mac' : tmplt.format(cls.mac_platform_token(),
                         saf,
                         version,
                         saf),
        }

        if fingerprint_cookie and 'platform' in fingerprint_cookie.keys():
            if fingerprint_cookie['platform'].lower() in cls.platforms:
                return 'Mozilla/5.0 ' + platforms[fingerprint_cookie['platform'].lower()]
        return 'Mozilla/5.0 ' + platforms[cls.random_element(platforms.keys())]


    def firefox(cls, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
            if fingerprint_cookiejar:
                fingerprint_cookie = fingerprint_cookiejar.data
            else:
                fingerprint_cookie = None
        else:
            fingerprint_cookiejar = None
            fingerprint_cookie = None
        version = random.choice(cls.firefox_versions)
        ver = (
            'Gecko/{0} Firefox/{1}'.format(
                str(datetime(2011, 1, 1).date()).replace('-', ''), version),
            'Gecko/{0} Firefox/{1}'.format(
                str(random_date(
                    datetime(2010, 1, 1)).date()).replace('-', ''), version),
        )
        tmplt_win = '({0}; {1}; rv:{2}) {3}'
        tmplt_lin = '({0}; rv:{1}) {2}'
        tmplt_mac = '({0}; rv:{1}) {2}'
        platforms = {
            'windows' : tmplt_win.format(cls.windows_platform_token(),
                             cls.random_element(cls.langs),
                             version,
                             random.choice(ver)),
            'linux' : tmplt_lin.format(cls.linux_platform_token(),
                             version,
                             random.choice(ver)),
            'mac' : tmplt_mac.format(cls.mac_platform_token(),
                             version,
                             random.choice(ver)),
        }
        if fingerprint_cookie and 'platform' in fingerprint_cookie.keys():
            return 'Mozilla/5.0 ' + platforms[fingerprint_cookie['platform'].lower()]
        return 'Mozilla/5.0 ' + platforms[cls.random_element(platforms.keys())]


    def safari(cls, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
            if fingerprint_cookiejar:
                fingerprint_cookie = fingerprint_cookiejar.data
            else:
                fingerprint_cookie = None
        else:
            fingerprint_cookiejar = None
            fingerprint_cookie = None
        saf = "{0}.{1}.{2}".format(random.randint(531, 535),
                                   random.randint(1, 50),
                                   random.randint(1, 7))
        if random.randint(0, 1) == 0:
            ver = "{0}.{1}".format(random.randint(4, 5),
                                   random.randint(0, 1))
        else:
            ver = "{0}.0.{1}".format(random.randint(4, 5),
                                     random.randint(1, 5))
        tmplt_win = '(Windows; U; {0}) AppleWebKit/{1} (KHTML, like Gecko)' \
                    ' Version/{2} Safari/{3}'
        tmplt_mac = '({0} rv:{1}.0; {2}) AppleWebKit/{3} (KHTML, like Gecko)' \
                    ' Version/{4} Safari/{5}'
        platforms = {
            'windows' : tmplt_win.format(cls.windows_platform_token(),
                             saf,
                             ver,
                             saf),
            'mac' : tmplt_mac.format(cls.mac_platform_token(),
                             random.randint(2, 6),
                             cls.random_element(cls.langs),
                             saf,
                             ver,
                             saf),
        }
        if fingerprint_cookie and 'platform' in fingerprint_cookie.keys():
            return 'Mozilla/5.0 ' + platforms[fingerprint_cookie['platform'].lower()]
        return 'Mozilla/5.0 ' + platforms[cls.random_element(platforms.keys())]


    def opera(cls, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
            if fingerprint_cookiejar:
                fingerprint_cookie = fingerprint_cookiejar.data
            else:
                fingerprint_cookie = None
        else:
            fingerprint_cookiejar = None
            fingerprint_cookie = None
        version = random.choice(cls.opera_versions)[0]
        tmplt = '({0}; {1}) Presto/2.9.{2} Version/{3}'
        platforms = {
            'linux' : tmplt.format(cls.linux_platform_token(),
                         cls.random_element(cls.langs),
                         random.randint(160, 190),
                         version),
            'windows' : tmplt.format(cls.windows_platform_token(),
                         cls.random_element(cls.langs),
                         random.randint(160, 190),
                         version),
        }
        if fingerprint_cookie and 'platform' in fingerprint_cookie.keys():
            return 'Opera/{0}.{1}.{2}'.format(random.randint(8, 9), random.randint(10, 99), platforms[fingerprint_cookie['platform'].lower()])
        return 'Opera/{0}.{1}.{2}'.format(random.randint(8, 9),
                                          random.randint(10, 99),
                                          platforms[cls.random_element(platforms.keys())])



    def windows_platform_token(cls):
        processor = random.choice(("32 bit", "64 bit"))
        if processor == "64 bit":
            return cls.random_element(cls.windows_platform_tokens) + "; " + cls.random_element(cls.windows_processor_tokens)
        else:
            return cls.random_element(cls.windows_platform_tokens)


    def linux_platform_token(cls):
        return 'X11; Linux {0}'.format(
            cls.random_element(cls.linux_processors))


    def mac_platform_token(cls):
        return 'Macintosh; {0} Mac OS X 10_{1}_{2}'.format(
            cls.random_element(cls.mac_processors),
            random.randint(5, 8), random.randint(0, 9))

def detect_user_agent_properties(user_agent):
    appVersion = None
    appName = None
    platform = None
    browser = None
    productSub = None
    product = None
    cpu = None
    if 'windows' in user_agent.lower():
        platform = 'windows'
    elif 'linux' in user_agent.lower():
        platform = 'linux'
    elif 'mac' in user_agent.lower():
        platform = 'mac'
    if 'chrome' in user_agent.lower():
        browser = 'chrome'
        productSub = "20030107"
        appVersion = user_agent[8:]  
        appName = "Netscape"     
    elif 'safari' in user_agent.lower():
        browser = 'safari'
        productSub = "20030107"
        appVersion = user_agent[8:]   
        appName = "Netscape"
    elif 'opera' in user_agent.lower():
        browser = 'opera'
        productSub = "20030107"
        appVersion = user_agent[8:]   
        appName = "Opera"
    elif 'firefox' in user_agent.lower():
        browser = 'firefox'
        productSub = "20100101"
        appName = "Netscape"
        if platform == 'windows':
            appVersion = "5.0 (Windows)"
        elif platform == 'linux':
            appVersion = "5.0 (X11)"
        elif platform == 'mac':
            appVersion = "5.0 (Mac)"
    if platform == 'windows':
        cpu = re.search('(Windows[^\)]+)\s*\S*-*\S*',user_agent).group(1)
    elif platform == 'linux':
        cpu = re.search('(Linux[^\)]+)\s*\S*-*\S*',user_agent).group(1)
    elif platform == 'mac':
        cpu = re.search('(Macintosh[^\)]+)\s*\S*-*\S*',user_agent).group(1)
    if "gecko" in user_agent.lower():
        product = "Gecko"
    elif "presto" in user_agent.lower():
        product = "Presto"
    prop = dict()
    prop['platform'] = platform
    prop['browser'] = browser
    prop['oscpu'] = cpu
    prop['product'] = product
    prop['productSub'] = productSub
    prop['appVersion'] = appVersion
    prop['appName'] = appName
    return prop


def random_date(start, end = datetime.now()):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    if delta in (0,None,''):
        return start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)



fake = Faker()        
fake.add_provider(Dom)
fake.add_provider(HttpHeaders)
fake.add_provider(UserAgent)
