import json
import os

os.system('rdb --command json dump.rdb > temp_json_2.json')

with open('temp_json_2.json') as data_file:
    tmp_data = json.load(data_file)[0]

for item in tmp_data:
    if isinstance(tmp_data[item], unicode):
        tmp_data[item] = json.loads(tmp_data[item])

with open('dump.json', 'w') as df:
    json.dump(tmp_data, df)

os.system('rm temp_json_2.json')