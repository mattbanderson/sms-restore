#!/usr/bin/env python3

import plistlib


if __name__ == '__main__':
    p1 = plistlib.readPlist('/Users/matt/code/eliz-texts/data/SAMSUNG-SM-G930V_20180318_184420/Messages.list')
    for thread in p1['Threads']:
        for item in thread['Items']:
            if 'Content' in item and 'Number' in item and 'SendState' in item:
                if item['SendState'] == 'Sent':
                    print('{0} said: {1}'.format(item['Number'], item['Content']))
                elif item['SendState'] == 'InBox':
                    print('You replied to {0}: {1}'.format(item['Number'], item['Content']))
