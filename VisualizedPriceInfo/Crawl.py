#!/bin/python
# -*- coding: utf-8 -*-


# http://www.twse.com.tw/exchangeReport/MI_INDEX?response=html&date=20170524&type=ALLBUT0999


import os
import re
import sys
import csv
import time
import string
import logging
import requests
import argparse
from datetime import datetime, timedelta

from os import mkdir
from os.path import isdir

FOLDER = 'data'

def string_to_time(string):
    year, month, day = string.split('/')
    return datetime(int(year) + 1911, int(month), int(day))

def is_same(row1, row2):
    if not len(row1) == len(row2):
        return False

    for index in range(len(row1)):
        if row1[index] != row2[index]:
            return False
    else:
        return True

def rmDuplicates():
    file_names = os.listdir(FOLDER)
    for file_name in file_names:
        if not file_name.endswith('.csv'):
            continue

        dict_rows = {}

        # Load and remove duplicates (use newer)
        with open('{}/{}'.format(FOLDER, file_name), 'r') as file:
            for line in file.readlines():
                dict_rows[line.split(',', 1)[0]] = line

        # Sort by date
        rows = [row for date, row in sorted(
            dict_rows.items(), key=lambda x: string_to_time(x[0]))]

        with open('{}/{}'.format(FOLDER, file_name), 'w') as file:
            file.writelines(rows)

class Crawler():
    def __init__(self, prefix="data"):
        ''' Make directory if not exist when initialize '''
        if not isdir(prefix):
            mkdir(prefix)
        self.prefix = prefix

    def _clean_row(self, row):
        ''' Clean comma and spaces '''
        for index, content in enumerate(row):
            row[index] = re.sub(",", "", content.strip())
        return row

    def _record(self, stock_id, row):
        ''' Save row to csv file '''
        f = open('{}/{}.csv'.format(self.prefix, stock_id), 'a')
        cw = csv.writer(f, lineterminator='\n')
        cw.writerow(row)
        f.close()

    def _get_tse_data(self, date_tuple):
        date_str = '{0}{1:02d}{2:02d}'.format(date_tuple[0], date_tuple[1], date_tuple[2])
        url = 'http://www.twse.com.tw/exchangeReport/MI_INDEX'

        query_params = {
            'date': date_str,
            'response': 'json',
            'type': 'ALL',
            '_': str(round(time.time() * 1000) - 500)
        }

        # Get json data
        page = requests.get(url, params=query_params)

        if not page.ok:
            logging.error("Can not get TSE data at {}".format(date_str))
            return

        content = page.json()

        # For compatible with original data
        date_str_mingguo = '{0}/{1:02d}/{2:02d}'.format(date_tuple[0] - 1911, date_tuple[1], date_tuple[2])

        for data in content['data5']:
            sign = '-' if data[9].find('green') > 0 else ''
            row = self._clean_row([
                date_str_mingguo, # 日期
                data[2], # 成交股數
                data[4], # 成交金額
                data[5], # 開盤價
                data[6], # 最高價
                data[7], # 最低價
                data[8], # 收盤價
                sign + data[10], # 漲跌價差
                data[3], # 成交筆數
            ])
        
            self._record(data[0].strip(), row)

    def _get_otc_data(self, date_tuple):
        date_str = '{0}/{1:02d}/{2:02d}'.format(date_tuple[0] - 1911, date_tuple[1], date_tuple[2])
        ttime = str(int(time.time()*100))
        url = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d={}&_={}'.format(date_str, ttime)
        page = requests.get(url)

        if not page.ok:
            logging.error("Can not get OTC data at {}".format(date_str))
            return

        result = page.json()

        if result['reportDate'] != date_str:
            logging.error("Get error date OTC data at {}".format(date_str))
            return

        for table in [result['mmData'], result['aaData']]:
            for tr in table:
                row = self._clean_row([
                    date_str,
                    tr[8], # 成交股數
                    tr[9], # 成交金額
                    tr[4], # 開盤價
                    tr[5], # 最高價
                    tr[6], # 最低價
                    tr[2], # 收盤價
                    tr[3], # 漲跌價差
                    tr[10] # 成交筆數
                ])
                self._record(tr[0], row)


    def get_data(self, date_tuple):
        print('Crawling {}'.format(date_tuple))
        self._get_tse_data(date_tuple)
        self._get_otc_data(date_tuple)

