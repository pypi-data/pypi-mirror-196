from typing import Any, Dict, List, Tuple, Union

from ..core.transforms_interface import TextTransform
from ..corpora.corpus_types import Text
from .utils import split_text
from . import functional as F

__all__ = [
    "RandomDeletionWords",
    "RandomDeletionSentences",
    "RandomSwapWords",
    "RandomSwapSentences",
    "SynonymsReplacement",
]


class RandomDeletionWords(TextTransform):
    """Randomly deletes words in the input text.
    
    Args:
        deletion_prob (float): Probability of deleting a word. Default 0.1.
        min_words_each_sentence (float or int):
            If a `float`, then it is the minimum proportion of words to retain in each sentence after deletion.
            If an `int`, then it is the minimum number of words in each sentence. Default 5.
        p (float): Probability of applying the transform. Default: 0.5.
        
    Targets:
        text
    """

    def __init__(
        self,
        deletion_prob: float = 0.1,
        min_words_each_sentence: Union[float, int] = 5,
        ignore_first: bool = False,
        always_apply: bool = False, 
        p: float = 0.5
    ) -> None:
        super(RandomDeletionWords, self).__init__(ignore_first, always_apply, p)
        
        if not isinstance(min_words_each_sentence, (float, int)):
            raise TypeError(
                f"min_words_each_sentence must be either an int or a float. Got: {type(min_words_each_sentence)}"
            )
        if isinstance(min_words_each_sentence, float) and not (0.0 <= min_words_each_sentence <= 1.0):
            raise ValueError(
                f"If min_words_each_sentence is a float, it must be between 0 and 1. Got: {min_words_each_sentence}"
            )
        if isinstance(min_words_each_sentence, int) and min_words_each_sentence < 0:
            raise ValueError(
                f"If min_words_each_sentence is an int, it must be a non-negative. Got: {min_words_each_sentence}"
            )

        self.deletion_prob = deletion_prob
        self.min_words_each_sentence = min_words_each_sentence

    def apply(self, text: Text, **params: Any) -> Text:
        return F.delete_words(text, self.deletion_prob, self.min_words_each_sentence)

    def get_transform_init_args_names(self) -> Tuple[str, str]:
        return "deletion_prob", "min_words_each_sentence"
    
    
class RandomDeletionSentences(TextTransform):
    """Randomly deletes sentences in the input text.
    
    Args:
        deletion_prob (float): Probability of deleting a sentence. Default 0.1.
        min_sentences (float or int):
            If a `float`, then it is the minimum proportion of sentences to retain in the text after deletion.
            If an `int`, then it is the minimum number of sentences in the text. Default 3.
        p (float): Probability of applying the transform. Default: 0.5.
        
    Targets:
        text
    """

    def __init__(
        self,
        deletion_prob: float = 0.1,
        min_sentences: Union[float, int] = 3,
        ignore_first: bool = False,
        always_apply: bool = False, 
        p: float = 0.5
    ) -> None:
        super(RandomDeletionSentences, self).__init__(ignore_first, always_apply, p)
        
        if not isinstance(min_sentences, (float, int)):
            raise TypeError(f"min_sentences must be either an int or a float. Got: {type(min_sentences)}")
        if isinstance(min_sentences, float) and not (0.0 <= min_sentences <= 1.0):
            raise ValueError(f"If min_sentences is a float, it must be between 0 and 1. Got: {min_sentences}")
        if isinstance(min_sentences, int) and min_sentences < 0:
            raise ValueError(f"If min_sentences is an int, it must be a non-negative. Got: {min_sentences}")

        self.deletion_prob = deletion_prob
        self.min_sentences = min_sentences

    def apply(self, text: Text, min_sentences: Union[float, int] = 3, **params: Any) -> Text:
        return F.delete_sentences(text, self.deletion_prob, min_sentences)

    @property
    def targets_as_params(self) -> List[str]:
        return ["text"]

    def get_params_dependent_on_targets(self, params: Dict[str, Text]) -> Dict[str, Union[float, int]]:
        if isinstance(self.min_sentences, int):
            return {"min_sentences": self.min_sentences - self.ignore_first}

        # n: Length of original sentences (>= 2)
        # p: `min_sentences` ([0, 1))
        # q: The minimum proportion of sentences to retain in the text after deletion if `ignore_first` is True
        # If not `ignore_first`: the minimum number of sentences after deleting is n * p
        # If `ignore_first`: the minimum number of sentences after deleting is 1 + (n - 1)*q
        # So, n * p == 1 + (n - 1)*q, ===> q = (n*p - 1) / (n - 1)

        text = params["text"]
        num_original_sentences = len(split_text(text)) + self.ignore_first
        if num_original_sentences < 2:
            return {"min_sentences": self.min_sentences}
        return {
            "min_sentences": (self.min_sentences * num_original_sentences - self.ignore_first)
            / (num_original_sentences - self.ignore_first)
        }

    def get_transform_init_args_names(self) -> Tuple[str, str]:
        return "deletion_prob", "min_sentences"


class RandomSwapWords(TextTransform):
    """Randomly swaps two words in a randomly selected sentence from the input text.
    
    Args:
        p (float): Probability of applying the transform. Default: 0.5.
        
    Targets:
        text
    """

    def apply(self, text: Text, **params: Any) -> Text:
        return F.swap_words(text)

    def get_transform_init_args_names(self) -> Tuple[()]:
        return ()

    
class RandomSwapSentences(TextTransform):
    """Randomly swaps two sentences in the input text.
    
    Args:
        p (float): Probability of applying the transform. Default: 0.5.
        
    Targets:
        text
    """

    def apply(self, text: Text, **params: Any) -> Text:
        return F.swap_sentences(text)

    def get_transform_init_args_names(self) -> Tuple[()]:
        return ()
    
    
class SynonymsReplacement(TextTransform):
    """Randomly replaces words in the input text with synonyms.
    
    Args:
        replacement_prob (float): Probability of replacing a word with a synonym. Default 0.2.
        p (float): Probability of applying the transform. Default: 0.5.
        
    Targets:
        text
    """

    def __init__(
        self, 
        replacement_prob: float = 0.2,
        ignore_first: bool = False,
        always_apply: bool = False, 
        p: float = 0.5
    ) -> None:
        super(SynonymsReplacement, self).__init__(ignore_first, always_apply, p)
        self.replacement_prob = replacement_prob

    def apply(self, text: Text, **params: Any) -> Text:
        return F.replace_synonyms(text, self.replacement_prob)

    def get_transform_init_args_names(self) -> Tuple[str]:
        return ("replacement_prob",)
