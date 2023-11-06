# coding=utf-8
import pandas as pd


def most_common_age_group(df, d):
    """10년단위로 무리짓고 가장 사람 많은 무리 출력.
    df: 데이터프레임
    d: 파일 이름"""
    age_groups = pd.cut(
        df["age"],
        [0, 30, 40, 50, 60, 70, 80, 90, 100],
        labels=["0-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100"],
    )

    # 나이 그룹을 데이터프레임에 추가합니다.
    df["age_group"] = age_groups

    # 각 구역에서 가장 많은 나이 그룹을 찾습니다.
    most_common_age_group_by_region = df.groupby("sdName")["age_group"].agg(
        lambda x: x.mode().iloc[0]
    )

    # 결과를 출력합니다.
    print(d, most_common_age_group_by_region)
