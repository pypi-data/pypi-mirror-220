import logging
import re
import math
import random

import numpy as np
import pandas as pd
from collections import Counter
from typing import Callable, Optional, Union, Literal, List
from pathlib import Path
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from textacy.extract.kwic import keyword_in_context

from .topic_modeler import TextProcessor

ZH_WEBSITES = ["Douban"]

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def read_jsonl_to_dataframe(*paths: Union[Path, str]) -> pd.DataFrame:
    """
    Read JSONL files into a single pandas DataFrame.

    Args:
        *paths (Union[Path, str]): The paths to the JSONL files.

    Returns:
        pd.DataFrame: The combined DataFrame containing the contents of all JSONL files.
    """
    full_df = pd.DataFrame()

    for path in paths:
        path = Path(path)
        if not path.exists():
            logging.error(f'"{path}" does not exist.')
            continue

        files = []
        if path.is_file():
            if path.suffix == ".jsonl":
                files = [path]
            else:
                logging.error(f'"{path}" is not a JSONL file.')
                continue
        elif path.is_dir():
            files = list(path.glob("*.jsonl"))
            if files == []:
                logging.error(f'"{path}" does not contain any JSONL files.')
                continue
        else:
            logging.error(f'"{path}" is neither a file nor a directory.')
            continue

        for file in files:
            df = pd.read_json(file, lines=True)
            full_df = pd.concat([full_df, df], ignore_index=True)

    return full_df


def get_column_types(df: pd.DataFrame) -> dict[str, str]:
    """
    Get the data types of each column in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame.

    Returns:
        dict[str, str]: A dictionary mapping column names to their data types.
    """
    column_types = {}

    df_types = df.applymap(type)

    for column in df.columns:
        unique_types = df_types[column].unique()

        unique_types = [t.__name__ for t in unique_types]

        column_types[column] = ", ".join(set(unique_types))

    return column_types


def clean_zh_noise(text: str) -> str:
    """
    Clean noise from Chinese text.

    Args:
        text (str): The input text.

    Returns:
        str: The cleaned text.
    """
    text = text.replace("\n", "")
    text = re.sub(r"\s+", "", text)
    text = re.sub(
        r"([。，！？#＄¥％＆＊＋－／：；（）＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟–—‘’‛“”„‟…‧﹏.])\1+",
        r"\1",
        text,
    )

    return text


def clean_en_noise(text: str) -> str:
    """
    Clean noise from English text.

    Args:
        text (str): The input text.

    Returns:
        str: The cleaned text.
    """
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(
        r"([!?#$%&'()*+,-./:;<=>@[\]^_`{|}~\'\"])\1+",
        r"\1",
        text,
    )

    return text


def clean_text_basic(
    row: pd.Series,
    zh_websites: List[str] = ZH_WEBSITES,
    clean_zh_noise=clean_zh_noise,
    clean_en_noise=clean_en_noise,
) -> str:
    """
    Clean the review text based on the language of the website.

    Args:
        row (pd.Series): The row of the DataFrame.
        zh_websites (List[str]): The list of Chinese websites (default=ZH_WEBSITES).
        clean_zh_noise (Callable): The function to clean Chinese noise (default=clean_zh_noise).
        clean_en_noise (Callable): The function to clean English noise (default=clean_en_noise).

    Returns:
        str: The cleaned review text.
    """
    review = row["review"]
    if row["website"] in zh_websites:
        return clean_zh_noise(review)
    else:
        return clean_en_noise(review)


def calculate_review_length(
    row: pd.Series, zh_websites: List[str] = ZH_WEBSITES
) -> int:
    """
    Calculate the length of the review text based on the language of the website.

    Args:
        row (pd.Series): The row of the DataFrame.
        zh_websites (List[str]): The list of Chinese websites (default=ZH_WEBSITES).

    Returns:
        int: The length of the review text.
    """
    if row["website"] in zh_websites:
        return len(row["review"])
    else:
        return len(re.findall(r"(?u)\b[\w-]+\b", row["review"]))


