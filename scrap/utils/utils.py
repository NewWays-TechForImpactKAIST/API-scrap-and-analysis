from scrap.utils.requests import get_soup

def getPartyList():
    url = 'https://www.nec.go.kr/site/nec/ex/bbs/List.do?cbIdx=1239'
    soup = get_soup(url)
    table = soup.find('table', class_='list type2')
    partyList = []
    for tr in table.find('tbody').find_all('tr'):
        td = tr.find_all('td')
        if td[0].get_text(strip=True).split("<br>")[0] == '시도':
            continue
        partyList.append(td[0].get_text(strip=True).split("<br>")[0])
    return partyList