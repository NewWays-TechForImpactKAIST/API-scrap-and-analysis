# coding=utf-8
import pandas as pd
import os
import warnings
from matplotlib import font_manager
from analysis.age.most_common_age_group import most_common_age_group
from analysis.age.hist_groups import cluster
from analysis.age import BasicArgument
from db.client import client

# 경고 무시
warnings.filterwarnings("ignore", category=FutureWarning)

BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
# matplotlib 한국어 폰트 설정
font_name = font_manager.FontProperties(
    fname=os.path.join(BASE_DIR, "_data", "NanumSquareL.ttf")
).get_name()

councilordict = {
    "시도의원": "metro_councilor",
    "광역의원비례대표": "metro_councilor",
    "구시군의회의원": "local_councilor",
    "기초의원비례대표": "local_councilor",
}

personDB = client["council"]

def run_by_excel(cluster_by, filenames, N=5, folder_name="To_be_filled"):
    assert cluster_by in ["sdName", "wiwName"]
    level = 1 if cluster_by == "sdName" else 2
    datadir = os.path.join(BASE_DIR, "_data", folder_name)
    df = pd.DataFrame()
    for d in filenames:
        df_new = pd.read_excel(os.path.join(datadir, d))
        df = pd.concat([df, df_new])
    if level == 1:
        df = df[["sgId", "sdName", "name", "age", "gender"]]
    else:
        df = df[["sgId", "sdName", "wiwName", "name", "age", "gender"]]
    df = df.sort_values(by="age")
    df["year"] = df["sgId"] // 10000
    is_elected = (
        True
        if "당선" in d
        else False
        if "후보" in d
        else ValueError("엑셀파일 이름에 '당선'이든지 '후보'가 있어야 합니다.")
    )
    councilorType = councilordict[d.split("[")[-1].split("]")[0]]
    for method in ["kmeans", "equal"]:
        basedic = BasicArgument(
            councilorType=councilorType,
            is_elected=is_elected,
            level=level,
            method=method,
        )
        cluster(df, N, basedic)
# def main(N=5):
#     run_by_excel("sdName", ["[당선][시도의원].xlsx", "[당선][광역의원비례대표].xlsx"])
#     run_by_excel("sdName", ["[후보][시도의원].xlsx", "[후보][광역의원비례대표].xlsx"])
#     run_by_excel("sdName", ["[당선][구시군의회의원].xlsx", "[당선][기초의원비례대표].xlsx"])
#     run_by_excel("sdName", ["[후보][구시군의회의원].xlsx", "[후보][기초의원비례대표].xlsx"])
#     run_by_excel("wiwName", ["[당선][구시군의회의원].xlsx", "[당선][기초의원비례대표].xlsx"])
#     run_by_excel("wiwName", ["[후보][구시군의회의원].xlsx", "[후보][기초의원비례대표].xlsx"])

def run_by_mongo(cluster_by, is_elected, councilorType, N=5):
    assert cluster_by in ["sdName", "wiwName"]
    level = 1 if cluster_by == "sdName" else 2
    data = []
    if not is_elected:
        councilorType = councilorType + "_candidate"
    cursor = personDB[councilorType].find()
    if level == 1:
        for person in cursor:
            data.append({"year": person.get("year"), "sdName": person.get("sdName"), "name": person.get("name"),
                        "age": person.get("age"), "gender": person.get("gender")})
    else:
        for person in cursor:
            data.append({"year": person.get("year"), "sdName": person.get("sdName"), "wiwName": person.get("wiwName"),
                        "name": person.get("name"), "age": person.get("age"), "gender": person.get("gender")})

    df = pd.DataFrame(data)
    df = df.sort_values(by="age")

    for method in ["kmeans", "equal"]:
        basedic = BasicArgument(
            councilorType=councilorType,
            is_elected=is_elected,
            level=level,
            method=method,
        )
        cluster(df, N, basedic, clean_flag = True)

def main(N=5):
    # 세종시의 경우 어느 순간 승급하기 때문에 sdName을 먼저 해야, sdName이 cluster 시작 때 밀려도 괜챃다. (cluster 함수 참조)
    run_by_mongo("sdName", is_elected = True, councilorType = "metro_councilor")
    run_by_mongo("sdName", is_elected = False, councilorType = "metro_councilor")
    run_by_mongo("sdName", is_elected = True, councilorType = "local_councilor")
    run_by_mongo("sdName", is_elected = False, councilorType = "local_councilor")
    run_by_mongo("wiwName", is_elected = True, councilorType = "local_councilor")
    run_by_mongo("wiwName", is_elected = False, councilorType = "local_councilor")

main()