def calculate_rating_level(row: pd.Series) -> Optional[str]:
    """
    Calculate the rating level based on the rating ratio.

    Args:
        row (pd.Series): The row of the DataFrame.

    Returns:
        Optional[str]: The rating level.
    """
    rating_ratio = row["rating_ratio"]
    if (math.isnan(rating_ratio)) or (rating_ratio is None):
        return None
    elif rating_ratio >= 0.8:
        return "Good (>=8/10)"
    elif rating_ratio <= 0.4:
        return "Bad (<=4/10)"
    else:
        return "Ok (4~8/10)"


def calculate_like_level(row: pd.Series) -> Optional[str]:
    """
    Calculate the like level based on the like ratio.

    Args:
        row (pd.Series): The row of the DataFrame.

    Returns:
        Optional[str]: The like level.
    """
    like_ratio = row["like_ratio"]
    if (math.isnan(like_ratio)) or (like_ratio == None):
        return None
    elif like_ratio >= 0.8:
        return "Mostly Agree (>80%)"
    elif 0.5 < like_ratio < 0.8:
        return "Somewhat Agree (50%~80%)"
    elif 0.2 < like_ratio <= 0.5:
        return "Somewhat Disgree (20%~50%)"
    else:
        return "Mostly Disagree (<20%)"


def update_column(
    df: pd.DataFrame, apply_function: Callable, column_name: str, *args, **kwargs
) -> None:
    """
    Apply a function to update a column in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame.
        apply_function (Callable): The function to apply.
        column_name (str): The name of the column to update.
        *args: Additional positional arguments to pass to the function.
        **kwargs: Additional keyword arguments to pass to the function.
    """
    df[column_name] = df.apply(lambda row: apply_function(row, *args, **kwargs), axis=1)


def auto_basic_process(df: pd.DataFrame) -> None:
    """
    Perform automatic basic processing on a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to process.

    Note:
        This function modifies the DataFrame in-place.
    """
    update_column(df, clean_text_basic, column_name="review")
    update_column(df, calculate_review_length, column_name="review_length")
    update_column(df, calculate_rating_level, column_name="rating_level")
    update_column(df, calculate_like_level, column_name="like_level")


def auto_nlp_process(
    df: pd.DataFrame, processor: TextProcessor, language: str = Literal["zh", "en"]
) -> None:
    """
    Perform automatic NLP processing on a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        processor (TextProcessor): The TextProcessor instance.
        language (str): The language of the text ("zh" for Chinese, "en" for English).

    Note:
        This function modifies the DataFrame in-place.
    """
    if language == "zh":
        (
            df["tokens"],
            df["entities"],
            df["bigrams"],
            df["trigrams"],
            df["quadgrams"],
        ) = zip(*list(processor.process_zh(df["review"])))
    else:
        (
            df["tokens"],
            df["entities"],
            df["bigrams"],
            df["trigrams"],
            df["quadgrams"],
        ) = zip(*list(processor.process_en(df["review"])))


def create_tf_df(
    df: pd.DataFrame, column: str = "tokens", min_tf: int = 2
) -> pd.DataFrame:
    """
    Create a term frequency DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame.
        column (str): The column containing the tokens (default="tokens").
        min_tf (int): The minimum term frequency (default=2).

    Returns:
        pd.DataFrame: The term frequency DataFrame.
    """
    counter = Counter()
    df[column].map(counter.update)

    tf_df = pd.DataFrame.from_dict(counter, orient="index", columns=["tf"])
    tf_df = tf_df.query("tf >= @min_tf")
    tf_df.index.name = "object"

    return tf_df.sort_values("tf", ascending=False)


def create_idf_df(
    df: pd.DataFrame, column: str = "tokens", min_df: int = 2
) -> pd.DataFrame:
    """
    Create an inverse document frequency DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame.
        column (str): The column containing the tokens (default="tokens").
        min_df (int): The minimum document frequency (default=2).

    Returns:
        pd.DataFrame: The inverse document frequency DataFrame.
    """

    def update(objects):
        counter.update(set(objects))

    counter = Counter()
    df[column].map(update)

    idf_df = pd.DataFrame.from_dict(counter, orient="index", columns=["df"])
    idf_df = idf_df.query("df >= @min_df")
    idf_df["idf"] = np.log(len(df) / idf_df["df"]) + 0.1
    idf_df.index.name = "object"

    return idf_df.sort_values("idf", ascending=False)


