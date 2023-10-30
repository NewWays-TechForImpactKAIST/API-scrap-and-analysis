# coding=utf-8
import pandas as pd
import os
import warnings
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
from matplotlib import font_manager, rc

# 경고 무시
warnings.filterwarnings("ignore", category=FutureWarning)

BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
datadir = os.path.join(BASE_DIR, "_data")
outdir = os.path.join(BASE_DIR, "output")

# 폰트 경로를 rcParams에 설정합니다.
plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 기호 표시 설정

for d in os.listdir(datadir):
    # xlsx 파일을 읽어옵니다.
    if not d.endswith(".xlsx"):
        continue
    df = pd.read_excel(os.path.join(datadir, d))

    # 필요한 열만 추출합니다.
    df = df[["sdName", "name", "age"]]

    # 나이를 기반으로 그룹을 만듭니다.
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

    # 각 구역의 나이 평균을 계산합니다.
    average_age_by_region = df.groupby("sdName")["age"].mean()

    # 결과를 출력합니다.
    print(average_age_by_region)

    # K-means 클러스터링을 위한 데이터를 준비합니다.
    data_for_clustering = df[["age"]]

    # 클러스터의 개수 설정
    n_clusters = 5  # 원하는 클러스터 개수를 지정합니다.

    # K-means 모델을 초기화하고 학습합니다.
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(data_for_clustering)

    # 각 데이터 포인트가 속한 클러스터를 나타내는 레이블을 가져옵니다.
    cluster_labels = kmeans.labels_

    # 클러스터 중심 나이를 계산합니다.
    cluster_centers_age = []
    for i in range(n_clusters):
        cluster_data = df[cluster_labels == i]
        cluster_center_age = round(cluster_data["age"].mean(), 2)  # 나이를 소수점 2자리까지 반올림
        cluster_centers_age.append(cluster_center_age)

    # 결과를 출력합니다.
    print(cluster_centers_age)

    # 클러스터링 결과로 얻은 레이블을 데이터프레임에 추가합니다.
    df["cluster_label"] = cluster_labels

    # 클러스터 중심 위치를 가져옵니다.
    cluster_centers = kmeans.cluster_centers_

    # 클러스터링 결과로부터 각 데이터 포인트와 클러스터 중심 간의 거리를 계산합니다.
    distances = pairwise_distances(data_for_clustering, cluster_centers)

    # 각 클러스터에서 가장 가까운 데이터의 인덱스를 찾습니다.
    closest_data_indices = distances.argmin(axis=1)

    # 각 클러스터에서 가장 가까운 데이터의 수를 세어 출력합니다.
    for cluster_label in range(n_clusters):
        closest_data_count = sum(df["cluster_label"] == cluster_label)
        print(
            f"Cluster {cluster_label}: Age {cluster_centers_age[cluster_label]}, {closest_data_count} closest data points"
        )

    # 산점도로 클러스터링 결과를 시각화합니다.
    sns.set(style="whitegrid")  # Seaborn 스타일 설정 (선택적)
    plt.figure(figsize=(10, 6))  # 그림 크기 설정 (선택적)

    sns.scatterplot(
        data=df, x="age", y="sdName", hue="cluster_label", palette="viridis"
    )

    # 클러스터 중심 나이를 플롯에 추가합니다.
    for i, age in enumerate(cluster_centers_age):
        plt.text(age, i, f"Cluster {i}: {age:.2f}", fontsize=12, ha="right")

    plt.xlabel("나이")
    plt.ylabel("지역")
    plt.title("K-means 클러스터링 결과")
    plt.legend(title="클러스터")
    # 그래프를 이미지 파일로 저장합니다.
    pngpath = os.path.join(outdir, "clustering_result.png")
    plt.savefig(pngpath, dpi=300)  # 파일 이름 및 해상도 설정 (선택적)

    break
