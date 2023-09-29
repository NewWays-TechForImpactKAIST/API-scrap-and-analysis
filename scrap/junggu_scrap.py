# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

base_url = "https://02jgnew.council.or.kr"
link = "/kr/member/active"
full_url = base_url + link

response = requests.get(full_url, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')

profiles = soup.find_all('div', class_='profile')

for profile in profiles:
    name = profile.find('em', class_='name').text
    party = profile.find('ul', class_='dot').find('li').find_next_sibling('li').find('span').text
    
    # 프로필보기 링크 가져오기
    profile_link = profile.find('a', class_='start')
    if profile_link:
        profile_url = base_url + profile_link['href']
        
        # 프로필 페이지로 이동
        profile_response = requests.get(profile_url, verify=False)
        profile_soup = BeautifulSoup(profile_response.text, 'html.parser')
        
        # 프로필 페이지에서 원하는 정보를 추출하고 출력
        # 여기에서 필요한 정보를 추출하는 방법에 따라 코드를 작성해주세요.

        # print('이름:', name)
        # print('프로필 페이지 URL:', profile_url)
        # print('---')
        # "소속정당" 정보 추출
        party_info = profile_soup.find('em', text='소속정당 : ')
        party = party_info.find_next('span').string if party_info else '정당 정보 없음'

        print('이름:', name)
        print('정당:', party)


