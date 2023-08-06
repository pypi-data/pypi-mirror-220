import sys
from pathlib import Path

import pytest
import torch
from fake_data import ENGLISH_SENTENCES, FRENCH_SENTENCES

sys.path.append(str(Path(__file__).parent.parent))
from easylaser import Laser


def test_cpu_working():
    laser = Laser(device="cpu")
    laser.start_encoder()
    assert laser.device == "cpu"
    result = laser.embed_sentences(ENGLISH_SENTENCES)
    laser.stop_encoder()
    assert result.shape == (len(ENGLISH_SENTENCES), 1024)


def test_align_test_sentences():
    with Laser(device="cpu") as laser:
        result = laser.align_sentences(["hello, my name is John"], ["bonjour, je m'appelle John"])
        assert result != []

def test_cpu_working_with_context_manager():
    with Laser(device="cpu") as laser:
        assert laser.device == "cpu"
        laser.embed_sentences(ENGLISH_SENTENCES)


def test_gpu_working():
    if torch.cuda.is_available():
        laser = Laser(device="cuda")
        laser.start_encoder()
        assert laser.device == "cuda"
        laser.embed_sentences(ENGLISH_SENTENCES)
        laser.stop_encoder()


def test_multi_gpu_working():
    if torch.cuda.is_available():
        laser = Laser(device=["cuda:0", "cuda:1"])
        laser.start_encoder()
        assert laser.device == ["cuda:0", "cuda:1"]
        laser.embed_sentences(ENGLISH_SENTENCES)
        laser.stop_encoder()


def test_align_sentences():
    laser = Laser(device="cpu")
    laser.start_encoder()
    result = laser.align_sentences(ENGLISH_SENTENCES, FRENCH_SENTENCES)
    laser.stop_encoder()
    assert result != []
    
def test_align_sentences_with_context_manager():
    with Laser(device="cpu") as laser:
        result = laser.align_sentences(ENGLISH_SENTENCES, FRENCH_SENTENCES)
        assert result != []
 
def test_align_sentences_with_context_manager_and_gpu():
    with Laser(device=["cuda:0", "cuda:1"]) as laser:
        result = laser.align_sentences(ENGLISH_SENTENCES, FRENCH_SENTENCES)
        assert result != []

