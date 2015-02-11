#!/usr/bin/python
# -*- coding: utf-8 -*-


import os

import constants
from containers import TransformedDict
from fingerprint import fake


class Plugins(object):
    def __init__(self, **kwargs):
        self.plugins = list()
        if 'fingerprint_cookiejar' in kwargs.keys():
            self.fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            self.fingerprint_cookiejar = None
        self.randamize()

    def add(self, name, description, filename, version, length = 0):
        plugin = dict()
        plugin['name'] = name
        plugin['description'] = description
        plugin['filename'] = filename
        plugin['version'] = version
        plugin['length'] = length
        self.plugins.append(plugin)

    def randamize(self, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            fingerprint_cookiejar = self.fingerprint_cookiejar
        fake_plugins = fake.plugins(fingerprint_cookiejar = fingerprint_cookiejar)
        self.plugins = fake_plugins

    def setup(self):
        script = """
        plugins = {};
        plugins.length = %s;
        var index = 0;
        p=%s;
        for (var i in p){
            plugins[p[i].name] =p[i];
            plugins[index] = p[i];
            i = i + 1;
        }
        navigator.__defineGetter__('plugins', function () { return plugins; });
        """ %(len(self.plugins), self.plugins)
        return script


class MimeTypes(object):
    def __init__(self, **kwargs):
        self.mime_types = list()
        if 'fingerprint_cookiejar' in kwargs.keys():
            self.fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            self.fingerprint_cookiejar = None
        self.randamize()

    def add(self, description, mime_type, suffixes):
        mime = dict()
        mime['description'] = description
        mime['type'] = mime_type
        mime['suffixes'] = suffixes
        self.mime_types.append(mime)

    def randamize(self, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            fingerprint_cookiejar = self.fingerprint_cookiejar
        fake_mime_types = fake.MimeTypes(fingerprint_cookiejar = fingerprint_cookiejar)
        self.mime_types = fake_mime_types

    def setup(self):
        script = """
        mime_types = {};
        mime_types.length = %s;
        var index = 0;
        m=%s;
        for (var i in m){
            mime_types[m[i].name] =m[i];
            mime_types[index] = m[i];
            i = i + 1;
        }
        navigator.__defineGetter__('mime_types', function () { return mime_types; });
        """%(len(self.mime_types), self.mime_types)
        return script


class Navigator(TransformedDict):
    def __init__(self, **kwargs):
        super(Navigator, self).__init__()
        self.navigator = self.store
        if 'fingerprint_cookiejar' in kwargs.keys():
            self.fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            self.fingerprint_cookiejar = None
        self.randamize()

    def randamize(self, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            fingerprint_cookiejar = self.fingerprint_cookiejar
        fake_navigator = fake.navigator(fingerprint_cookiejar = fingerprint_cookiejar)
        for i in fake_navigator.keys():
            self.navigator[i] = fake_navigator[i]

    def setup(self):
        script = """var __originalNavigator = navigator;
        navigator = new Object();
        navigator.__proto__ = __originalNavigator;"""
        yield script
        for key in self.navigator.keys():
            if type(self.navigator[key]) == str:
                script = "navigator.__defineGetter__('%s', function () { return '%s'; });" %(key, self.navigator[key])
            else:
                script = "navigator.__defineGetter__('%s', function () { return %s; });" %(key, self.navigator[key])
            yield script


class Screen(TransformedDict):
    def __init__(self, **kwargs):
        super(Screen, self).__init__()
        self.screen = self.store
        if 'fingerprint_cookiejar' in kwargs.keys():
            self.fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            self.fingerprint_cookiejar = None
        self.randamize()

    def randamize(self, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            fingerprint_cookiejar = self.fingerprint_cookiejar
        fake_screen = fake.screen(fingerprint_cookiejar = fingerprint_cookiejar)
        for i in fake_screen.keys():
            self.screen[i] = fake_screen[i]

    def setup(self):
        script = """var __originalScreen = screen;
        screen = new Object();
        screen.__proto__ = __originalScreen;"""
        yield script
        for key in self.screen.keys():
            if type(self.screen[key]) == str:
                script = "screen.__defineGetter__('%s', function () { return '%s'; });" %(key, self.screen[key])
            else:
                script = "screen.__defineGetter__('%s', function () { return %s; });" %(key, self.screen[key])
            yield script
            

class Window(TransformedDict):
    def __init__(self, **kwargs):
        super(Window, self).__init__()
        self.window = self.store
        if 'fingerprint_cookiejar' in kwargs.keys():
            self.fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            self.fingerprint_cookiejar = None
        self.randamize()

    def randamize(self, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            fingerprint_cookiejar = self.fingerprint_cookiejar
        fake_window = fake.window(fingerprint_cookiejar = fingerprint_cookiejar)
        for i in fake_window.keys():
            self.window[i] = fake_window[i]

    def setup(self):
        script = """var __originalWindow = window;
        window = new Object();
        window.__proto__ = __originalWindow;"""
        yield script
        for key in self.window.keys():
            #print key,self.window[key],
            if key == 'history_length':
                script = "history.__defineGetter__('length', function () { return %s; });" %(self.window[key])
            elif type(self.window[key]) == str:
                script = "window.__defineGetter__('%s', function () { return '%s'; });" %(key, self.window[key])
            else:
                script = "window.__defineGetter__('%s', function () { return %s; });" %(key, self.window[key])
            yield script



class Document(TransformedDict):
    def __init__(self, **kwargs):
        super(Document, self).__init__()
        self.document = self.store
        if 'fingerprint_cookiejar' in kwargs.keys():
            self.fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            self.fingerprint_cookiejar = None
        self.randamize()
        self.document['referrer'] = ""
        #self.document['cookie'] = ""

    def randamize(self, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            fingerprint_cookiejar = self.fingerprint_cookiejar
        fake_document = fake.document(fingerprint_cookiejar = fingerprint_cookiejar)
        for i in fake_document.keys():
            self.document[i] = fake_document[i]

    def setup(self):
        script = """var __originalDocument = document;
        document = new Object();
        document.__proto__ = __originalDocument;"""
        yield script
        for key in self.document.keys():
            if type(self.document[key]) == str:
                script = "document.__defineGetter__('%s', function () { return '%s'; });" %(key, self.document[key])
            else:
                script = "document.__defineGetter__('%s', function () { return %s; });" %(key, self.document[key])
            yield script


class Date(object):
    def __init__(self, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            self.fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            self.fingerprint_cookiejar = None
        self.randamize()

    def randamize(self, **kwargs):
        if 'fingerprint_cookiejar' in kwargs.keys():
            fingerprint_cookiejar = kwargs['fingerprint_cookiejar']
        else:
            fingerprint_cookiejar = self.fingerprint_cookiejar
        fake_date = fake.date(fingerprint_cookiejar = fingerprint_cookiejar)
        self.time = fake_date['time']
        self.time_zone_offset = fake_date['time_zone_offset']

    def setup(self):
        self.script = []
        f = open(os.path.join(constants.requirements_path, 'timeshift.js'))
        timeshift_src = f.read()
        self.script.append(timeshift_src)
        self.script.append('Date = TimeShift.Date;')
        self.script.append('TimeShift.setTime(%s);'%self.time)       #undefined for original date
        self.script.append('TimeShift.setTimezoneOffset(%s);'%self.time_zone_offset)
        #self.script.append('Date.prototype.__defineGetter__('getTimezoneOffset', function () { return '-30'''; });'')
        for i in self.script:
            yield i



