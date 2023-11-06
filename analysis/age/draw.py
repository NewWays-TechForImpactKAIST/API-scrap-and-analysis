import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt


def make_scatterplot(package):
    (
        outdir,
        total_population_count,
        year,
        df_age,
        n_clst,
        method,
        cluster_by,
        folder_name,
        colors,
        font_name,
    ) = package
    # 산점도로 클러스터링 결과를 시각화합니다.
    sns.set(style="whitegrid")  # Seaborn 스타일 설정 (선택적)
    plt.figure(figsize=(10, 6))  # 그림 크기 설정 (선택적)
    print(df_age)
    sns.scatterplot(data=df_age, x="age", y="area", palette="viridis")
    # 클러스터 중심 나이를 플롯에 추가합니다.
    for _, row in df_age.iterrows():
        area = row["area"]
        age = row["age"]
        print(age)
        plt.text(
            age,
            area,
            "{:.2f}".format(float(age)),
            fontsize=12,
            ha="right",
            fontname=font_name,
        )
    plt.xlabel("나이", fontname=font_name)
    plt.ylabel("지역", fontname=font_name)
    plt.yticks(fontname=font_name)
    plt.title(
        f"{folder_name}자 나이 분포 ({year})  <총 {total_population_count}명>",
        fontname=font_name,
    )
    # 그래프를 이미지 파일로 저장합니다.
    plt.savefig(
        os.path.join(outdir, method, f"clustering_result ({year}).png"), dpi=300
    )  # 파일 이름 및 해상도 설정 (선택적)
    plt.close()


def plot_eachgroup(df, n_clst, colors):
    minage = min(df["age"].min(), 20)
    maxage = max(df["age"].max(), 80)
    for i in range(n_clst):
        clst_data = df[df["cluster_label"] == i]
        sns.histplot(
            data=clst_data,
            x="age",
            kde=False,
            label=f"Cluster {i}",
            color=colors[i],
            element="step",
            bins=range(minage, maxage, 1),
        )
        # 몇 명인지 프린트하기
        print(f"Cluster {i}: {clst_data.shape[0]} people")
        # 그룹마다 몇 살인지 프린트하기
        print(f"Cluster {i}: {clst_data['age']}")


def make_hist(package):
    (
        outdir,
        df,
        year,
        area,
        n_clst,
        method,
        cluster_by,
        folder_name,
        colors,
        font_name,
    ) = package
    plt.figure(figsize=(10, 6))
    # 시각화
    # plot_young_and_old(yb_clst, ob_clst)
    plot_eachgroup(df, n_clst, colors)
    total_population_count = df[df[cluster_by] == area].shape[0]
    if cluster_by == "sdName":
        plt.title(
            f"{area} {folder_name}자 나이 분포 ({year})  <총 {total_population_count}명>",
            fontname=font_name,
        )
    elif cluster_by == "wiwName":
        sdName = df[df["wiwName"] == area]["sdName"].iloc[0]
        plt.title(
            f"{sdName} {area} {folder_name}자 나이 분포 ({year})  <총 {total_population_count}명>",
            fontname=font_name,
        )
    else:
        print("cluster_by를 sdName 또는 wiwName으로 설정해주세요.")
        return
    plt.xlabel("나이", fontname=font_name)
    plt.ylabel("인원 수", fontname=font_name)
    max_ppl_in_age = df["age"].value_counts().max()
    plt.yticks(np.arange(0, max(10, max_ppl_in_age), step=5), fontsize=12)
    plt.savefig(os.path.join(outdir, method, f"{year}-{area}.png"))
    plt.close()
    print(f"Saved ", os.path.join(outdir, method, f"{year}-{area}.png"))
