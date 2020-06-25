import requests
import json
import time
import pymysql

url = 'http://www.cjh.com.cn/sqindex.html'

response = requests.get(url)
response.encoding = 'utf-8'
web_data = response.text
web_data = web_data[web_data.find('var sssq = ') + 11 :]
web_data = web_data[: web_data.find(';')]
data = json.loads(web_data)
# print(data)

db_url = 'localhost'
db_user = root
db_pwd = ''
db_name = 'flood'
sql_template = "INSERT INTO `waterLevel` (`site`, `waterSource`, `datetime`, `waterLevel`, `flow`) \
    VALUES ('%s', '%s', '%s', '%s', '%s')"

db = pymysql.connect(db_url, db_user, db_pwd, db_name)
cursor = db.cursor()

for record in data:
    waterLevel = record['z']
    in_flow = record['q']
    out_flow = record['oq']
    site = record['stnm']
    waterSource = record['rvnm']
    datetime = time.localtime(int(record['tm']) // 1000)
    datetime = format("%d-%02d-%02d %02d:%02d:%02d" %
                      (datetime.tm_year, datetime.tm_mon, datetime.tm_mday,
                      datetime.tm_hour, datetime.tm_min, datetime.tm_sec))
    try:
        if int(in_flow) > 0:
            try:
                sql = format("SELECT MAX(`datetime`) FROM `waterLevel` WHERE site = '%s'" % site)
                cursor.execute(sql)
                latest_date = cursor.fetchone()
            except:
                print('error in select latest date')
            if latest_date[0] is None or str(latest_date[0]) < datetime:
                sql = format(sql_template % (site, waterSource, datetime, waterLevel, in_flow))
                # print(sql)
                cursor.execute(sql)
                print("updata %s at %s" % (site, datetime))
        if int(out_flow) > 0:
            try:
                sql = format("SELECT MAX(`datetime`) FROM `waterLevel` WHERE site = '%s'" % (site + '(出库)'))
                cursor.execute(sql)
                latest_date = cursor.fetchone()
            except:
                print('error in select latest date')
            if latest_date[0] is None or str(latest_date[0]) < datetime:
                sql = format(sql_template % (site + '(出库)', waterSource, datetime, waterLevel, out_flow))
                # print(sql)
                cursor.execute(sql)
                print("updata %s at %s" % (site + '(出库)', datetime))
        db.commit()
    except:
        db.rollback()
        print('error in insert date: ', record)
db.close()
