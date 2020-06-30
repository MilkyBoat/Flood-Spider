import pymysql
import json


def output():
	db_url = 'localhost'
	db_user = 'root'
	db_pwd = ''
	db_name = 'flood'
	js_path = './js/'

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
		datatime = format(
			"%d-%d-%d" % (line[3].month, line[3].day, line[3].hour + 0 if line[3].minute < 30 else 1))
		datas[line[1]][datatime] = [float(line[4]), float(line[5])]

	max_len = max([len(datas[i]) for i in datas])

	data = {
		'level': {
			'legend': {'type': 'scroll', 'top': 10, 'data': []},
			'dataZoom': [
				{ 'startValue': 1, 'type': 'slider', 'xAxisIndex': [0]},
				{ 'startValue': 1, 'type': 'slider', 'yAxisIndex': [0]}
			],
			'xAxis': {
				'type': 'category',
				'data': [],
				'name': '日期时间',
				'nameTextStyle': {
					'fontWeight': 600,
					'fontSize': 18
				}
			},
			'yAxis': {
				'type': 'value',
				'name': '水位',
				'nameTextStyle': {
					'fontWeight': 600,
					'fontSize': 18
				}
			},
			'label': {},
			'tooltip': {'trigger': 'item'},
			'series': []
		},
        'flow': {
			'legend': {'type': 'scroll', 'top': 10, 'data': []},
            'dataZoom': [
				{'startValue': 1, 'type': 'slider', 'xAxisIndex': [0]},
				{'startValue': 1, 'type': 'slider', 'yAxisIndex': [0]}
			],
			'xAxis': {
				'type': 'category',
				'data': [],
				'name': '日期时间',
				'nameTextStyle': {
					'fontWeight': 600,
					'fontSize': 18
				}
			},
			'yAxis': {
				'type': 'value',
				'name': '流量',
				'nameTextStyle': {
					'fontWeight': 600,
					'fontSize': 18
				}
			},
			'label': {},
			'tooltip': {'trigger': 'item'},
			'series': []
		}
	}

	for site in datas:
		if len(datas[site]) == max_len:
			data['level']['xAxis']['data'] = list(datas[site].keys())
			data['flow']['xAxis']['data'] = list(datas[site].keys())
			break

	for site in datas:
		data['level']['legend']['data'].append(site)
		data['flow']['legend']['data'].append(site)

		s_item = {
			'name': site,
			'data': [],
			'type': 'line'
		}
		s_item['data'] = [
			datas[site][datatime][0] if datatime in datas[site] else 'NaN'
			for datatime in data['level']['xAxis']['data']
		]
		data['level']['series'].append(s_item)

		s_item1 = {
			'name': site,
			'data': [],
			'type': 'line'
		}
		s_item1['data'] = [
			datas[site][datatime][1] if datatime in datas[site] else 'NaN'
			for datatime in data['flow']['xAxis']['data']
		]
		data['flow']['series'].append(s_item1)

	js_file = open(js_path + 'data.js', 'w', encoding='utf-8')
	js_file.write('var level=' + json.dumps(data['level'], ensure_ascii=False) + '\n')
	js_file.write('var flow=' + json.dumps(data['flow'], ensure_ascii=False) + '\n')
	js_file.close()


if __name__ == '__main__':
	output()
