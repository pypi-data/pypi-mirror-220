import logging

logging.getLogger("fairseq.tasks.text_to_speech").setLevel(logging.ERROR)


from fairseq.data.dictionary import Dictionary
from fairseq.models.transformer import (
    Embedding,
    TransformerEncoder,
)
from fairseq.modules import LayerNorm


class LaserTransformerEncoder(TransformerEncoder):
    def __init__(self, state_dict, vocab_path):
        self.dictionary = Dictionary.load(vocab_path)
        if any(
            k in state_dict["model"]
            for k in ["encoder.layer_norm.weight", "layer_norm.weight"]
        ):
            self.dictionary.add_symbol("<mask>")
        cfg = state_dict["cfg"]["model"]
        self.sentemb_criterion = cfg.sentemb_criterion
        self.pad_idx = self.dictionary.pad_index
        self.bos_idx = self.dictionary.bos_index
        embed_tokens = Embedding(
            len(self.dictionary),
            cfg.encoder_embed_dim,
            self.pad_idx,
        )
        super().__init__(cfg, self.dictionary, embed_tokens)
        if "decoder.version" in state_dict["model"]:
            self._remove_decoder_layers(state_dict)
        if "layer_norm.weight" in state_dict["model"]:
            self.layer_norm = LayerNorm(cfg.encoder_embed_dim)
        self.load_state_dict(state_dict["model"])

    def _remove_decoder_layers(self, state_dict):
        for key in list(state_dict["model"].keys()):
            if not key.startswith(
                (
                    "encoder.layer_norm",
                    "encoder.layers",
                    "encoder.embed",
                    "encoder.version",
                )
            ):
                del state_dict["model"][key]
            else:
                renamed_key = key.replace("encoder.", "")
                state_dict["model"][renamed_key] = state_dict["model"].pop(key)

    def forward(self, src_tokens, src_lengths):
        encoder_out = super().forward(src_tokens, src_lengths)
        if isinstance(encoder_out, dict):
            x = encoder_out["encoder_out"][0]  # T x B x C
        else:
            x = encoder_out[0]
        if self.sentemb_criterion == "cls":
            cls_indices = src_tokens.eq(self.bos_idx).t()
            sentemb = x[cls_indices, :]
        else:
            padding_mask = src_tokens.eq(self.pad_idx).t().unsqueeze(-1)
            if padding_mask.any():
                x = x.float().masked_fill_(padding_mask, float("-inf")).type_as(x)
            sentemb = x.max(dim=0)[0]
        return {"sentemb": sentemb}
