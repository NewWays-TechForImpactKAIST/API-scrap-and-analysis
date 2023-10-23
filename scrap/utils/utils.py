from scrap.utils.requests import get_soup


def getPartyList():
    """
    중앙선거관리위원회에서 제공하는 정당 목록을 가져옵니다.
    """
    url = "https://www.nec.go.kr/site/nec/ex/bbs/List.do?cbIdx=1239"
    soup = get_soup(url)
    table = soup.find("table", class_="list type2")
    partyList = []
    for tr in table.find("tbody").find_all("tr"):
        td = tr.find_all("td")
        if td[0].get_text(strip=True).split("<br>")[0] == "시도":
            continue
        # 더불어민주당(민주당, 더민주) 등은 약자가 괄호 안에 있다.
        partyList.append(td[0].get_text(strip=True).split("<br>")[0].split("(")[0])
    return partyList


if __name__ == "__main__":
    print(getPartyList())
