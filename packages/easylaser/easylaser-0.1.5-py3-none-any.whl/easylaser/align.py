import logging

logging.getLogger("faiss.loader").setLevel(logging.ERROR)

import faiss

from enum import Enum
import numpy as np


def match_sentences_with_best_neighbors(
    sentences_lang0,
    sentences_lang1,
    best_neighbors,
    scores,
    threshold_score,
    keep_bad_matched=False,
):
    """
    Only keep the best match for each sentence in lang1, and remplace the index of the sentences by the sentences themselves
    """
    result = []
    for i, (match_index, score) in enumerate(zip(best_neighbors, scores)):
        lang0_sentence = sentences_lang0[i]
        lang1_sentence = sentences_lang1[match_index]

        if score < threshold_score or any(
            match_index == best_neighbors[j] and scores[j] > score
            for j in range(len(best_neighbors))
        ):
            if keep_bad_matched:
                result.append((lang0_sentence, None, 0))
        else:
            result.append((lang0_sentence, lang1_sentence, score))

    return result


# more optimized version of match_sentences_with_best_neighbors (but less readable)
# need to be adapted to work with keep_bad_matched=False
# def match_sentences_with_best_neighbors(
#     sentences_lang0, sentences_lang1, best_neighbors, scores, keep_bad_matched=False
# ):
#     """
#     Only keep the best match for each sentence in lang1, and remplace the index of the sentences by the sentences themselves
#     """
#     matched_without_duplicates = []
#     # dict_best_neighbors: key: index lang1 sentence, index lang0 sentence
#     best_matched_for_lang_1 = {}
#     for index_lang0, sentence_lang0 in enumerate(sentences_lang0):
#         index_lang1 = best_neighbors[index_lang0]
#         if index_lang1 not in best_matched_for_lang_1:
#             matched_without_duplicates.append(
#                 (
#                     sentence_lang0,
#                     sentences_lang1[index_lang1],
#                     scores[index_lang0],
#                 )
#             )
#             best_matched_for_lang_1[index_lang1] = index_lang0
#         else:
#             if scores[best_matched_for_lang_1[index_lang1]] > scores[index_lang0]:
#                 # there is already a best match for lang1 sentence
#                 matched_without_duplicates.append((sentences_lang1[index_lang0], None, 0))
#             else:
#                 # this is a better match for lang1 sentence
#                 matched_without_duplicates.append(
#                     (
#                         sentence_lang0,
#                         sentences_lang1[index_lang1],
#                         scores[index_lang0],
#                     )
#                 )
#                 matched_without_duplicates[best_matched_for_lang_1[index_lang1]] = (
#                     sentences_lang1[best_matched_for_lang_1[index_lang1]],
#                     None,
#                     0,
#                 )
#                 best_matched_for_lang_1[index_lang1] = index_lang0
#     return matched_without_duplicates


class Margin(Enum):
    RATIO = "ratio"
    DISTANCE = "distance"
    ABSOLUTE = "absolute"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


def _score_margin(
    Dxy: np.ndarray,
    Ixy: np.ndarray,
    Ax: np.ndarray,
    Ay: np.ndarray,
    margin: str,
    k: int,
) -> np.ndarray:
    nbex = Dxy.shape[0]
    scores = np.zeros((nbex, k))
    for i in range(nbex):
        for j in range(k):
            jj = Ixy[i, j]
            a = Dxy[i, j]
            b = (Ax[i] + Ay[jj]) / 2
            if margin == Margin.RATIO.value:
                scores[i, j] = a / b
            else:  # distance margin
                scores[i, j] = a - b
    return scores


def score_knn(x: np.ndarray, y: np.ndarray, k: int, margin: str) -> np.ndarray:
    nbex, dim = x.shape
    # create index
    idx_x = faiss.IndexFlatIP(dim)
    idx_y = faiss.IndexFlatIP(dim)
    # L2 normalization needed for cosine distance
    faiss.normalize_L2(x)
    faiss.normalize_L2(y)
    idx_x.add(x)
    idx_y.add(y)
    if margin == Margin.ABSOLUTE.value:
        scores, indices = idx_y.search(x, 1)
    else:
        # return cosine similarity and indices of k closest neighbors
        Cos_xy, Idx_xy = idx_y.search(x, k)
        Cos_yx, Idx_yx = idx_x.search(y, k)

        # average cosines
        Avg_xy = Cos_xy.mean(axis=1)
        Avg_yx = Cos_yx.mean(axis=1)

        scores = _score_margin(Cos_xy, Idx_xy, Avg_xy, Avg_yx, margin, k)

        # find best
        best = scores.argmax(axis=1)
        indices = np.zeros((nbex, 1), dtype=np.int32)
        for i in range(nbex):
            indices[i] = Idx_xy[i, best[i]]
    return indices, scores


def get_best_neighbors(lang0_embeddings, lang1_embeddings, scoring_method):
    k = min(len(lang0_embeddings), 4)
    indices, scores = score_knn(
        lang0_embeddings,
        lang1_embeddings,
        4,
        scoring_method,
    )
    return indices.flatten().tolist(), scores.max(axis=1)
