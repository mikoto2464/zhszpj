import random
import time

from utils import *
from curl_cffi import Session, CurlMime

print('福鼎一中 综合素质评价')

config = read_config()
session = Session(impersonate='chrome120')
session.cookies.set('JSESSIONID', config['session-id'])
session.cookies.set('SECKEY_ABVK', config['abvk-secret'])
session.cookies.set('BMAP_SECKEY', config['bmap-secret'])
session.cookies.set('Authorization', config['access-token'])

print(f'项目1: 班级活动:主题班会')
if input('确认提交(Y/N):').lower() == 'y':
    body = {
        'activityType': '主题班会',
        'activityLevel': '班级活动',
        '_': int(time.time() * 1000)
    }
    resp = session.get('http://fd.sxxdyzx.cn/dictionaryNew/getNameByType', params=body)
    objs = resp.json()['obj']
    for i in range(len(objs)):
        obj = objs[i]
        print(obj['activityName'])
        body = {
            'year': '2025-2026第一学期',
            'activityLevel': obj['activityLevel'],
            'activityType': obj['activityType'],
            'activityName': obj['activityName'],
            'activityNameOther': '',
            'role': '参与者',
            'beginTime': get_week_date(i),
            'endDate': get_week_date(i),
            'activityNum': '0.8',
            'description': '',
            'stuList': '{"stuData":[]}',
            'approval': obj['activityApproval'],
            'activityDicId': obj['aId'],
            'tid': obj['uid'],
            'status': '0',
        }
        filename = random.choice(config['class-img'])
        mp = CurlMime()
        with open(filename, 'rb') as f:
            file_content = f.read()
        if filename.split('.')[-1] == 'jpg' or filename.split('.')[-1] == 'jpeg':
            content_type = 'image/jpeg'
        elif filename.split('.')[-1] == 'png':
            content_type = 'image/png'
        else:
            raise FileNotFoundError(f'{filename}不适配')
        mp.addpart(
            name='file',
            filename=filename,
            content_type=content_type,
            data=file_content,
        )
        resp = session.post('http://fd.sxxdyzx.cn/activityNew/insertByStudentPC', data=body, multipart=mp)
        print(resp.json()['msg'])