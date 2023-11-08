# coding=utf-8
import pandas as pd
import os
import warnings
from matplotlib import font_manager
from analysis.age.most_common_age_group import most_common_age_group
from analysis.age.hist_groups import cluster

# 경고 무시
warnings.filterwarnings("ignore", category=FutureWarning)

BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
# matplotlib 한국어 폰트 설정
font_name = font_manager.FontProperties(
    fname=os.path.join(BASE_DIR, "_data", "NanumSquareL.ttf")
).get_name()


def main():
    for folder_name in ["지선-당선", "지선-후보"]:
        for cluster_by in ["sdName", "wiwName"]:
            # folder_name = input("_data 내의 폴더 이름은 무엇인가요?")
            # cluster_by = input("구역을 나눌 기준을 입력해주세요 (sdName 즉 시/도 또는 wiwName 즉 기초단체단위): ")
            datadir = os.path.join(BASE_DIR, "_data", folder_name)
            outdir = os.path.join(
                BASE_DIR, "output", f"age_all_{cluster_by}", folder_name
            )

            for d in os.listdir(datadir):
                # xlsx 파일을 읽어옵니다.
                if not d.endswith(".xlsx"):
                    continue
                df = pd.read_excel(os.path.join(datadir, d))

                # 필요한 열만 추출합니다.
                df = df[["sdName", "wiwName", "name", "age", "gender"]]
                df = df.sort_values(by="age")
                year = d[7:11]
                # most_common_age_group(df, year)
                cluster(
                    df, year, 7, "kmeans", cluster_by, outdir, font_name, folder_name
                )
                cluster(
                    df, year, 7, "equal", cluster_by, outdir, font_name, folder_name
                )


main()