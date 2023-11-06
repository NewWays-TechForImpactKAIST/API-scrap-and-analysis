import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
datadir = os.path.join(BASE_DIR, "_data")
outdir = os.path.join(BASE_DIR, "output")

xls_names = [
    "5회 지선 (2010) [후보][구시군의회의원].xlsx",
    "6회 지선 (2014) [후보][구시군의회의원].xlsx",
    "7회 지선 (2018) [후보][구시군의회의원].xlsx",
    "8회 지선 (2022) [후보][구시군의회의원].xlsx",
]


def gini_simpson(data: pd.DataFrame, col_name: str) -> float:
    """주어진 데이터에 대해 지니-심슨 다양성 지표를 계산합니다."""
    each_cnt = data.groupby(col_name).size()
    total = each_cnt.sum()
    return 1.0 - sum(each_cnt * (each_cnt - 1) / total / (total - 1))


def simpson(data: pd.DataFrame, col_name: str) -> float:
    """주어진 데이터에 대해 심슨 다양성 지표를 계산합니다."""
    each_cnt = data.groupby(col_name).size()
    total = each_cnt.sum()
    return 1.0 - sum((each_cnt / total) ** 2)


def shannon_wiener(data: pd.DataFrame, col_name: str) -> float:
    """주어진 데이터에 대해 심슨 다양성 지표를 계산합니다."""
    each_cnt = data.groupby(col_name).size()
    total = each_cnt.sum()
    return sum(-each_cnt / total * np.log2(each_cnt / total))


def plot_diversity_trend(div_index: callable([[pd.DataFrame, str], float]), name: str):
    """제 5회 지선~제 8회 지선 후보자에 대해 다양성 지표의 변화를 보여줍니다."""
    party_indices = []
    gender_indices = []
    age_indices = []

    for xls_name in xls_names:
        print(f"{xls_name=}")
        df = pd.read_excel(os.path.join(datadir, xls_name))

        parties = df[["jdName"]]
        party_indices.append(div_index(parties, "jdName"))
        print(f"정당 다양성 지표: {party_indices[-1]:.3f}")

        genders = df[["gender"]]
        gender_indices.append(div_index(genders, "gender"))
        print(f"성별 다양성 지표: {gender_indices[-1]:.3f}")

        ages = (df[["age"]] // 10) * 10
        age_indices.append(div_index(ages, "age"))
        print(f"연령 다양성 지표: {age_indices[-1]:.3f}")

    plt.clf()

    plt.bar([4.8, 5.8, 6.8, 7.8], party_indices, width=0.2, label="party")
    plt.bar([5, 6, 7, 8], gender_indices, width=0.2, label="gender")
    plt.bar([5.2, 6.2, 7.2, 8.2], age_indices, width=0.2, label="age")

    plt.title(f"{name} Diversity Indices")
    plt.xlabel("Election")
    plt.ylabel("Diversity Index")
    plt.legend()

    pngpath = os.path.join(outdir, f"diversity_{name}.png")
    plt.savefig(pngpath, dpi=300)


if __name__ == "__main__":
    plot_diversity_trend(gini_simpson, "Gini-Simpson")
    plot_diversity_trend(simpson, "Simpson")
    plot_diversity_trend(shannon_wiener, "Shannon-Wiener")
