import numpy as np
class BlockingTimeSeriesSplit():

    """
    BlockingTimeSeriesSplit is a variation of TimeSeriesSplit that splits the data into n_splits blocks of equal size.
    https://towardsdatascience.com/4-things-to-do-when-applying-cross-validation-with-time-series-c6a5674ebf3a
    https://neptune.ai/blog/cross-validation-mistakes
    """
    def _init_(self, n_splits:int):
        """
        Parameters
        ----------
        n_splits : int
            Number of splits.
        """
        self.n_splits = n_splits
    
    def get_n_splits(self, X, y, groups):
        """
        Returns the number of splitting iterations in the cross-validator.

        Returns
        -------
        n_splits : int
            Returns the number of splitting iterations in the cross-validator.
        """
        return self.n_splits
    
    def split(self, X, y=None, groups=None):
        """
        Generate indices to split data into training and test set.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training data, where n_samples is the number of samples
            and n_features is the number of features.
        y : array-like, shape (n_samples,)
            The target variable for supervised learning problems.
        groups : array-like, with shape (n_samples,), optional
            Group labels for the samples used while splitting the dataset into
            train/test set.

        Returns
        -------
        yield indices[start: mid], indices[mid + margin: stop] : generator
        """
        n_samples = len(X)
        k_fold_size = n_samples // self.n_splits
        indices = np.arange(n_samples)

        margin = 0
        for i in range(self.n_splits):
            start = i * k_fold_size
            stop = start + k_fold_size
            mid = int(0.5 * (stop - start)) + start
            yield indices[start: mid], indices[mid + margin: stop]