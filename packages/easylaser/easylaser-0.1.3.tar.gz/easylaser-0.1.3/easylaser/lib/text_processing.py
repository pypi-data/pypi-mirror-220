import logging
import sentencepiece as spm
import ftfy
#from mosestokenizer import MosesPunctuationNormalizer

# from transliterate import translit
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("preprocess")


def SPMApply(
    sentences,
    sp,
    lang="en",
    lower_case=True,
    descape=False,
    verbose=False,
):
    assert lower_case, "lower case is needed by all the models"
    if verbose:
        logger.info("SPM processing")
    #mosesPunctuationNormalizer = MosesPunctuationNormalizer(lang)
    sentences = [
        #mosesPunctuationNormalizer(ftfy.fix_text(s).lower()) for s in sentences
        ftfy.fix_text(s).lower() for s in sentences
    ]
    # line = translit(line, language_code=, reversed=True)
    # in 3.11 might need to do transformrf_sentences = [sp.EncodeAsPieces(sentence) for sentence in sentences]
    transformed_sentences = sp.EncodeAsPieces(sentences)

    return [" ".join([word for word in sentence]) for sentence in transformed_sentences]
