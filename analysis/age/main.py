# coding=utf-8
import pandas as pd
import os
import warnings
from matplotlib import font_manager
from analysis.age.most_common_age_group import most_common_age_group
from analysis.age.hist_groups import cluster
from analysis.age import BasicArgument

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

def main(N=5, folder_name="To_be_filled"):
    ## TO-DO: excel말고 mongodb에서 받아오도록 합니다.
    ## 이 링크에 구현될 save_to_mongo함수 참고 : https://github.com/NewWays-TechForImpactKAIST/API-scrap-and-analysis//blob/bd817e9a15086d313d9615b2515a81e0dbd73850/API/utils.py#L34
    ## 1. 지역의회
    # cluster_by = input("구역을 나눌 기준을 입력해주세요 (sdName 즉 시/도 또는 wiwName 즉 기초단체단위): ")
    cluster_by = "wiwName"
    assert cluster_by in ["sdName", "wiwName"]
    level = 1 if cluster_by == "sdName" else 2
    datadir = os.path.join(BASE_DIR, "_data", folder_name)
    # for d in os.listdir(datadir):
        # xlsx 파일을 읽어옵니다.
        # if not d.endswith(".xlsx"):
        #     continue
    # df = pd.read_excel(os.path.join(datadir, d))
    # d = "[당선][시도의원].xlsx"
    d = "[당선][구시군의회의원].xlsx"
    df_1 = pd.read_excel(os.path.join(datadir, d))
    # d = "[당선][광역의원비례대표].xlsx"
    d = "[당선][기초의원비례대표].xlsx"
    df_2 = pd.read_excel(os.path.join(datadir, d))
    df = pd.concat([df_1, df_2])
    # 필요한 열만 추출합니다.
    if level == 1:
        df = df[["sgId", "sdName", "name", "age", "gender"]]
    else:
        df = df[["sgId", "sdName", "wiwName", "name", "age", "gender"]]
    df = df.sort_values(by="age")
    is_elected = (
        True
        if "당선" in d
        else False
        if "후보" in d
        else ValueError("엑셀파일 이름에 '당선'이든지 '후보'가 있어야 합니다.")
    )
    councilorType = councilordict[d.split('[')[-1].split(']')[0]]
    for method in ["kmeans", "equal"]:
        basedic = BasicArgument(councilorType=councilorType, is_elected=is_elected, level=level, method=method)
        cluster(
            df, N, basedic
        )
    ## 2. 광역의회


main()
