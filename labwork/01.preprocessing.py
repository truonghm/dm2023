import pandas as pd
import numpy as np
import argparse

from typing import List, Dict, Optional

REVIEW_PATH = "../data/yelp_academic_dataset_review.json"


def read_data(path: str, nrows: Optional[int] = None) -> pd.DataFrame:
    with open(path, "r") as f:
        if nrows:
            return pd.read_json(f, orient="records", lines=True, nrows=nrows)
        else:
            return pd.read_json(f, orient="records", lines=True)


def count_words(corpus):
    """
    Count the number of words in a text
    """

    freqs = {}
    for doc in corpus:
        for word in doc:
            if word not in freqs:
                freqs[word] = 1
            else:
                freqs[word] += 1

    return freqs


def calculate_tfidf(
    corpus: List[str],
) -> Dict:
    tfidf = {}
    D = {}

    vocab = set([word for doc in corpus for word in doc])

    for word in vocab:
        for doc in corpus:
            if word in doc:
                if word not in D:
                    D[word] = 1
                else:
                    D[word] += 1

    for doc in corpus:
        for word in set(doc):
            if word not in tfidf:
                tf = doc.count(word) / len(doc)
                idf = np.log(len(corpus) / (1 + D[word]))
                tfidf[word] = tf * idf

    return tfidf


def process_data(
    nrows: Optional[int] = None,
    stopword_threshold: int = 0.02,
    freq_threshold: int = 30,
) -> List[str]:
    review_df = read_data(REVIEW_PATH, nrows)
    review_df["text_normalized"] = (
        review_df["text"]
        .str.lower()
        .str.replace(r"[^a-z0-9]+", " ", regex=True)
        .str.strip()
        .str.split()
    )
    vocab = count_words(review_df.text_normalized)
    vocab_df = pd.DataFrame.from_dict(vocab, orient="index").sort_values(
        by=0, ascending=False
    )
    vocab_df.columns = ["freq"]

    vocab_df["tfidf"] = vocab_df.index.map(
        calculate_tfidf(
            review_df.text_normalized,
        )
    )

    vocab_df.sort_values(by="tfidf", ascending=False, inplace=True)
    vocab_df["is_stopword"] = np.where(vocab_df.tfidf < stopword_threshold, True, False)

    describe_words = vocab_df[
        (~vocab_df.is_stopword) & (vocab_df.freq >= freq_threshold)
    ].index

    return list(describe_words)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-st",
        "--stopword_threshold",
        type=float,
        default=0.02,
        help="threshold for stopword",
    )
    parser.add_argument(
        "-ft", "--freq_threshold", type=int, default=30, help="threshold for frequency"
    )
    parser.add_argument(
        "-n", "--nrows", type=int, default=1000, help="limit rows for processing"
    )
    args = parser.parse_args()
    print(f"Processing data with args: {args.__dict__}")

    describe_words = process_data(
        stopword_threshold=args.stopword_threshold,
        freq_threshold=args.freq_threshold,
        nrows=args.nrows,
    )
    
    print("List of words that describe the restaurants are:", describe_words[:10])
    print("Saving describe words to ../data/describe_words.txt")
    with open("../data/describe_words.txt", "w") as f:
        f.write("\n".join(describe_words))
