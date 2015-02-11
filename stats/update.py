#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Browser stats obtained from statcounter.com

from datetime import datetime
import requests
import csv
import os
import time

import ujson


def get(device = 'desktop', stat_type = 'browser', local_filename = ".tmp.csv"):
    print "+"*30
    print stat_type
    countries = [ ('ww', 'Worldwide'), ('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AD', 'Andorra'),
    ('AO', 'Angola'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AU', 'Australia'), ('AT', 'Austria'),
    ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BY', 'Belarus'),
    ('BE', 'Belgium'), ('BJ', 'Benin'), ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BW', 'Botswana'),
    ('BR', 'Brazil'), ('BG', 'Bulgaria'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'),
    ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CO', 'Colombia'), ('KM', 'Comoros'),
    ('HR', 'Croatia'), ('CU', 'Cuba'), ('CY', 'Cyprus'), ('DK', 'Denmark'), ('DJ', 'Djibouti'),
    ('DM', 'Dominica'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('ER', 'Eritrea'), ('EE', 'Estonia'),
    ('ET', 'Ethiopia'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GA', 'Gabon'),
    ('GM', 'Gambia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GR', 'Greece'), ('GT', 'Guatemala'),
    ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'),
    ('HN', 'Honduras'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'),
    ('IR', 'Iran'), ('IQ', 'Iraq'), ('IL', 'Israel'), ('IT', 'Italy'), ('JE', 'Jersey'), ('JO', 'Jordan'),
    ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KW', 'Kuwait'), ('LA', 'Lao'),
    ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LI', 'Liechtenstein'),
    ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MK', 'Macedonia'), ('MG', 'Madagascar'),
    ('MW', 'Malawi'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MR', 'Mauritania'),
    ('MU', 'Mauritius'), ('MX', 'Mexico'), ('FM', 'Micronesia'), ('MD', 'Moldova'), ('MC', 'Monaco'),
    ('ME', 'Montenegro'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'),
    ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NI', 'Nicaragua'), ('NE', 'Niger'),
    ('NG', 'Nigeria'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'),
    ('PA', 'Panama'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PL', 'Poland'),
    ('PT', 'Portugal'), ('QA', 'Qatar'), ('RW', 'Rwanda'), ('WS', 'Samoa'), ('SN', 'Senegal'),
    ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SG', 'Singapore'), ('SI', 'Slovenia'), ('SO', 'Somalia'),
    ('ES', 'Spain'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SZ', 'Swaziland'), ('SE', 'Sweden'),
    ('CH', 'Switzerland'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania'), ('TH', 'Thailand'),
    ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TO', 'Tonga'), ('TN', 'Tunisia'), ('TR', 'Turkey'),
    ('UG', 'Uganda'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'),
    ('VE', 'Venezuela'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe') ]

    year_now = datetime.now().year
    month_now = datetime.now().month
    date = "%s-%s"%(year_now, month_now)

    url = """http://gs.statcounter.com/chart.php?device={{DEVICE}}&device_hidden={{DEVICE}}""" + \
    """&statType_hidden={{STAT_TYPE}}&region_hidden={{REGION_CODE}}&granularity=monthly&statType={{STAT_TYPE}}&""" + \
    """region={{REGION}}&fromInt={{DATE_INT}}&toInt={{DATE_INT}}&fromMonthYear={{DATE_FORMATTED}}&""" + \
    """toMonthYear={{DATE_FORMATTED}}&{{DATE_INT}}=undefined&multi-device=true&csv=1"""
    url = url.replace("{{DEVICE}}", device.lower())
    url = url.replace("{{STAT_TYPE}}", stat_type.lower())
    url = url.replace("{{DATE_FORMATTED}}", date)
    url = url.replace("{{DATE_INT}}", date.replace("-", ""))
    stat = dict()
    for ind, country in enumerate(countries):
        if ind==1:
            break
        region_code = country[0]
        region = country[1]
        stat[region] = dict()
        url = url.replace("{{REGION_CODE}}", region_code)
        url = url.replace("{{REGION}}", region)
        try:
            r = requests.get(url)
        except:
            time.sleep(5)
            r = requests.get(url)
        f = open(local_filename, 'w')
        for chunk in r.iter_content(chunk_size=512 * 1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
        f.close()
        with open(local_filename, 'r') as f:
            csv_read = csv.reader(f)
            for index, i in enumerate(csv_read):
                if index == 0:
                    continue
                stat[region][i[0]] = i[1]
        os.remove(local_filename)
        print "Done %s" %region
    return stat


def update(filename = 'stats.json'):
    devices = ['desktop', 'mobile']
    stat_types = ['browser', 'browser_version', 'resolution', 'os']
    if device != 'desktop':
        stat_type.append('vendor')
    stats = dict()
    for d in devices:
        stats[d] = dict()
        for s in stat_types:
            stat = get(device = d, stat_type = s)
            stats[d][s] = stat
    stats_file = open("."+ filename, 'w')
    stats = ujson.dumps(stats)
    stats_file.write(stats)
    stats_file.close()  
    """
    os.remove(filename)  
    os.rename("."+filename, filename)
    f= open('last_update.log','w')
    f.write(str(datetime.now())
    f.close()
    """







if __name__ == '__main__':
    update()




import collections


class TransformedDict(collections.MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys
    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]
    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value
    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]
    def __iter__(self):
        return iter(self.store)
    def __len__(self):
        return len(self.store)
    def __keytransform__(self, key):
        return key
