#!/usr/bin/env python3

import csv
import plistlib


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


if __name__ == '__main__':
    p1 = plistlib.readPlist('/Users/matt/code/eliz-texts/data/SAMSUNG-SM-G930V_20180318_184420/Messages.list')
    with open('/Users/matt/code/eliz-texts/output/texts.csv', 'w') as csvfile:
        fieldnames = ['from', 'to', 'date', 'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for thread in p1['Threads']:
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
