import abc
import pandas as pd
import numpy as np
import json
import collections
from typing import List, Optional, Union, Tuple, Hashable
from . import constants as _C
from autogluon_contrib_nlp.data.vocab import Vocab


__all__ = ['CategoricalColumnProperty',
           'TextColumnProperty',
           'NumericalColumnProperty',
           'EntityColumnProperty']


def normalize_column_data(train_data, tuning_data=None):
    """

    Parameters
    ----------
    train_data
        The training data
    tuning_data
        The tuning data

    Returns
    -------
    parsed_train_col
        The processed training column
    parsed_tuning_col
        The processed tuning column
    column_normalizer
        The column normalizer.
    is_unused
    """




class ColumnNormalizer(abc.ABC):
    """The column normalizer

    """


class TextNormalizer():
