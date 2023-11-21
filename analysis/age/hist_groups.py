# coding=utf-8
import os
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from matplotlib import cm
from analysis.age.draw import make_scatterplot, make_hist


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
    return df


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
    youngest_age = ("", 100)
    oldest_age = ("", 0)
    print(f"({year}), {n_clst} clusters")
    print(f"{'-' * 20}")
    # Get a colormap for generating unique colors for clusters
    colors = cm.rainbow(np.linspace(0, 1, n_clst))

    # 데이터프레임에서 시도별로 묶은 후 나이 열만 가져옵니다.
    df_age = pd.DataFrame(columns=["area", "age"])
    for area, df_clst in df.groupby(cluster_by):
        df_clst = cluster_data(method, n_clst, df_clst)
        # 클러스터 중심 나이를 계산합니다.
        clst_age_mean = []
        for i in range(n_clst):
            clst_data = df_clst[df_clst["cluster_label"] == i]
            cluster_center_age = round(clst_data["age"].mean(), 2)  # 나이를 소수점 2자리까지 반올림
            clst_age_mean.append(cluster_center_age)

        clst_of_young = clst_age_mean.index(min(clst_age_mean))
        clst_of_old = clst_age_mean.index(max(clst_age_mean))
        clst_age_mean.sort()
        new_data = pd.DataFrame({"area": area, "age": clst_age_mean})
        df_age = pd.concat([df_age, new_data], ignore_index=True)
        print(clst_age_mean)

        yb_clst = df_clst[df_clst["cluster_label"] == clst_of_young]
        ob_clst = df_clst[df_clst["cluster_label"] == clst_of_old]
        print(f"Youngest in {area}: {yb_clst['age'].min()} - {yb_clst['age'].max()}")
        print(f"Oldest in {area}: {ob_clst['age'].min()} - {ob_clst['age'].max()}")
        if clst_age_mean[0] < youngest_age[1]:
            youngest_age = (area, clst_age_mean[0])
        if clst_age_mean[-1] > oldest_age[1]:
            oldest_age = (area, clst_age_mean[-1])

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
        data = [
            {
                "minAge": age,
                "maxAge": age + 1,
                "count": count,
                "ageGroup": age_group,
                "color": colors[age_group]
            }
            for age, count, age_group in zip(
                range(df_clst['age'].min(), df_clst['age'].max() + 1),
                df_clst.groupby('age').size(),
                df_clst.groupby('age')['cluster_label'].first()
            )
        ]

        # 그리기
        package = (
            outdir,
            df_clst,
            year,
            area,
            n_clst,
            method,
            cluster_by,
            folder_name,
            colors,
            font_name,
        )
        make_hist(package)

        print(f"Number of data points per cluster for {area}")
        for cluster_label in range(n_clst):
            closest_data_count = sum(df_clst["cluster_label"] == cluster_label)
            print(
                f"Cluster {cluster_label}: Age {clst_age_mean[cluster_label]}, {closest_data_count} closest data points"
            )
    print(f"Youngest in {youngest_age[0]}: {youngest_age[1]}")
    print(f"Oldest in {oldest_age[0]}: {oldest_age[1]}")

    # 그리기
    package = (
        outdir,
        df.shape[0],
        year,
        df_age,
        n_clst,
        method,
        cluster_by,
        folder_name,
        colors,
        font_name,
    )
    make_scatterplot(package)
