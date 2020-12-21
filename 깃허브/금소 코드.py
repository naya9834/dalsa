import requests
import json
import datetime

vilage_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?"

service_key = 'cXLuSMw5cHouRWF%2FTgayzwkB6IORmmjZe5siIC7P%2Bj1KCueBLD7Y1uu8JQrcit8F1r2Kkg3%2FXIuaCjYzHs5n%2Bg%3D%3D' 

today = datetime.datetime.today()
base_date = today.strftime("%Y%m%d") # "20200214" == 기준 날짜
base_time = "0800" # 날씨 값

nx = "60"
ny = "128"

payload = "serviceKey=" + service_key + "&" +\
    "dataType=json" + "&" +\
    "base_date=" + base_date + "&" +\
    "base_time=" + base_time + "&" +\
    "nx=" + nx + "&" +\
    "ny=" + ny

# 값 요청
res = requests.get(vilage_weather_url + payload)

items = res.json().get('response').get('body').get('items')
#{'item': [{'baseDate': '20201221',
#   'baseTime': '0500',
#   'category': 'POP',
#   'fcstDate': '20201221',
#   'fcstTime': '0900',
#   'fcstValue': '0',
#   'nx': 60,
#   'ny': 128},
#  {'baseDate': '20201221',
#   'baseTime': '0500',
#   'category': 'PTY',
#   'fcstDate': '20201221',
#   'fcstTime': '0900',
#   'fcstValue': '0',
#   'nx': 60,
#   'ny': 128},
#      'ny': 128},
#     {'baseDate': '20201221'

data = dict()
data['date'] = base_date

weather_data = dict()
for item in items['item']:
    # 기온
    if item['category'] == 'T3H':
        weather_data['tmp'] = item['fcstValue']
    
    # 기상상태
    if item['category'] == 'PTY':
        
        weather_code = item['fcstValue']
        
        if weather_code == '1':
            weather_state = '비'
        elif weather_code == '2':
            weather_state = '비/눈'
        elif weather_code == '3':
            weather_state = '눈'
        elif weather_code == '4':
            weather_state = '소나기'
        elif weather_state=='5':
            weather_state=='햇빛'
        else:
            weather_state = '없음'
        
        weather_data['code'] = weather_code
        weather_data['state'] = weather_state

data['weather'] = weather_data
data['weather']
# {'code': '0', 'state': '없음', 'tmp': '9'} # 9도 / 기상 이상 없음

rain_clothes="반바지, 가디건, 남방"
snow_clothes="니트, 모피소재"
sunny_clothes="푸른계열옷, 흰색옷"


#네이버 인증
#https://developers.naver.com/apps
#해당 사이트에서 로그인 후 "Cliend ID"와 "Client Secrete"을 얻어오기.
ncreds={
    "client_id":"<naya9834>",
    "client_secret":"<kimbokyung1!>"
}
nheaders={
    "X-Naver-Client-Id" : ncreds.get('client_id'),
    "X-Naver_Client_Secret": ncreds.get('client_secret')
}

# 경우 1 : 비/눈/소나기   =>날씨에 따라 옷 추천
# 경우 2 : 정상           =>리뷰 많은 순 옷 코디 추천

#weather_state
if data.get('weather').get('code') !='0':
    weather_state='1'

else:
    weather_state= '2'

import random
#random.sample(x,k=len(x)) 무작위로 리스트 섞기

clothes_list=None

#경우 1,2
if weather_state== '1':
    clothes_list=random.sample(rain_clothes, k=len(rain_clothes))
else:
    clothes_list=['']
clothes_list
#['니트','남방','푸른계열색상의 옷', '반바지', '흰색옷']

import urllib
# urllib.parse.quote(query) URL에서 검색어를 인코딩하기 위한 라이브러리

# 네이버 지역 검색 주소
naver_local_url = "https://openapi.naver.com/v1/search/local.json?"

# 검색에 사용될 파라미터
# 정렬 sort : 리뷰순(comment)
# 검색어 query : 인코딩된 문자열
params_format = "sort=comment&query="

# 위치는 사용자가 사용할 지역으로 변경가능
location = "경기"

# 추천된 옷을 담을 리스트
recommands = []
for clothes in clothes_list:
    # 검색어 지정
    query = location + " " + clothes + " 옷추천"
    # 지역검색 요청 파라메터 설정
    params = "sort=comment" \
              + "&query=" + query \
              + "&display=" + '5'
    
    # 검색
    # headers : 네이버 인증 정보
    res = requests.get(naver_local_url + params, headers=nheaders)
    
    # 옷추천 검색 결과
    result_list = res.json().get('items')

    # 경우 3 처리
    # 옷추천 결과에서 가장 상위 3개를 가져옴
    if weather_state == '3':
        for i in range(0,3):
            recommands.append(result_list[i])
        break
    
    # 경우 1,2 처리
    # 해당 옷추천 검색 결과에서 가장 상위를 가져옴
    if result_list:
        recommands.append(result_list[0])
        # 3개를 찾았다면 검색 중
        if len(recommands) >= 3:
            break


 # recommands
