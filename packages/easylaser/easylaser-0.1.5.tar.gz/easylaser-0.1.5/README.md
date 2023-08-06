# EasyLaser

This package is created to use simply [LASER](https://github.com/facebookresearch/LASER) from MetaAI to create embeddings. It uses list of string as input and returns list of numpy arrays as output instead of using files. It also does not require external tools to be installed. The package automatically downloads the required laser models.

## Get started

### Install with pip

```bash
pip install easylaser
```

### Build from source

```bash
git clone https://gitlab.com/linguacustodia/easylaser.git
cd easylaser
pip install .
```

### Simple embeddings creation

```python
from easylaser import Laser
sentences = ["This is a sentence", "this is another sentences."]
with Laser() as laser:
    embeddings = laser.embed_sentences(sentences=sentences)
```

By default, it will try to run on the first gpu if it's available, if you don't have a gpu it will switch back to CPU.

## Embeddings

So as we have seen you can use it with a context manager or without

```python
from easylaser import Laser
sentences = ["This is a sentence", "this is another sentences."]

# with context manager
with Laser() as laser:
    embeddings = laser.embed_sentences(sentences=sentences)

# without
laser = Laser()
laser.is_encoder_active() # return False
laser.start_encoder()
embeddings = laser.embed_sentences(sentences=sentences)
laser.is_encoder_active() # return True
laser.stop_encoder()
```

## Multi GPU

You can specify the hardware you want to run on :

```python
from easylaser import Laser

laser = Laser(device="cpu")
laser = Laser(device="cuda")
laser = Laser(device=["cuda:0", "cuda:1"])

```

If you specify multiple graphic card, the inference will be multi-processed, leading to speed gain.

CAUTION : There is know bug, see Issues below, with multiple graphic card, one of the parent function which use Laser should be called from `if __name__ == '__main__':`

From our test the relation between the number of gpu and the speed is sub-linear. If you have some ideas to improve the speed, please contact us.

## Alignement

### Embeddings and Alignement

```python

from datolaser import Laser
english_sentences = ["A cat","This is a sentence", "this is another sentences."]
french_sentences = ["C'est une phrase", "Un chat","c'est une autre phrase."]
with Laser() as laser:
    aligned_sentences = laser.align_sentences(
                    english_sentences,
                    french_sentences,
                    threshold_score = 0,
                    keep_bad_matched = False
                    )
```

Every sentences, below the threshold will be considered as bad_matched.

If keep_bad_matched is `True`, it keep sentence with no match as `(sentence_1, None,0)`, if set to `False` it removes them.

### Only alignement

You can use `align_with_embeddings` if you have embeddings and just want to align sentences

```
from easylaser import align_with_embeddings

align_with_embeddings(
    embeddings_lang0,
    embeddings_lang1,
    sentences_lang0,
    sentences_lang1,
    threshold_score=0,
    keep_bad_matched=False,
)
```

## Issues

- Because of an [issue](https://github.com/facebookresearch/fairseq/issues/5012) with faiss this package cannot go above pyhton 3.10.

- If you encounter the following error:

```
RuntimeError:
        An attempt has been made to start a new process before the
        current process has finished its bootstrapping phase.

        This probably means that you are not using fork to start your
        child processes and you have forgotten to use the proper idiom
        in the main module:

            if __name__ == '__main__':
                freeze_support()
                ...

        The "freeze_support()" line can be omitted if the program
        is not going to be frozen to produce an executable.
```

You might need to use this [strutucture](https://pytorch.org/docs/stable/notes/windows.html#multiprocessing-error-without-if-clause-protection) to used embed_sentences with multiple GPUs

```python
def main()
    # do something here

if __name__ == '__main__':
    main()
```

## Supported languages

### LASER2

The LASER2 model was trained on the following languages, so you don't need to specify a lang for these languages:

Afrikaans, Albanian, Amharic, Arabic, Armenian, Aymara, Azerbaijani, Basque, Belarusian, Bengali,
Berber languages, Bosnian, Breton, Bulgarian, Burmese, Catalan, Central/Kadazan Dusun, Central Khmer,
Chavacano, Chinese, Coastal Kadazan, Cornish, Croatian, Czech, Danish, Dutch, Eastern Mari, English,
Esperanto, Estonian, Finnish, French, Galician, Georgian, German, Greek, Hausa, Hebrew, Hindi,
Hungarian, Icelandic, Ido, Indonesian, Interlingua, Interlingue, Irish, Italian, Japanese, Kabyle,
Kazakh, Korean, Kurdish, Latvian, Latin, Lingua Franca Nova, Lithuanian, Low German/Saxon,
Macedonian, Malagasy, Malay, Malayalam, Maldivian (Divehi), Marathi, Norwegian (Bokmål), Occitan,
Persian (Farsi), Polish, Portuguese, Romanian, Russian, Serbian, Sindhi, Sinhala, Slovak, Slovenian,
Somali, Spanish, Swahili, Swedish, Tagalog, Tajik, Tamil, Tatar, Telugu, Thai, Turkish, Uighur,
Ukrainian, Urdu, Uzbek, Vietnamese, Wu Chinese and Yue Chinese.

It has also observed that the model seems to generalize well to other (minority) languages or dialects, e.g.

Asturian, Egyptian Arabic, Faroese, Kashubian, North Moluccan Malay, Nynorsk Norwegian, Piedmontese, Sorbian, Swabian, Swiss German or Western Frisian.

### LASER3

You can also use laser on other languages in the list laser3_langs in lib/constants.py by using the lang parameter.

```python
with Laser(lang="zul_Latn") as laser:
    embeddings = laser.embed_sentences(sentences=sentences)
```

You might have issue with Laser3, we haven't properly tested it as we don't need it.

## Remove models

If you want to delete laser models they are here, run :

```bash
rm -r $HOME/.cache/laser-models
```

## License

LASER is BSD-licensed, as found in the [`LICENSE`](LICENSE) file in the root directory of this source tree.
