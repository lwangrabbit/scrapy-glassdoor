# -*- coding:utf-8 -*-

import time
import logging


ERROR = 'MY_INTER_ERROR'


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "cookie": "gdId=f64d2f17-c492-45b4-a1af-3b2617d15f7e; trs=https%3A%2F%2Fcn.bing.com%2F:SEO:SEO:2018-06-03+03%3A02%3A45.381:undefined:undefined; ARPNTS=2875566272.64288.0000; ARPNTS_AB=323; _ga=GA1.2.695594756.1528020167; __qca=P0-578821465-1528020171692; cto_lwid=6813cc15-609c-4744-9bb3-619acaa4ecc5; _mibhv=anon-1528020405980-6482900678_6890; ki_r=; uc=8F0D0CFA50133D96DAB3D34ABA1B873349553F05C1B918562134523F91615591AEC27D25F9D026E941F1883F2DEDEFD14DD2EEBAC5BE1BE99D4A64B2C79989410B6C30C8C47402366C83032C0E7FF7260A622C2AB14D7A9CF053FC675D005A43FC662B4915981B20C32A037C14390578D03C2B553E04C0457B9218495C206342F95F092D2A815BB1B37B9AC298C0AE67EEAB644D28BEA0248479CCE39E7856FA; ab.storage.userId.bbafb5ff-3006-4aaf-bbe3-179521353526=%7B%22g%22%3A%2242658486%22%2C%22c%22%3A1529330894889%2C%22l%22%3A1529330894889%7D; ab.storage.deviceId.bbafb5ff-3006-4aaf-bbe3-179521353526=%7B%22g%22%3A%2255ce00d6-8c94-5c77-7d08-3339848a64cd%22%2C%22c%22%3A1529330894906%2C%22l%22%3A1529330894906%7D; rm=a2FpZmVuZy5qaWFuZ0BnbWFpbC5jb206MTU2MTQ5MTc4NzQ2MTo2YzZhMzYzMzYyN2Q1YjI1YjcxMzhhZTA4YTkwNjljZg; __gdpopuc=1; _gid=GA1.2.1277069287.1530545092; ki_t=1529300660386%3B1530719806407%3B1530719806407%3B2%3B4; ht=%7B%22quantcast%22%3A%5B%22D%22%5D%7D; JSESSIONID_JX_APP=259BE0B66C12AE4FB44B036E9403CE54; ARPNTS-JX=1063626944.64288.0000; ab.storage.sessionId.bbafb5ff-3006-4aaf-bbe3-179521353526=%7B%22g%22%3A%22e68dcddf-21c0-c989-102d-74c798cec128%22%2C%22e%22%3A1531040187918%2C%22c%22%3A1531037381829%2C%22l%22%3A1531038387918%7D; JSESSIONID=3860379BA3DC09120EF1356644502F4B; _uac=00000164799735e48c2a37445f72ce85; GSESSIONID=3860379BA3DC09120EF1356644502F4B; cass=1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }


cookie = {
    'gdId': 'f64d2f17-c492-45b4-a1af-3b2617d15f7e',
    'trs': 'https%3A%2F%2Fcn.bing.com%2F:SEO:SEO:2018-06-03+03%3A02%3A45.381:undefined:undefined',
    'ARPNTS': '2875566272.64288.0000',
    'ARPNTS_AB': '323',
    '_ga': 'GA1.2.695594756.1528020167',
    '__qca': 'P0-578821465-1528020171692',
    'cto_lwid': '6813cc15-609c-4744-9bb3-619acaa4ecc5',
    '_mibhv': 'anon-1528020405980-6482900678_6890',
    'ki_r': '',
    'uc': '8F0D0CFA50133D96DAB3D34ABA1B873349553F05C1B918562134523F91615591AEC27D25F9D026E941F1883F2DEDEFD14DD2EEBAC5BE1BE99D4A64B2C79989410B6C30C8C47402366C83032C0E7FF7260A622C2AB14D7A9CF053FC675D005A43FC662B4915981B20C32A037C14390578D03C2B553E04C0457B9218495C206342F95F092D2A815BB1B37B9AC298C0AE67EEAB644D28BEA0248479CCE39E7856FA',
    'ab.storage.userId.bbafb5ff-3006-4aaf-bbe3-179521353526': '%7B%22g%22%3A%2242658486%22%2C%22c%22%3A1529330894889%2C%22l%22%3A1529330894889%7D',
    'ab.storage.deviceId.bbafb5ff-3006-4aaf-bbe3-179521353526': '%7B%22g%22%3A%2255ce00d6-8c94-5c77-7d08-3339848a64cd%22%2C%22c%22%3A1529330894906%2C%22l%22%3A1529330894906%7D',
    'rm': 'a2FpZmVuZy5qaWFuZ0BnbWFpbC5jb206MTU2MTQ5MTc4NzQ2MTo2YzZhMzYzMzYyN2Q1YjI1YjcxMzhhZTA4YTkwNjljZg',
    '__gdpopuc': '1',
    '_gid': 'GA1.2.1277069287.1530545092',
    'ki_t': '1529300660386%3B1530719806407%3B1530719806407%3B2%3B4',
    'ht': '%7B%22quantcast%22%3A%5B%22D%22%5D%7D',
    'JSESSIONID_JX_APP': '259BE0B66C12AE4FB44B036E9403CE54',
    'ARPNTS-JX': '1063626944.64288.0000',
    'ab.storage.sessionId.bbafb5ff-3006-4aaf-bbe3-179521353526': '%7B%22g%22%3A%22e68dcddf-21c0-c989-102d-74c798cec128%22%2C%22e%22%3A1531040187918%2C%22c%22%3A1531037381829%2C%22l%22%3A1531038387918%7D',
    'JSESSIONID': '3860379BA3DC09120EF1356644502F4B',
    '_uac': '00000164799735e48c2a37445f72ce85',
    'GSESSIONID': '3860379BA3DC09120EF1356644502F4B',
    'cass': '1'
}


logging.basicConfig(filename='spider_url.log', filemode="w", level=logging.INFO)


def loggerInfo(log_str):
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print '%s: %s' % (time_str, log_str)
    logging.info('%s: %s' % (time_str, log_str))