def main():
    # Set logging
    if not os.path.isdir('log'):
        os.makedirs('log')
    logging.basicConfig(filename='log/crawl-error.log',
        level=logging.ERROR,
        format='%(asctime)s\t[%(levelname)s]\t%(message)s',
        datefmt='%Y/%m/%d %H:%M:%S')

    # Get arguments
    parser = argparse.ArgumentParser(description='Crawl data at assigned day')
    #parser.add_argument('day', type=int, nargs='*',
    parser.add_argument('day', nargs='*',
        help='assigned day (format: YYYY MM DD), default is today')
    parser.add_argument('-b', '--back', action='store_true',
        help='crawl back from assigned day until 2004/2/11')
    parser.add_argument('-c', '--check', action='store_true',
        help='crawl back 10 days for check data')
#    parser.add_argument('-t', '--timeperiod', action='store_true',
#        help='a period of time for crawling data (format: YYYYmmdd YYYYmmdd, ex: 20180101 20180131)')
    parser.add_argument('-r', '--rmduplicates', action='store_true',
        help='remove duplicates')
    
    args = parser.parse_args()
#    print "here"
    print(args.day[0])
#    sys.exit()


    # Day only accept 0 or 3 arguments
    if len(args.day) == 0:
        first_day = datetime.today()
    #elif len(args.day) == 3:
#        first_day = datetime(args.day[0], args.day[1], args.day[2])
    elif len(args.day) == 1:
        first_day = datetime(int(args.day[0][0:4]), int(args.day[0][4:6]), int(args.day[0][6:]))
    #elif len(args.day) == 6:
    #    first_day = datetime(args.day[0], args.day[1], args.day[2])
    #    last_day = datetime(args.day[3], args.day[4], args.day[5])
    elif len(args.day) == 2:
        first_day = datetime(int(args.day[0][0:4]), int(args.day[0][4:6]), int(args.day[0][6:]))
        last_day = datetime(int(args.day[1][0:4]), int(args.day[1][4:6]), int(args.day[1][6:]))
    else:
      #  if args.timeperiod:
      #      if len(args.day) == 2:
      #          first_day = datetime(int(args.day[0][0:4]), int(args.day[0][4:6]), int(args.day[0][6:]))
      #          last_day = datetime(int(args.day[1][0:4]), int(args.day[1][4:6]), int(args.day[1][6:]))
      #      else:
      #          parser.error('Date should be assigned with (YYYYmmdd1 YYYYmmdd2)')
      #  else:
        parser.error('Date should be assigned with (YYYYmmdd) or none')
        return

    crawler = Crawler()

    # If back flag is on, crawl till 2004/2/11, else crawl one day
    if args.back or args.check:
        # otc first day is 2007/04/20
        # tse first day is 2004/02/11

        last_day = datetime(2004, 2, 11) if args.back else first_day - timedelta(10)
        max_error = 5
        error_times = 0

        while error_times < max_error and first_day >= last_day:
            try:
                crawler.get_data((first_day.year, first_day.month, first_day.day))
                error_times = 0
            except:
                date_str = first_day.strftime('%Y/%m/%d')
                logging.error('Crawl raise error {}'.format(date_str))
                error_times += 1
                continue
            finally:
                first_day -= timedelta(1)
    else:
        if len(args.day) == 1:
            crawler.get_data((first_day.year, first_day.month, first_day.day))
        elif len(args.day) == 2:
                dateobj = first_day
                while dateobj <= last_day:
                    try: 
                        crawler.get_data((dateobj.year, dateobj.month, dateobj.day))
                    except:
                        logging.error('Crawl raise error {}'.format(dateobj))

                    dateobj = dateobj + timedelta(days=1)

    if args.rmduplicates:
        rmDuplicates()

if __name__ == '__main__':
    main()
