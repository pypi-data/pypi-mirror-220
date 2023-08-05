import logging
import re
import sys
from collections import namedtuple
from pathlib import Path
from typing import Union

import numpy as np
import torch

from .laserLstmEncoder import LaserLstmEncoder
from .laserTransformerEncoder import LaserTransformerEncoder

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("embed")

SPACE_NORMALIZER = re.compile(r"\s+")
Batch = namedtuple("Batch", "srcs tokens lengths")


class SentenceEncoder:
    def __init__(
        self,
        model_path,
        max_sentences=None,
        max_tokens=None,
        spm_vocab=None,
        fp16=False,
        verbose=False,
        sort_kind="quicksort",
    ):
        self.verbose = verbose
        if self.verbose:
            logger.info(f"loading encoder: {model_path}")
        self.max_sentences = max_sentences
        logger.info("max_sentences: %s", self.max_sentences)
        self.max_tokens = max_tokens
        if self.max_tokens is None and self.max_sentences is None:
            self.max_sentences = 1
        state_dict = torch.load(model_path)
        if "params" in state_dict:
            self.encoder = LaserLstmEncoder(**state_dict["params"])
            self.encoder.load_state_dict(state_dict["model"])
            self.dictionary = state_dict["dictionary"]
            self.prepend_bos = False
            self.left_padding = False
        else:
            self.encoder = LaserTransformerEncoder(state_dict, spm_vocab)
            self.dictionary = self.encoder.dictionary.indices
            self.prepend_bos = state_dict["cfg"]["model"].prepend_bos
            self.left_padding = state_dict["cfg"]["model"].left_pad_source
        del state_dict
        self.bos_index = self.dictionary["<s>"] = 0
        self.pad_index = self.dictionary["<pad>"] = 1
        self.eos_index = self.dictionary["</s>"] = 2
        self.unk_index = self.dictionary["<unk>"] = 3

        if fp16:
            self.encoder.half()
        self.encoder.eval()
        self.sort_kind = sort_kind

    def _choose_encoder_device(self, device=None):
        """
        Choose device (CPU or GPU) for encoder. By default choose the first GPU avalaible is cpu is False.
        """
        cpu = device == "cpu"
        if cpu:
            device = None
        self.device = device
        self.use_cuda = torch.cuda.is_available() and not cpu
        if self.use_cuda:
            if self.verbose:
                logger.info("transfer encoder to GPU")
                if device is not None:
                    logger.info(f"device: {device}")
                else:
                    logger.info("Choosing default GPU device")
            self.encoder.cuda(self.device)

    def _process_batch(self, batch):
        tokens = batch.tokens
        lengths = batch.lengths
        if self.use_cuda:
            tokens = tokens.cuda(self.device)
            lengths = lengths.cuda(self.device)

        with torch.no_grad():
            sentemb = self.encoder(tokens, lengths)["sentemb"]
        embeddings = sentemb.detach().cpu().numpy()
        return embeddings

    def _tokenize(self, line):
        tokens = SPACE_NORMALIZER.sub(" ", line).strip().split()
        ntokens = len(tokens)
        if self.prepend_bos:
            ids = torch.LongTensor(ntokens + 2)
            ids[0] = self.bos_index
            for i, token in enumerate(tokens):
                ids[i + 1] = self.dictionary.get(token, self.unk_index)
            ids[ntokens + 1] = self.eos_index
        else:
            ids = torch.LongTensor(ntokens + 1)
            for i, token in enumerate(tokens):
                ids[i] = self.dictionary.get(token, self.unk_index)
            ids[ntokens] = self.eos_index
        return ids

    def _make_batches(self, lines):
        tokens = [self._tokenize(line) for line in lines]
        lengths = np.array([t.numel() for t in tokens])
        indices = np.argsort(-lengths, kind=self.sort_kind)

        def batch(tokens, lengths, indices):
            toks = tokens[0].new_full((len(tokens), tokens[0].shape[0]), self.pad_index)
            if not self.left_padding:
                for i in range(len(tokens)):
                    toks[i, : tokens[i].shape[0]] = tokens[i]
            else:
                for i in range(len(tokens)):
                    toks[i, -tokens[i].shape[0] :] = tokens[i]
            return (
                Batch(srcs=None, tokens=toks, lengths=torch.LongTensor(lengths)),
                indices,
            )

        batch_tokens, batch_lengths, batch_indices = [], [], []
        ntokens = nsentences = 0
        for i in indices:
            if nsentences > 0 and (
                (self.max_tokens is not None and ntokens + lengths[i] > self.max_tokens)
                or (self.max_sentences is not None and nsentences == self.max_sentences)
            ):
                yield batch(batch_tokens, batch_lengths, batch_indices)
                ntokens = nsentences = 0
                batch_tokens, batch_lengths, batch_indices = [], [], []
            batch_tokens.append(tokens[i])
            batch_lengths.append(lengths[i])
            batch_indices.append(i)
            ntokens += tokens[i].shape[0]
            nsentences += 1
        if nsentences > 0:
            yield batch(batch_tokens, batch_lengths, batch_indices)

    def encode_sentences(self, sentences):
        indices = []
        results = []
        for batch, batch_indices in self._make_batches(sentences):
            indices.extend(batch_indices)
            results.append(self._process_batch(batch))
        return np.vstack(results)[np.argsort(indices, kind=self.sort_kind)]


def load_model(
    encoder_path: str,
    spm_model: str,
    verbose=False,
    **encoder_kwargs,
) -> SentenceEncoder:
    if spm_model:
        spm_vocab = str(Path(spm_model).with_suffix(".cvocab"))
        if verbose:
            logger.info(f"spm_model: {spm_model}")
            logger.info(f"spm_cvocab: {spm_vocab}")
    else:
        spm_vocab = None
    return SentenceEncoder(
        encoder_path, spm_vocab=spm_vocab, verbose=verbose, **encoder_kwargs
    )
