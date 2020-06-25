import pymysql
from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

db_url = 'localhost'
db_user = 'root'
db_pwd = ''
db_name = 'flood'

db = pymysql.connect(db_url, db_user, db_pwd, db_name)
cursor = db.cursor()
raw_data = []

try:
	sql = "SELECT * FROM `waterLevel` ORDER BY datetime"
	cursor.execute(sql)
	raw_data = cursor.fetchall()
except:
	print('error in select date')
finally:
	db.close()

datas = {}
for line in raw_data:
	if line[1] not in datas:
		datas[line[1]] = {}
	time = line[3]
	datatime = format("%d-%d-%d" % (line[3].month, line[3].day, line[3].hour + 0 if line[3].minute < 30 else 1))
	datas[line[1]][datatime] = [float(line[4]), float(line[5])]

x = [datatime for datatime in datas['寸滩']]
y = {}
for site in datas:
	y[site] = [
		[datas[site][datatime][0] for datatime in datas[site]],
		[datas[site][datatime][1] for datatime in datas[site]]
	]

x_major_locator = plt.MultipleLocator(3)
for site in y:
	if len(x) != len(y[site][0]):
		continue
	plt.plot(x, y[site][0], label=site)
plt.xlabel('时间 (月-日-时)')
plt.ylabel('水位')
plt.legend(loc='best')
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
plt.show()

for site in y:
	if len(x) != len(y[site][1]):
		continue
	plt.plot(x, y[site][1], label=site)
plt.xlabel('时间 (月-日-时)')
plt.ylabel('流量')
plt.legend(loc='best')
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
plt.show()
