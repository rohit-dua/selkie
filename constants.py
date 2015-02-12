#!/usr/bin/python
# -*- coding: utf-8 -*-


import os


version = "1.0"
license = "GPLv3"	#./docs/LICENSE.txt
author = 'Rohit Dua <8ohit.dua@gmail.com>'
base_path =  os.path.abspath(os.path.dirname(__file__))
if 'selkie' not in base_path:
	base_path = os.path.join(base_path, 'selkie')
screenshot_path = os.path.join(base_path, 'screenshots')
log_path = os.path.join(base_path, 'log')
lib_path = os.path.join(base_path, 'lib')
requirements_path = os.path.join(base_path, 'requirements')
cache_path = os.path.join(base_path, 'cache')
db_path = os.path.join(base_path, 'db')