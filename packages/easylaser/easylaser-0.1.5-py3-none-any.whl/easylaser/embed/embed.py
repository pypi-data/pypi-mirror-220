#!/usr/bin/python3
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
# LASER  Language-Agnostic SEntence Representations
# is a toolkit to calculate multilingual sentence embeddings
# and to use them for document classification, bitext filtering
# and mining
#
# --------------------------------------------------------
#
# Tool to calculate to embed a text file
# The functions can be also imported into another Python code


import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional, Union

import numpy as np

from ..lib.text_processing import SPMApply
from .encoder import SentenceEncoder
from .multiGpuEncoder import MultiGpuEncoder

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("embed")


def EncodeTime(t):
    t = int(time.time() - t)
    if t < 1000:
        return "{:d}s".format(t)
    else:
        return "{:d}m{:d}s".format(t // 60, t % 60)


# Encode sentences (existing file pointers)
def EncodeText(encoder, sentences, fp16=False, verbose=False):
    t = time.time()
    # do I need a buffer ?
    if verbose:
        logger.info(f" - Beginning of the encoding")
    encoded = encoder.encode_sentences(sentences)
    if fp16:
        encoded = encoded.astype(np.float16)
    if verbose:
        logger.info(f"encoded {len(sentences)} sentences in {EncodeTime(t)}")
    return encoded


# Load existing embeddings
def EmbedLoad(fname, dim=1024, verbose=False):
    x = np.fromfile(fname, dtype=np.float32, count=-1)
    x.resize(x.shape[0] // dim, dim)
    if verbose:
        print(" - Embeddings: {:s}, {:d}x{:d}".format(fname, x.shape[0], dim))
    return x


# Get memory mapped embeddings
def EmbedMmap(fname, dim=1024, dtype=np.float32, verbose=False):
    nbex = int(os.path.getsize(fname) / dim / np.dtype(dtype).itemsize)
    E = np.memmap(fname, mode="r", dtype=dtype, shape=(nbex, dim))
    if verbose:
        print(" - embeddings on disk: {:s} {:d} x {:d}".format(fname, nbex, dim))
    return E


def embed_sentences(
    sentences: list[str],
    encoder: MultiGpuEncoder | SentenceEncoder = None,
    encoder_path: Path = None,
    sp = None,
    verbose: bool = False,
    buffer_size: int = 10000,
    max_sentences: Optional[int] = None,
    fp16: bool = False,
):
    if verbose:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.ERROR)
    assert encoder or encoder_path, "Provide initialised encoder or encoder_path"
    buffer_size = max(buffer_size, 1)
    assert (
        not max_sentences or max_sentences <= buffer_size
    ), "--max-sentences/--batch-size cannot be larger than --buffer-size"
    tSMP = time.time()
    sentences = SPMApply(sentences, sp)
    if verbose:
        logger.info(f" - Preprocessing finished at {time.time() - tSMP}")
    return EncodeText(encoder, sentences, fp16=fp16, verbose=verbose)
