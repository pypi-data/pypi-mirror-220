import numpy as np
import torch
import sentencepiece as spm

from .align import get_best_neighbors, match_sentences_with_best_neighbors
from .embed.embed import embed_sentences
from .embed.encoder import load_model
from .embed.multiGpuEncoder import MultiGpuEncoder
from .get_model import load_or_download_file
from .lib.constants import langs_with_specific_vocab, laser3_langs


def align_with_embeddings(
    embeddings_lang0,
    embeddings_lang1,
    sentences_lang0,
    sentences_lang1,
    threshold_score=0,
    keep_bad_matched=False,
    scoring_method="absolute"
):
    """
    Align sentences based on their embeddings
    :param threshold_score: minimum score to keep a match
    :param scoring_method: one of "absolute", "distance", "ratio". Absolute is the cosine similarity, see https://arxiv.org/pdf/1811.01136.pdf to have more details
    """
    best_neighbors, scores = get_best_neighbors(embeddings_lang0, embeddings_lang1, scoring_method=scoring_method)
    return match_sentences_with_best_neighbors(
        sentences_lang0,
        sentences_lang1,
        best_neighbors,
        scores,
        threshold_score,
        keep_bad_matched=keep_bad_matched,
    )


class Laser:
    """
    :param lang: only to be specified if using laser3, must be in laser3_langs. If None, will use laser2
    :param device: torch device to use for embedding, it can be "cpu", "cuda" or ["cuda:0", "cuda:1"] for multiprocessing
    :param verbose: if True, will print some information about the embedding process
    """

    def __init__(
        self,
        lang: str = None,
        device: list[str] | str = None,
        batch_size: int = 32,
        verbose=False,
    ):
        if device is None:
            if torch.cuda.is_available():
                device = "cuda"
            else:
                device = "cpu"
        self.set_lang(lang=lang)
        self.device = device
        self.batch_size = batch_size
        self.verbose = verbose
        self.encoder = None

    def __enter__(self):
        self.start_encoder()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_encoder()

    def stop_encoder(self):
        """
        Stop the encoder, free the GPU/CPU memory
        """
        del self.encoder

    def is_encoder_active(self):
        try:
            return not self.encoder is None
        except AttributeError:
            return False

    def start_encoder(self, device: list[str] | str = None, batch_size: int = None):
        """
        Start the encoder, you can overwrite the target_device and cpu parameters, else it will use the one specified at init
        :param target_device: ids of a GPU to use for embedding, if None, will use the first GPU available. If you want to use multiple GPUs, use launchMultiGpuEncoder
        :param cpu: if True, will use CPU for embedding and ignore target_devices
        """
        if device is not None:
            self.device = device
        if batch_size is not None:
            self.batch_size = batch_size

        multi_gpu = True if isinstance(self.device, list) else False
        self.encoder = self._load_encoder()
        if multi_gpu:
            self.encoder = MultiGpuEncoder(self.device, self.encoder)
        else:
            self.encoder._choose_encoder_device(device=self.device)

    def _load_encoder(
        self,
    ):
        version = 0
        if self.lang:
            version = 1
            pt = load_or_download_file(f"laser3-{self.lang}.v{version}.pt")
        else:
            pt = load_or_download_file("laser2.pt")
        if self.lang and self.lang in langs_with_specific_vocab:
            self.spm = load_or_download_file(
                f"laser3-{self.lang}.v{version}.spm"
            ).as_posix()
            load_or_download_file(f"laser3-{self.lang}.v{version}.cvocab")
        else:
            self.spm = str(load_or_download_file("laser2.spm").as_posix())
            load_or_download_file("laser2.cvocab")
        self.sp = spm.SentencePieceProcessor(model_file=self.spm)
        encoder = load_model(
            encoder_path=str(pt),
            spm_model=self.spm,
            verbose=self.verbose,
            max_sentences=self.batch_size,
        )
        return encoder

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def set_lang(self, lang: str):
        if lang and lang not in laser3_langs:
            raise ValueError(f"Language {lang} not supported")
        self.lang = lang

    def embed_sentences(self, sentences: list[str]) -> list[np.ndarray]:
        """
        :param sentences: list of sentences to embed
        :return: list of embeddings
        """
        if self.encoder is None:
            raise RuntimeError(
                "Encoder not started, please start it with start_encoder"
            )
        embeddings = embed_sentences(
            sentences=sentences,
            encoder=self.encoder,
            verbose=self.verbose,
            sp=self.sp,
        )
        return embeddings

    def align_sentences(
        self,
        sentences_lang0: list[str],
        sentences_lang1: list[str],
        threshold_score: float = 0,
        keep_bad_matched: bool = False,
    ) -> list[tuple[str, str, int]]:
        """
        Not compatible with laser3, if you want to use laser3 lang, use align_with_embeddings directly
        Align two lists of sentences using xSIM and the LASER embeddings
        :param sentences_lang0: list of sentences in lang0
        :param sentences_lang1: list of sentences in lang1
        :param threshold_score: if the score of the alignment is below this threshold, the alignment is considered bad
        :param keep_bad_matched: if True it keep sentence with no match as (sentence_1,None,0), if False it just removes them
        :return: list of tuples with at each time the lang0 sentence, the lang1 corresponding sentence and the alignment score. The order of sentences_lang0 is preserved.
        """
        embeddings_lang0 = self.embed_sentences(sentences=sentences_lang0)
        embeddings_lang1 = self.embed_sentences(sentences=sentences_lang1)
        return align_with_embeddings(
            embeddings_lang0,
            embeddings_lang1,
            sentences_lang0,
            sentences_lang1,
            threshold_score=threshold_score,
            keep_bad_matched=keep_bad_matched,
        )
