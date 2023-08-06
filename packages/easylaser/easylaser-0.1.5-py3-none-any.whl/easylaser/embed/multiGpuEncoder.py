import numpy as np
import torch.multiprocessing as mp


def init_process(encoder, devices: list[int]):
    device = devices[mp.current_process()._identity[0] - 1]
    global sentenceEncoder
    sentenceEncoder = encoder
    sentenceEncoder._choose_encoder_device(device)


def _encode_sentences_one_gpu(sentences: list[str]):
    if sentences == []:
        return None
    return sentenceEncoder.encode_sentences(sentences)


def split(a, n):
    k, m = divmod(len(a), n)
    return [a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)]


# only work for laser sentence encoder
class MultiGpuEncoder:
    def __init__(self, devices: list[int], encoder):
        self.devices = devices
        ctx = mp.get_context("spawn")
        self.pool = ctx.Pool(
            len(self.devices),
            initializer=init_process,
            initargs=(encoder, self.devices),
        )

    def encode_sentences(self, sentences: list[str]):
        batchs = split(sentences, len(self.devices))
        results = self.pool.map(_encode_sentences_one_gpu, batchs)
        results = [result for result in results if result is not None]
        return np.concatenate(results)

    def __del__(self):
        # Worker Termination
        self.pool.terminate()
        self.pool.join()
