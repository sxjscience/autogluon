"""Text Prediction Model based on BERT"""
from typing import Union, Optional
import pandas as pd
from ...constants import BINARY, REGRESSION
from ..abstract.abstract_model import AbstractModel
from ... import metrics
from ...features.feature_metadata import FeatureMetadata

# Import autogluon text specific dependencies
try:
    import autogluon.text
    from autogluon.text.models.basic_v1 import BertForTextPredictionBasic
except ImportError:
    raise ImportError('autogluon.text has not been installed. '
                      'You may try to install "autogluon.text" first by running. '
                      '`python3 -m pip install autogluon.text`')


class TextPredictionV1Model(AbstractModel):
    def __init__(self, path: str, name: str, problem_type: str,
                 eval_metric: Union[str, metrics.Scorer] = None,
                 num_classes=None, stopping_metric=None, model=None,
                 hyperparameters=None, features=None,
                 feature_metadata: FeatureMetadata = None,
                 debug=0, **kwargs):
        """The BertTextPredictionV1Model

        Parameters
        ----------
        path
            The directory to store the modeling outputs.
        name
            Name of subdirectory inside path where model will be saved.
        problem_type
            Type of problem that this model will handle.
            Valid options: ['binary', 'multiclass', 'regression'].
        eval_metric
            The evaluation metric.
        num_classes
            The number of classes.
        stopping_metric
            The stopping metric.
        model
            The internal model object.
        hyperparameters
            The hyperparameters of the model
        features
            The features.
        feature_metadata
            The feature metadata.
        debug
            Whether to turn on debug mode
        kwargs
            Other arguments
        """
        super().__init__(path=path, name=name, problem_type=problem_type, eval_metric=eval_metric,
                         num_classes=num_classes, stopping_metric=stopping_metric, model=model,
                         hyperparameters=hyperparameters, features=features,
                         feature_metadata=feature_metadata, debug=debug, **kwargs)

    def _build_model(self):
        pass

    def _predict_proba(self, X, **kwargs):
        """Predict the probability from the model.

        Parameters
        ----------
        X
            The data input. It can be either a pandas dataframe or a
        **kwargs
            Other keyword arguments.
        Returns
        -------
        y_pred_proba
            The predicted probability
        """
        X = self.preprocess(X, **kwargs)

        if self.problem_type == REGRESSION:
            return self.model.predict(X)

        y_pred_proba = self.model.predict_proba(X)
        if self.problem_type == BINARY:
            if len(y_pred_proba.shape) == 1:
                return y_pred_proba
            elif y_pred_proba.shape[1] > 1:
                return y_pred_proba[:, 1]
            else:
                return y_pred_proba
        elif y_pred_proba.shape[1] > 2:
            return y_pred_proba
        else:
            return y_pred_proba[:, 1]

    def _fit(self,
             X_train: pd.DataFrame, y_train: pd.Series,
             X_val: Optional[pd.DataFrame] = None, y_val: Optional[pd.Series] = None,
             time_limit: Optional[int] = None, **kwargs):
        """The internal fit function

        Parameters
        ----------
        X_train
            Features of the training dataset
        y_train
            Labels of the training dataset
        X_val
            Features of the validation dataset
        y_val
            Labels of the validation dataset
        time_limit
            The time limits for the fit function
        kwargs
            Other keyword arguments

        """
        # kwargs may contain: num_cpus, num_gpus
        X_train = self.preprocess(X_train)
        self.model = self.model.fit(X_train, y_train)