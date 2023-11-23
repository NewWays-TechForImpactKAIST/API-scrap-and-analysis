# coding=utf-8
import os
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from matplotlib import cm
from analysis.age.draw import make_scatterplot, make_hist
from db.client import client


def plot_young_and_old(youngest_cluster, oldest_cluster):
    try:
        sns.histplot(
            data=youngest_cluster,
            x="age",
            kde=True,
            label="Youngest Cluster",
            color="blue",
            element="step",
            bins=range(
                youngest_cluster["age"].min(), youngest_cluster["age"].max() + 1, 1
            ),
        )
    except:
        pass
    try:
        sns.histplot(
            data=oldest_cluster,
            x="age",
            kde=True,
            label="Oldest Cluster",
            color="red",
            element="step",
            bins=range(oldest_cluster["age"].min(), oldest_cluster["age"].max() + 1, 1),
        )
    except:
        pass


def cluster_data(method, n_clst, df):
    clst_labels = []
    if method == "kmeans":
        ages_data = df[["age"]]
        # K-means 모델을 초기화하고 학습합니다.
        kmeans = KMeans(n_clusters=min(n_clst, len(ages_data)), random_state=0)
        kmeans.fit(ages_data)

        # 각 데이터 포인트가 속한 클러스터를 나타내는 레이블을 가져옵니다.
        clst_labels = kmeans.labels_
    elif method == "equal":
        clst_labels = np.repeat(np.arange(n_clst), len(df) // n_clst)
        clst_labels = np.append(clst_labels, np.arange(len(df) % n_clst))
        clst_labels.sort()
        clst_labels = np.array(clst_labels)
    df["cluster_label"] = clst_labels
    # 같은 나이는 같은 클러스터에 속하도록 합니다.
    # 0번 클러스터는 생기도록 합니다.
    for i in [0]:
        max_age = df[df["cluster_label"] == i]["age"].max()
        # when "age" == max_age, change "cluster_label" to be i
        df.loc[df["age"] == max_age, "cluster_label"] = i
    for i in range(2, n_clst):
        min_age = df[df["cluster_label"] == i]["age"].min()
        # when "age" == min_age, change "cluster_label" to be i
        df.loc[df["age"] == min_age, "cluster_label"] = i
    # (n_clst - 1)번 클러스터는 생기도록 합니다.
    if df[df["cluster_label"] == (n_clst - 1)]["age"].shape[0] == 0:
        for i in range(n_clst - 2, 0, -1):
            cluster_to_exchange = df[df["cluster_label"] == i]
            if not cluster_to_exchange.empty:
                df.loc[cluster_to_exchange.index, "cluster_label"] = n_clst - 1
                break

    return df


# 이름이 바뀐 경우
change_city_name = {
    ("충청남도", "당진군"): "당진시",
    ("경상남도", "마산시"): "창원시",
    ("경상남도", "진해시"): "창원시",
    ("경기도", "여주군"): "여주시",
    ("충청북도", "청원군"): "청주시",
    ("인천광역시", "남구"): "미추홀구",
}

#
change_lvl2to1 = {"연기군": "세종특별자치시"}


def change_local_name(sdName, wiwName):
    """
    1. 만약 '시' 와 '구'가 모두 wiwName에 있다면, '시' 까지만 쓰기
    ex) '용인시수지구' (선거 단위) -> '용인시' (의회 단위)
    2. 지역이 승급되면 이름 바꾸기
    ex) '당진군' (~2011) -> '당진시' (2012~)
    Keyword arguments:
    argument -- string
    Return: processed string
    """
    if (sdName, wiwName) in change_city_name:
        return change_city_name[(sdName, wiwName)]
    if "구" in wiwName and "시" in wiwName:
        return wiwName.split("시")[0] + "시"
    else:
        return wiwName


def local_to_metro_list(sdName, wiwName):
    """
    구시군에서 광역시/도로 승격한 경우
    """
    if wiwName in change_lvl2to1:
        print("change", wiwName, "to", change_lvl2to1[wiwName])
        return change_lvl2to1[wiwName]
    else:
        return sdName


def insert_data_to_mongo(
    dic, histdata, histcoll, localId=None, statdata=None, statcoll=None
):
    if localId is None:
        dic["data"] = histdata
        histcoll.insert_one(dic)
        if statdata is not None:
            print(statdata)
            dic["data"] = statdata
            statcoll.insert_one(dic)
    else:
        dic["localId"] = localId
        dic["data"] = histdata
        histcoll.insert_one(dic)
        if statdata is not None:
            print(statdata)
            dic["data"] = statdata
            statcoll.insert_one(dic)


def cluster(df, year, n_clst, method, cluster_by, outdir, font_name, folder_name):
    """구역별 그룹을 만듭니다.
    df: 데이터프레임
    year: 선거 연도
    n_clst: 그룹 수
    method: "kmeans" 또는 "equal"
    cluster_by: "sdName" (1단계) 또는 "wiwName" (2단계)
    outdir: 출력 디렉토리
    font_name: 폰트 이름
    folder_name: 출력 디렉토리의 하위 디렉토리 이름. 현재 '지선-당선' 또는 '지선-후보'.
                 결과가 mongodb등으로 옮겨가야 하므로, 사용하지 않도록 바꿔야 함.
    """
    os.makedirs(os.path.join(outdir, method), exist_ok=True)
    distdb = client["district"]
    statdb = client["stats"]
    metroIds = distdb["metro_district"]
    localIds = distdb["local_district"]
    histcoll = statdb["age_hist"]
    statcoll = statdb["age_stat"] # method = "equal"에서 써 줄 통계.
    councilorType = "elected" if folder_name[-2:] == "당선"\
        else "candidate" if folder_name[-2:] == "후보"\
        else ValueError("folder_name should end with '당선' or '후보'")
    level = 1 if cluster_by == "sdName" else 2
    basedic = {"councilorType": councilorType,
                "year": year,
                "level": level,
                "method": method,
                }
    # 기존 histogram 정보는 삭제 (나이별로 넣는 것이기 때문에 찌꺼기값 존재가능)
    histcoll.delete_many(basedic)
    if method == "equal":
        statcoll.delete_many(basedic)
    youngest_age = ("", 100)
    oldest_age = ("", 0)
    print(f"({year}), {n_clst} clusters")
    print(f"{'-' * 20}")
    # # Get a colormap for generating unique colors for clusters
    # colors = cm.rainbow(np.linspace(0, 1, n_clst))

    # wiwName을 처리합니다
    if level == 2:
        df["sdName"] = df[["sdName", "wiwName"]].apply(
            lambda x: local_to_metro_list(*x), axis=1
        )
        df["wiwName"] = df[["sdName", "wiwName"]].apply(
            lambda x: change_local_name(*x), axis=1
        )
    # # 데이터프레임에서 시도별로 묶은 후 나이 열만 가져옵니다.
    # df_age = pd.DataFrame(columns=["area", "age"])
    for area, df_clst in df.groupby(cluster_by):
        df_clst = cluster_data(method, n_clst, df_clst)
        # 클러스터 중심 나이를 계산합니다.
        clst_age_mean = []
        for i in range(n_clst):
            clst_data = df_clst[df_clst["cluster_label"] == i]
            # print(f"Cluster {i} in {area}: {clst_data['age'].min()} - {clst_data['age'].max()}")
            cluster_center_age = round(clst_data["age"].mean(), 2)  # 나이를 소수점 2자리까지 반올림
            clst_age_mean.append(cluster_center_age)
        clst_of_young = 0
        clst_of_old = n_clst - 1
        if method == "kmeans":
            clst_of_young = clst_age_mean.index(min(clst_age_mean))
            clst_of_old = clst_age_mean.index(max(clst_age_mean))
            clst_age_mean.sort()
            # new_data = pd.DataFrame({"area": area, "age": clst_age_mean})
            # df_age = pd.concat([df_age, new_data], ignore_index=True)
        elif method == "equal":
            # firstquintile is the oldest age in the cluster_label == 0
            # lastquintile is the youngest age in the cluster_label == n_clst - 1
            firstquintile = df_clst[df_clst["cluster_label"] == 0]["age"].max()
            lastquintile = df_clst[df_clst["cluster_label"] == n_clst - 1]["age"].min()
        # 지역의 가장 젊은, 나이든 그룹을 찾습니다
        yb_clst = df_clst[df_clst["cluster_label"] == clst_of_young]
        ob_clst = df_clst[df_clst["cluster_label"] == clst_of_old]
        print(f"Youngest in {area}: {yb_clst['age'].min()} - {yb_clst['age'].max()}")
        print(f"Oldest in {area}: {ob_clst['age'].min()} - {ob_clst['age'].max()}")
        # 그룹의 성비를 계산합니다.
        young_group_sexratio = (
            yb_clst[yb_clst["gender"] == "여"].shape[0] / yb_clst.shape[0]
        )
        old_group_sexratio = (
            ob_clst[ob_clst["gender"] == "여"].shape[0] / ob_clst.shape[0]
        )
        print(
            f"젊은 층의 성비는 여자가 {young_group_sexratio}, 노인층의 성비는 여자가 {old_group_sexratio}"
        )
        # 년도의 가장 젊은, 나이든 그룹이 있는 지역을 찾습니다
        if clst_age_mean[0] < youngest_age[1]:
            youngest_age = (area, clst_age_mean[0])
        if clst_age_mean[-1] > oldest_age[1]:
            oldest_age = (area, clst_age_mean[-1])
        # 히스토그램을 그립니다.
        histdata = [
            {
                "minAge": age,
                "maxAge": age + 1,
                "count": count,
                "ageGroup": age_group,
            }
            for age, count, age_group in zip(
                range(df_clst["age"].min(), df_clst["age"].max() + 1),
                df_clst.groupby("age").size(),
                df_clst.groupby("age")["cluster_label"].first(),
            )
        ]
        statdata = None
        if method == "equal":
            statdata = [
                {
                    "firstquintile": int(firstquintile),
                    "lastquintile": int(lastquintile),
                    "population": int(df_clst.shape[0]),
                }
            ]
        # 지역 id를 잘 설정해줍니다.
        metroname = df_clst["sdName"].iloc[0]
        metroId = metroIds.find_one({"sdName": metroname})["metroId"]
        if level == 1:
            print("sdName is ", metroname)
            dic = basedic.copy()
            dic["metroId"] = metroId
            insert_data_to_mongo(
                dic, histdata, histcoll, statdata=statdata, statcoll=statcoll
            )
        elif metroname in change_lvl2to1.values():
            print("sdName is ", metroname)
            dic = basedic.copy()
            dic["level"] = 1
            dic["metroId"] = metroId
            histcoll.delete_many(dic)  # 기존 정보를 삭제
            if method == "kmeans":
                insert_data_to_mongo(dic, histdata, histcoll)
            else:
                # l1statcoll = statcollection[
                #     folder_name + "_" + year + "_1level_" + method
                # ]
                statcoll.delete_many(dic)
                insert_data_to_mongo(
                    dic,
                    histdata,
                    histcoll,
                    statdata=statdata,
                    statcoll=statcoll,
                )
        else:
            localname = df_clst["wiwName"].iloc[0]
            print("sdName is ", metroname, "wiwName is", localname)
            localId = localIds.find_one({"sdName": metroname, "wiwName": localname})[
                "localId"
            ]
            dic = basedic.copy()
            dic["metroId"] = metroId
            insert_data_to_mongo(
                dic,
                histdata,
                histcoll,
                statdata=statdata,
                statcoll=statcoll,
                localId=localId,
            )

        # # 그리기
        # package = (
        #     outdir,
        #     df_clst,
        #     year,
        #     area,
        #     n_clst,
        #     method,
        #     cluster_by,
        #     folder_name,
        #     colors,
        #     font_name,
        # )
        # make_hist(package)

        print(f"Number of data points per cluster for {area}, method {method}")
        for cluster_label in range(n_clst):
            closest_data_count = sum(df_clst["cluster_label"] == cluster_label)
            print(
                f"Cluster {cluster_label}: Age {clst_age_mean[cluster_label]}, {closest_data_count} closest data points"
            )
    print(f"Youngest in {youngest_age[0]}: {youngest_age[1]}")
    print(f"Oldest in {oldest_age[0]}: {oldest_age[1]}")

    # # 그리기
    # package = (
    #     outdir,
    #     df.shape[0],
    #     year,
    #     df_age,
    #     n_clst,
    #     method,
    #     cluster_by,
    #     folder_name,
    #     colors,
    #     font_name,
    # )
    # make_scatterplot(package)
