#!/usr/bin/env python3

import csv
import plistlib
import os
import time
import uuid
import xml.etree.ElementTree as ET


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
BASE_PATH = '/Users/matt/code/sms-restore'


def write_csv(plist):
    with open(os.path.join(BASE_PATH, 'output/texts.csv'), 'w') as csvfile:
        fieldnames = ['from', 'to', 'date', 'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for thread in plist['Threads']:
            for item in thread['Items']:
                if 'Content' in item and 'Number' in item and 'SendState' in item:
                    if item['SendState'] == 'Sent':
                        writer.writerow({
                            'from': item['Number'],
                            'to': 'Elizabeth Anderson',
                            'date': item['Time'].strftime(DATE_FORMAT),
                            'message': item['Content']})
                    elif item['SendState'] == 'InBox':
                        writer.writerow({
                            'from': 'Elizabeth Anderson',
                            'to': item['Number'],
                            'date': item['Time'].strftime(DATE_FORMAT),
                            'message': item['Content']})


def write_xml(plist):
    count = 0
    smses = ET.Element('smses')
    smses.set('backup_set', str(uuid.uuid4()))
    smses.set('backup_date', str(time.time()))

    for thread in plist['Threads']:
        for item in thread['Items']:
            if 'Content' in item and 'Number' in item and 'SendState' in item:
                sms = ET.Element('sms')
                sms.set('protocol', '0')
                sms.set('subject', 'null')
                sms.set('body', item['Content'])
                sms.set('toa', 'null')
                sms.set('sc_toa', 'null')
                sms.set('service_center', 'null')
                sms.set('read', '1')
                sms.set('status', '-1')
                sms.set('locked', '0')
                sms.set('date_sent', 'null')
                sms.set('readable_date', 'null')
                sms.set('contact_name', 'null')

                if item['SendState'] == 'Sent':
                    sms.set('type', '2')
                    sms.set('address', item['Number'])
                elif item['SendState'] == 'InBox':
                    sms.set('type', '1')
                    sms.set('address', '+{}'.format(item['Number']))
                count = count + 1
                smses.append(sms)

    smses.set('count', str(count))
    tree = ET.ElementTree(smses)
    tree.write(os.path.join(BASE_PATH, 'output/texts.xml'))


if __name__ == '__main__':
    p1 = plistlib.readPlist(os.path.join(BASE_PATH, 'data/SAMSUNG-SM-G930V_20180318_184420/Messages.list'))

    write_xml(p1)
    #write_csv(p1)
