import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
import os

from config import FILE_NAME

CURRENT_PATH = os.getcwd()

CSV_PATH = os.path.join(CURRENT_PATH, FILE_NAME)


def technologies_plot(df: DataFrame, limit: int) -> None:
    technologies = df["technologies"].str.split(", ", expand=True)
    technology_count = technologies.apply(pd.Series).stack().value_counts().head(limit)
    technology_count.plot(kind="bar", figsize=(10, 6), color="skyblue")
    plt.xticks(rotation=45, ha="right", va="top")
    plt.tight_layout()
    plt.savefig(os.path.join(CURRENT_PATH, "technologies"))


def english_level_pie(df: DataFrame) -> None:
    english = df["english"].value_counts()
    english.plot(kind="bar", figsize=(10, 6), color="skyblue")
    plt.xticks(rotation=0)
    plt.savefig(os.path.join(CURRENT_PATH, "english"))


def years_of_experience_plot(df: DataFrame) -> None:
    years = df["experience"].value_counts()
    years.plot(kind="bar", figsize=(10, 6), color="skyblue")
    plt.xticks(rotation=0)
    plt.savefig(os.path.join(CURRENT_PATH, "experience"))


def clean_location(df: DataFrame) -> DataFrame:
    df["location"] = df["location"].str.replace(",", "")
    df["location"] = df["location"].str.replace("(", "")
    df["location"] = df["location"].str.replace(")", "")
    return df


def location_plot(df: DataFrame, limit: int) -> None:
    df = clean_location(df)
    location = df["location"].str.split(" ", expand=True)
    location_count = location.apply(pd.Series).stack().value_counts().head(limit)
    location_count.plot(kind="bar", figsize=(10, 6), color="skyblue")
    plt.xticks(rotation=45, ha="right", va="top")
    plt.savefig(os.path.join(CURRENT_PATH, "location"))


if __name__ == "__main__":
    dataframe = pd.read_csv(CSV_PATH)
    technologies_plot(dataframe, 15)
    location_plot(dataframe, 10)
    years_of_experience_plot(dataframe)
    english_level_pie(dataframe)