def create_tfidf_df(
    df: pd.DataFrame, column: str = "tokens", min_tf: int = 2, min_df: int = 2
):
    """
    Create a TF-IDF DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame.
        column (str): The column containing the tokens (default="tokens").
        min_tf (int): The minimum term frequency (default=2).
        min_df (int): The minimum document frequency (default=2).

    Returns:
        pd.DataFrame: The TF-IDF DataFrame.
    """
    tf_df = create_tf_df(df=df, column=column, min_tf=min_tf)
    idf_df = create_idf_df(df=df, column=column, min_df=min_df)
    tfidf_df = pd.merge(tf_df, idf_df, on="object")
    tfidf_df["tfidf"] = tfidf_df["tf"] * tfidf_df["idf"]
    return tfidf_df


def wordcloud(
    freq: pd.Series, title: str = None, max_words: int = 100, language: str = "en"
):
    """
    Generate and display a word cloud based on term frequencies.

    Args:
        freq (pd.Series): The term frequencies.
        title (str): The title of the word cloud (default=None).
        max_words (int): The maximum number of words to display (default=100).
        language (str): The language of the text ("en" for English, "zh" for Chinese).

    Note:
        This function displays the word cloud using matplotlib.pyplot.
    """
    if language == "zh":
        font_path = "fonts/SourceHanSerifK-Light.otf"
        wc = WordCloud(
            font_path=font_path,
            width=800,
            height=400,
            background_color="black",
            colormap="Paired",
            max_font_size=150,
            max_words=max_words,
        )
    else:
        wc = WordCloud(
            width=800,
            height=400,
            background_color="black",
            colormap="Paired",
            max_font_size=150,
            max_words=max_words,
        )

    counter = Counter(freq.fillna(0).to_dict())

    wc.generate_from_frequencies(counter)
    plt.figure()
    plt.title(title)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")


def KWIC(*args, **kwargs):
    """
    Perform keyword-in-context (KWIC) analysis.

    Args:
        *args: Positional arguments to pass to keyword_in_context.
        **kwargs: Keyword arguments to pass to keyword_in_context.

    Returns:
        Generator: A generator of KWIC results.
    """
    return keyword_in_context(
        *args, **{kw: arg for kw, arg in kwargs.items() if kw != "print_only"}
    )


def kwic(texts: pd.Series, keyword: str, window: int = 60, print_samples: int = 20):
    """
    Perform keyword-in-context (KWIC) analysis on a series of texts.

    Args:
        texts (pd.Series): The series of texts.
        keyword (str): The keyword to search for.
        window (int): The window size around the keyword (default=60).
        print_samples (int): The number of random samples to print (default=20).
    """

    def add_kwic(text):
        kwic_list.extend(
            KWIC(text, keyword, ignore_case=True, window_width=window, print_only=False)
        )

    kwic_list = []
    texts.map(add_kwic)

    n = min(print_samples, len(kwic_list))
    print(f"{n} random samples out of {len(kwic_list)} " + f"contexts for '{keyword}':")

    for sample in random.sample(list(kwic_list), n):
        print(
            re.sub(r"[\n\t]", " ", sample[0])
            + " "
            + sample[1]
            + " "
            + re.sub(r"[\n\t]", " ", sample[2])
        )


def count_keywords(objects, keywords):
    """
    Count the occurrences of keywords in a list of objects.

    Args:
        objects: The list of objects.
        keywords: The list of keywords to count.

    Returns:
        List[int]: The counts of the keywords in the same order as the input keywords.
    """
    objects = [obj for obj in objects if obj in keywords]
    counter = Counter(objects)
    return [counter.get(k, 0) for k in keywords]


def count_keywords_by(
    df: pd.DataFrame, by: str, keywords: List[str], column: str = "tokens"
) -> pd.DataFrame:
    """
    Count the occurrences of keywords in a DataFrame grouped by a column.

    Args:
        df (pd.DataFrame): The DataFrame.
        by (str): The column to group by.
        keywords (List[str]): The list of keywords to count.
        column (str): The column containing the tokens (default="tokens").

    Returns:
        pd.DataFrame: The keyword counts grouped by the specified column.
    """
    df = df.reset_index()
    freq_matrix = df[column].apply(count_keywords, keywords=keywords)
    freq_df = pd.DataFrame.from_records(freq_matrix, columns=keywords)
    freq_df[by] = df[by]
    return freq_df.groupby(by=by).sum().sort_values(by)