[{'title': '눈 오는날 옷추천',
  'link': 'https://smartstore.naver.com/urbana/products/5193653931?NaPm=ct%3Dkivjmvz4%7Cci%3D352daf9f9833be5412184fe31782a759e4e6bce6%7Ctr%3Dslsl%7Csn%3D1064485%7Chk%3D21fcfc719dbc979ef53189bd486f9bc66bcde2e1',
  'category': '옷추천>여성의류',
  'description': '',
  'telephone': '010-8633-7238',
  'address': '서울특별시 강동구 천중로56길 61(뉴현대맨숀)가동 101호',
  'mapx': '312677',
  'mapy': '556720'},
 {'title': '비 오는 날 옷추천',
  'link': 'https://smartstore.naver.com/famoustore/products/2050560065?NaPm=ct%3Dkivji34w%7Cci%3D01c48ed30abed8cf3eff3c1853655c6ab63078a1%7Ctr%3Dslsl%7Csn%3D425184%7Chk%3D8a96dbcb56814175688cb904e2dc64fd9a9b3b76',
  'category': '옷추천>여성의류',
  'description': '',
  'telephone': '0507-1453-1610',
  'address': '서울특별시 강서구 화곡로 186-36 1층 102호',
  'mapx': '312675',
  'mapy': '556993'},
 {'title': '햇빛 강한 날 옷추천',
  'link': 'https://smartstore.naver.com/banpobrother/products/2605240859?NaPm=ct%3Dkivjs9nc%7Cci%3D90101923f39e7700b7010c4805fb31ee973ce610%7Ctr%3Dslct%7Csn%3D575041%7Chk%3Dda85155e616183169b24fe67c247b825c52baad2#scrollY=undefined',
  'category': '옷추천>여성의류',
  'description': '',
  'telephone': '010-2457-3790',
  'address': '서울특별시 서초구 신반포로 27-6(반포아파트, 한신종합상가)한신종합상가 D-5호',
  'mapx': '312616',
  'mapy': '556799'}]

with open("kakao_code.json","r") as fp:
    tokens=json.load(fp)

#카카오톡 인증
#https://developers.kakao.com/docs/restapi/tool
#해당 사이트에서 로그인 후 'Access token'을 얻어온다.
kcreds={
    "access_token": tokens['access_token']
}
kheaders={
    "Authorization":"Bearer"+kcreds.get('access_token')
}

import json

# 카카오톡 URL 주소
kakaotalk_template_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

# 날씨 상세 정보 URL
weather_url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EB%82%A0%EC%94%A8"

# 날씨 정보 만들기 
text = f"""\
#날씨 정보 ({data['date']})
기온 : {data['weather']['tmp']}
기우  : {data['weather']['state']}
미세먼지 : {data['dust']['PM10']['value']} {data['dust']['PM10']['state']}
초미세먼지 : {data['dust']['PM2.5']['value']} {data['dust']['PM2.5']['state']}
"""

# 텍스트 템플릿 형식 만들기
template = {
  "object_type": "text",
  "text": text,
  "link": {
    "web_url": weather_url,
    "mobile_web_url": weather_url
  },
  "button_title": "날씨 상세보기"
}

# JSON 형식 -> 문자열 변환
payload = {
    "template_object" : json.dumps(template)
}

# 카카오톡 보내기
res = requests.post(kakaotalk_template_url, data=payload, headers=kheaders)

if res.json().get('result_code') == 0:
    print('메시지를 성공적으로 보냈습니다.')
else:
    print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(res.json()))

# 리스트 템플릿 형식 만들기
contents = []
template = {
    "object_type" : "list",
    "header_title" : "현재 날씨에 따른 옷 추천",
    "header_link" : {
        "web_url": weather_url,
        "mobile_web_url" : weather_url
    },
    "contents" : contents,
    "buttons" : [
        {
            "title" : "날씨 정보 상세보기",
            "link" : {
                "web_url": weather_url,
                "mobile_web_url" : weather_url
            }
        }
    ],
}

# contents 만들기
for clothes in recommands:
    title = clothes.get('title')  # 찾고자하는 옷
    # title : 눈 오는날 옷추천
    title = title.replace('<b>','').replace('</b>','')
    
    category = clothes.get('category')  # 옷 카테고리
    telephone = clothes.get('telephone')  # 옷쇼핑몰 전화번호
    address = clothes.get('address')  # 옷쇼핑몰 지번 주소

    # 각 장소를 클릭할 때 네이버 검색으로 연결해주기 위해 작성된 코드
    enc_address = urllib.parse.quote(address + ' ' + title)
    query = "query=" + enc_address

    # 옷 카테고리가 여름옷이면 여름 이미지
    # 이외에는 여름을 제외한 이미지
    if '여름옷' in category:
        image_url = "https://blog.naver.com/mp5000/160351524"
    else:
        image_url = "https://blog.naver.com/chickkaeng1/220808255311"

# 전화번호가 있다면 제목과 함께 넣어줍니다.
    if telephone:
        title = title + "\ntel) " + telephone

    # 카카오톡 리스트 템플릿 형식에 맞춰줍니다.
    content = {
        "title": "[" + category + "] " + title,
        "description": ' '.join(address.split()[1:]),
        "image_url": image_url,
        "image_width": 50, "image_height": 50,
        "link": {
            "web_url": "https://search.naver.com/search.naver?" + query,
            "mobile_web_url": "https://search.naver.com/search.naver?" + query
        }
    }
    
    contents.append(content)

# JSON 형식 -> 문자열 변환
payload = {
    "template_object" : json.dumps(template)
}

# 카카오톡 보내기
res = requests.post(kakaotalk_template_url, data=payload, headers=kheaders)

if res.json().get('result_code') == 0:
    print('메시지를 성공적으로 보냈습니다.')
else:
    print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(res.json()))

    print('Hello')


