# coding=utf-8
# Source : https://www.data.go.kr/data/15000864/openapi.do#/tab_layer_detail_function
import requests
import xml.etree.ElementTree as ET
import pandas as pd

from mykey import serviceKey

base_url = 'http://apis.data.go.kr/9760000/WinnerInfoInqireService2/getWinnerInfoInqire'
params ={'serviceKey' : serviceKey,\
         'pageNo' : '1', 'numOfRows' : '10', 'sgId' : '20230405', 'sgTypecode' : '2', 'sdName' : '전라북도', 'sggName' : '전주시을', 'jdName' : ''}
page_no = 1
num_of_rows = 10000

parliamentVote = [20220601, 20230405]
sgCodes = input("Input the number of sgTypecode: ").split(',')
data_list = []
for sgId in parliamentVote:
    for code in sgCodes:
        params = {
            'serviceKey': serviceKey,
            'pageNo': str(page_no),
            'numOfRows': str(num_of_rows),
            'sgId': str(sgId),
            'sgTypecode': str(code),
            'sggName': '',
            'sdName': '',
            'jdName': ''
        }

        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Error: Unable to fetch data for page {page_no}")
            continue

        root = ET.fromstring(response.content)

        for item in root.findall(".//item"):
            sgId = item.find('sgId').text
            sggName = item.find('sggName').text
            sdName = item.find('sdName').text
            wiwName = item.find('wiwName').text
            giho = item.find('giho').text
            jdName = item.find('jdName').text
            name = item.find('name').text
            hanjaName = item.find('hanjaName').text
            gender = item.find('gender').text
            birthday = item.find('birthday').text
            age = item.find('age').text
            addr = item.find('addr').text
            jobId = item.find('jobId').text
            job = item.find('job').text
            eduId = item.find('eduId').text
            edu = item.find('edu').text
            career1 = item.find('career1').text
            career2 = item.find('career2').text
            # status = item.find('status').text

            data_list.append({
                'sgId': sgId,
                'sggName': sggName,
                'sdName': sdName,
                'wiwName': wiwName,
                'giho': giho,
                'jdName': jdName,
                'name': name,
                'hanjaName': hanjaName,
                'gender': gender,
                'birthday': birthday,
                'age': age,
                'addr': addr,
                'jobId': jobId,
                'job': job,
                'eduId': eduId,
                'edu': edu,
                'career1': career1,
                'career2': career2,
                # 'status': status
            })

# Create a DataFrame from the collected data
df = pd.DataFrame(data_list)

# Save the DataFrame to an Excel file
excel_file = '[당선][구시군의회의원].xlsx'
df.to_excel(excel_file, index=False)

print(f'Data has been saved to {excel_file}')