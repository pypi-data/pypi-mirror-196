import json
import os
from datetime import datetime
from itertools import chain
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import pyspark.ml.feature as ml_feature
import pyspark.sql.functions as func
from loguru import logger
from pyarrow import parquet as pq
from pyspark.mllib.linalg import DenseVector
from pyspark.sql import DataFrame, SparkSession, Window
from scipy.sparse import csr_matrix, save_npz
from scipy.sparse.linalg import svds
from sklearn.feature_extraction.text import CountVectorizer


def days_to_seconds(days: int) -> int:
    return days * 86400


def join_lists(list_2d: List[List[str]]) -> List[str]:
    return list(chain(*list_2d))


WINDOW_CENTER_LABEL = "center"
WINDOW_BACKWARD_LABEL = "backward"


def _get_window(radius_in_days: float, window_orientation: str, backend: str):
    """Create the window context for the cooccurrence matrix, adapted for each
    backend: in days for pandas, in seconds for spark.

    Args:
        radius_in_days (float): _description_
        window_orientation (str): _description_
        backend (str): Either pandas or spark

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    if backend == "spark":
        # timesecond are necessary for the window function of spark
        radius_ = days_to_seconds(radius_in_days)
        # chose window orientation
    elif backend == "pandas":
        # radius_ = pd.to_timedelta(radius_in_days, unit="d")
        radius_ = radius_in_days
    if window_orientation == WINDOW_CENTER_LABEL:
        window_start = -radius_ / 2
        window_end = radius_ / 2
    elif window_orientation == WINDOW_BACKWARD_LABEL:
        window_start = -radius_
        window_end = 0
    else:
        raise ValueError(
            f"Choose window_orientation in {[WINDOW_CENTER_LABEL, WINDOW_BACKWARD_LABEL]}"
        )
    if backend == "spark":
        window_start = int(window_start)
        window_end = int(window_end)
    return window_start, window_end


def build_cooccurrence_matrix_pd(
    events: DataFrame,
    output_dir: str = None,
    radius_in_days: int = 30,
    window_orientation: str = "center",
    colname_concept: str = "event_source_concept_id",
) -> Tuple[np.array, np.array, Dict]:
    """
    Pandas method for building the cooccurrence matrix in-memory.

    Parameters
    ----------
    events : DataFrame
        _description_
    output_dir : str, optional
        _description_, by default None
    radius_in_days : int, optional
        _description_, by default 30
    window_orientation : str, optional
        _description_, by default "center"
    colname_concept : str, optional
        _description_, by default "event_source_concept_id"

    Returns
    -------
    Tuple[np.array, np.array, Dict]
        _description_
    """
    window_start, window_end = _get_window(
        radius_in_days=radius_in_days,
        window_orientation=window_orientation,
        backend="pandas",
    )
    window = window_end - window_start
    if window_orientation == WINDOW_CENTER_LABEL:
        center = True
    elif window_orientation == WINDOW_BACKWARD_LABEL:
        center = False
    else:
        raise ValueError(
            f"Choose window_orientation in {[WINDOW_CENTER_LABEL, WINDOW_BACKWARD_LABEL]}"
        )
    events_sorted = events.sort_values(["person_id", "start"])
    events_in_window = events_sorted.groupby("person_id")[
        [colname_concept, "start"]
    ].rolling(
        on="start", window=str(window) + "D", center=center, closed="both"
    )
    sep_tok = "<SEP>"
    windowed_events = [
        sep_tok.join(w.tolist()) for w in events_in_window[colname_concept]
    ]
    # TODO: we can do better than joining the word and then making the
    # countvectorizer split them. Eg. build a dummy analyzer that does nothing
    transformer = CountVectorizer(analyzer=lambda x: x.split(sep_tok))
    logger.info("Fit, transform events with count vectorizer model")
    sparse_counts = transformer.fit_transform(windowed_events)
    logger.info(f"Vocabulary of length {len(transformer.vocabulary_)}")
    encoder = transformer.vocabulary_
    decoder = transformer.get_feature_names()
    vocabulary_size = len(encoder.keys())
    # TODO: is it less efficient than a join ?
    context_encoded = (
        events_sorted[colname_concept].apply(lambda x: encoder[x]).values
    )
    n_words = sparse_counts.sum(axis=0)
    n_contexts = np.unique(context_encoded, return_counts=True)[1]
    # use ultra fast sparse matrix product
    rows = np.arange(len(context_encoded))
    cols = context_encoded
    values = np.ones(len(context_encoded))
    context_matrix = csr_matrix(
        (values, (rows, cols)),
        shape=(len(context_encoded), vocabulary_size),
    ).transpose()
    sparse_cooccurrence = context_matrix.dot(sparse_counts)
    # Have to withdraw the diagonal to avoid double counting
    cooccurrence_matrix = sparse_cooccurrence - csr_matrix(np.diag(n_contexts))
    if output_dir is not None:
        logger.info(
            f"Saving coocurrence_matrix, event_count and vocabulary at {output_dir}"
        )
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        path2matrix = str(Path(output_dir) / "sparse_matrix.npz")
        logger.info(f"Saving cooccurrence matrix as parquet at: {path2matrix}")
        save_npz(path2matrix, cooccurrence_matrix)
        with open(os.path.join(output_dir, "vocabulary.json"), "w") as file:
            json.dump(encoder, file)
        np.save(os.path.join(output_dir, "event_count.npy"), n_contexts)
    return cooccurrence_matrix, n_contexts, encoder


def build_cooccurrence_matrix_spark(
    events: DataFrame,
    output_dir: str = None,
    radius_in_days: int = 30,
    window_orientation: str = "center",
    matrix_type: str = "numpy",
    colname_concept: str = "event_source_concept_id",
) -> Tuple[np.array, np.array, Dict]:
    """
    Description: Leverage spark backend to compute cooccurrence matrix for an
    event table.

    :param events: event dataframe
    :param output_dir:
    :param radius_in_days: size of the context window in days, this is to be thought as the radius
    around the central word of reference. Depending of the orientation of the window, the size of
    window will be 2 * radius_in_days if centered
    :param window_orientation: choose position of the reference word in the context window:
        ['centered', 'future'], this changes the focus of the co-occurrence matrix.
        NB : The future configuration leads to an asymetric cooccurrence matrix.
    :param matrix_type:
    :return:
        - cooccurrence_matrix, matrix of cooccurrence of size VxV  where V is the vocabulary size
         with M[i, j] = #|i and j occurs in a window of size window_in_days|
        - event_count, array of size V with the number of single occurrence of each word
        - label2ix, dictionary of size V giving the correspondence between a word and its index in
        the matrix
    """

    window_start, window_end = _get_window(
        radius_in_days=radius_in_days,
        window_orientation=window_orientation,
        backend="spark",
    )
    # little hack of the rangeBetween function
    w = (
        Window.partitionBy("person_id")
        .orderBy(func.col("start").cast("long"))
        .rangeBetween(window_start, window_end)
    )
    events_in_window = events.withColumn(
        "cooccurrence", func.collect_list(func.col(colname_concept)).over(w)
    )

    codes_vectorizer = ml_feature.CountVectorizer(
        inputCol="cooccurrence", outputCol="cooccurrence_ohe", minDF=0
    )

    logger.info("Fit count vectorizer model")
    codes_vectorizer_model = codes_vectorizer.fit(events_in_window)
    logger.info(
        "Vocabulary of length {}".format(
            len(codes_vectorizer_model.vocabulary)
        )
    )
    logger.info("Transform events with count vectorizer model")
    events_ohe = codes_vectorizer_model.transform(events_in_window)
    label2ix = {
        label: i
        for (label, i) in zip(
            codes_vectorizer_model.vocabulary,
            range(len(codes_vectorizer_model.vocabulary)),
        )
    }
    # adding ix for future reduced key
    mapping_expr = func.create_map(
        [func.lit(x) for x in chain(*label2ix.items())]
    )
    events_ohe_with_ix = events_ohe.withColumn(
        "ix", mapping_expr.getItem(func.col(colname_concept)).cast("int")
    )
    # sort by item ix and get back raw counts (suppres
    # s item ignored by count vectorizer)
    event_count = np.array(
        events_ohe_with_ix.groupBy("ix")
        .count()
        .filter(~func.col("ix").isNull())
        .sort(func.col("ix"))
        .drop("ix")
        .collect()
    ).reshape(-1)

    # aggregate one line per item and sort by item index
    events_ohe_grouped = (
        events_ohe_with_ix.select("ix", "cooccurrence_ohe")
        .rdd.mapValues(lambda v: v.toArray())
        .reduceByKey(lambda x, y: x + y)
        .mapValues(lambda x: DenseVector(x))
        .toDF(["ix", "cooccurrence_ohe"])
    )
    # remove excluded code from count_vectorizer and sort by ix
    events_ohe_grouped_sorted = events_ohe_grouped.filter(
        ~func.col("ix").isNull()
    ).sort(func.col("ix").asc())
    # collect and reshape the cooccurrence matrix
    if matrix_type == "numpy":
        logger.info("Collect co-occurrence matrix as numpy")
        x_3d = np.array(
            events_ohe_grouped_sorted.select("cooccurrence_ohe").collect()
        )
        rows, idx, vocab_size = x_3d.shape
        # Have to withdraw the diagonal to avoid double counting
        cooccurrence_matrix = x_3d.reshape(rows, rows) - np.diag(event_count)

    elif matrix_type == "parquet":
        # user = os.getenv("USER")
        # hdfs_path +
        # hdfs_path = f"hdfs://bbsedsi/user/{user}/"
        spark = SparkSession.builder.getOrCreate()
        path2spark_matrix = str(output_dir) + "/spark_matrix.parquet"

        logger.info(f"Saving cooccurrence matrix at: {path2spark_matrix}")
        events_ohe_grouped_sorted.write.mode("overwrite").parquet(
            path2spark_matrix
        )
        logger.info(f"Saving event count at: {path2spark_matrix}")

        spark.createDataFrame(
            pd.DataFrame({"event_count": event_count})
        ).write.mode("overwrite").parquet(
            str(output_dir) + "/event_count.parquet"
        )
        # TODO: could ty to use [spark.ml.sparse to create sparse
        # matrix](https://spark.apache.org/docs/latest/mllib-dimensionality-reduction.html#svd-example)
        # https://spark.apache.org/docs/latest/api/java/org/apache/spark/ml/linalg/SparseMatrix.html

        # The cooccurrence matrix has to be sorted because it has been saved
        # with random row order depending on the workers.
        matrix_before_stacking = spark.read.parquet(path2spark_matrix).sort(
            "ix"
        )
        cooccurrence_matrix = np.vstack(
            matrix_before_stacking.toPandas()["cooccurrence_ohe"].values
        ) - np.diag(event_count)
    else:
        raise NotImplementedError(
            "Matrix collection should be either numpy or parquet"
        )

    if output_dir is not None:
        logger.info(
            f"Saving coocurrence_matrix, event_count and vocabulary at {output_dir}"
        )
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        with open(Path(output_dir) / "vocabulary.json", "w") as file:
            json.dump(label2ix, file)
        np.save(
            Path(output_dir) / "cooccurrence_matrix.npy",
            cooccurrence_matrix,
        )
        np.save(Path(output_dir) / "event_count.npy", event_count)
    return cooccurrence_matrix, event_count, label2ix


def sparse_to_array(v):
    """
    Description: udf to transform to dense vector spark sparse vector
    :param v:
    :return:
    """
    v = DenseVector(v)
    new_array = list([float(x) for x in v])
    return new_array


def build_ppmi(
    cooccurrence_matrix: np.array,
    event_count: np.array,
    smoothing_factor: float = 0.75,
    k: int = 1,
) -> np.array:
    """
    Description: Build the pmi matrix from the cooccurrence matrix M:
    $$pmi = log[\frac{p(w,c)}{p(w)p(c)}]$$
    # Take the raw item count as the Z denominator
    # We might try some large definition of context where we throws up from the denominator
    # all self-cooccurrence (ie windows of size 1 with an item alone)
    # Our lines/columns do not sum to 1 because we exclude the column where there are counts of
    # the line item co-occurring with the same occurrence of itself.
    # The diagonal corresponds only to co-occurrences of the item with a different occurrence of
    # itself.
    :param cooccurrence_matrix:
    :param item_count:
    :param smoothing_factor:
    :param k: shift value, default 1 which is log(1) = 0 shift.
    :return:
    """

    total_event_count = event_count.sum()
    cooccurrence_ratio = cooccurrence_matrix / total_event_count
    item_ratio = (event_count / total_event_count) ** smoothing_factor
    inverse_item_ratio = 1 / item_ratio
    pmi_matrix = np.log(
        cooccurrence_ratio * np.outer(inverse_item_ratio, inverse_item_ratio)
    )
    ppmi = pmi_matrix - np.log(k)
    ppmi[ppmi <= 0] = 0

    return ppmi


def build_embeddings(
    ppmi: np.array, d: int, window_orientation="center", sparse: bool = True
):
    """
    TODO should use pyspark.mlib if the matrix is too big for numpy
    Description: perform symetric singular value reconstruction
    :param window_orientation: choose position of the reference word in the context window:
        ['centered', 'future'], this changes the focus of the co-occurrence matrix.
        NB : The future configuration leads to an asymetric cooccurrence matrix.
    :param ppmi:
    :param d:
    :return:
    """
    if window_orientation == WINDOW_CENTER_LABEL:
        pass
    elif window_orientation == WINDOW_BACKWARD_LABEL:
        # TODO: I think that the symetrization is not necessary. A symmetric ppmi means word and context
        # embeddings are the same. We could use different ones.
        # Symetrization of the cooccurrence matrix
        ppmi = (ppmi + np.transpose(ppmi)) / 2
    else:
        raise ValueError(
            f"Choose window_orientation in {[WINDOW_CENTER_LABEL, WINDOW_BACKWARD_LABEL]}"
        )
    if d > ppmi.shape[0]:
        raise Exception(
            "Continuous vector dimension should be lower than vocabulary size!"
        )
    # TODO: Why not using [sklearn truncated
    # svd ?](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html)

    if sparse:
        sparse_ppmi = csr_matrix(ppmi)
        u_d, s_d, v_d = svds(sparse_ppmi, k=d)
    else:
        u, s, v = np.linalg.svd(ppmi)
        u_d = u[:, :d]
        v_d = v[:d, :]
        s_d = s[:d]
    embeddings = u_d.dot(np.diag(np.sqrt(s_d))) + v_d.transpose().dot(
        np.diag(np.sqrt(s_d))
    )

    return embeddings


def event2vec(
    events=DataFrame,
    output_dir: str = None,
    colname_concept: str = "event_source_concept_id",
    window_radius_in_days=30,
    window_orientation: str = "center",
    matrix_type: str = "numpy",
    backend="pandas",
    d: int = 300,
    smoothing_factor: float = 0.75,
    k: int = 1,
):
    """
    Wrapper around build_cooccurrence_matrix, build_ppmi and build_embeddings to
    create concept embeddings from raw event codes.

    Args:
        events (_type_, optional): _description_. Defaults to DataFrame.
        output_dir (str, optional): _description_. Defaults to None.
        colname_concept (str, optional): _description_. Defaults to
        "event_source_concept_id". window_radius_in_days (int, optional):
        _description_. Defaults to 30. window_orientation (str, optional):
        _description_. Defaults to "centered". matrix_type (str, optional):
        _description_. Defaults to "numpy". d (int, optional): _description_.
        Defaults to 300. smoothing_factor (float, optional): _description_.
        Defaults to 0.75. k (int, optional): _description_. Defaults to 1.

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    if backend == "spark":
        (
            cooccurrence_matrix,
            event_count,
            label2ix,
        ) = build_cooccurrence_matrix_spark(
            events,
            output_dir=output_dir,
            radius_in_days=window_radius_in_days,
            colname_concept=colname_concept,
            matrix_type=matrix_type,
        )
    elif backend == "pandas":
        (
            cooccurrence_matrix,
            event_count,
            label2ix,
        ) = build_cooccurrence_matrix_pd(
            events,
            output_dir=output_dir,
            radius_in_days=window_radius_in_days,
            colname_concept=colname_concept,
        )
    if window_orientation not in [WINDOW_BACKWARD_LABEL, WINDOW_CENTER_LABEL]:
        raise ValueError(
            f"Choose window_orientation in {[WINDOW_BACKWARD_LABEL, WINDOW_CENTER_LABEL]}"
        )
    t_0 = datetime.now()
    logger.info(
        f"Shape of the co-occurrence matrix: {cooccurrence_matrix.shape}"
    )
    logger.info(
        f"Build PPMI with smoothing factor {smoothing_factor} and shift {k}"
    )
    ppmi = build_ppmi(
        cooccurrence_matrix=cooccurrence_matrix,
        event_count=event_count,
        smoothing_factor=smoothing_factor,
        k=k,
    )
    logger.info("PPMI factorization with SVD")
    event_embeddings = build_embeddings(
        ppmi=ppmi, d=d, window_orientation=window_orientation
    )
    t_1 = datetime.now()
    logger.info(
        f"Embeddings of dimension {d} created from the co-occurrence matrix in {t_1 - t_0}"
    )
    embeddings_dict = dict(zip(label2ix.keys(), np.array(event_embeddings)))

    embeddings_df = pd.DataFrame.from_dict(embeddings_dict, orient="columns")
    if output_dir is not None:
        path2emb = (
            output_dir
            / f"tuto_snds2vec_alpha={smoothing_factor}_k={k}_d={d}.parquet"
        )
        logger.info(f"Saving embeddings as parquet dataframe at {path2emb}")
        embeddings_df.to_parquet(path2emb)
    return embeddings_df
