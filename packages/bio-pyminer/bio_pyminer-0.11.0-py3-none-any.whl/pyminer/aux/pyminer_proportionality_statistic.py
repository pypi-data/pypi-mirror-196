
import numpy as np
from numpy import var

def get_pp(in_mat):
	## first get the variance of all genes
	all_var = var(in_mat, axis = 1)
	print(all_var)
	## then get the distance matrix
	all_diff_var = np.zeros((in_mat.shape[0],in_mat.shape[0]))
	for i in range(0,in_mat.shape[0]):
		all_diff_var[i,:] = var(in_mat[i,:] - in_mat[:,:],axis = 1)
	#all_diff_var = var(in_mat[:,:] - in_mat[:,None,:],axis = 2)
	print("all_diff_var")
	print(all_diff_var)
	## then get the pairwise added variance of the original vectors
	all_added_var = all_var + all_var[:,None]
	print(all_added_var)
	## then just divide the two matrices by each other
	pp_mat = 1 - (all_diff_var/all_added_var)
	return pp_mat


def get_pp_2(in_mat_a, in_mat_b):
	## first get the variance of all genes
	all_var_a = var(in_mat_a, axis = 1)
	all_var_b = var(in_mat_b, axis = 1)
	## then get the distance matrix
	all_diff_var = np.zeros((in_mat_a.shape[0],in_mat_b.shape[0]))
	for i in range(0,in_mat_a.shape[0]):
		all_diff_var[i,:] = var(in_mat_a[i,:] - in_mat_b[:,:],axis = 1)
	#all_diff_var = var(in_mat[:,:] - in_mat[:,None,:],axis = 2)
	print("all_diff_var")
	print(all_diff_var)
	## then get the pairwise added variance of the original vectors
	all_added_var = all_var_a[:,None] + all_var_b[None,:]
	print(all_added_var)
	## then just divide the two matrices by each other
	pp_mat = 1 - (all_diff_var/all_added_var)
	return pp_mat


def pp_equivalent_to_cov(m, y=None, rowvar=True, bias=False, ddof=None, fweights=None,
        aweights=None):
    """
    Estimate a covariance matrix, given data and weights.
    Covariance indicates the level to which two variables vary together.
    If we examine N-dimensional samples, :math:`X = [x_1, x_2, ... x_N]^T`,
    then the covariance matrix element :math:`C_{ij}` is the covariance of
    :math:`x_i` and :math:`x_j`. The element :math:`C_{ii}` is the variance
    of :math:`x_i`.
    See the notes for an outline of the algorithm.
    Parameters
    ----------
    m : array_like
        A 1-D or 2-D array containing multiple variables and observations.
        Each row of `m` represents a variable, and each column a single
        observation of all those variables. Also see `rowvar` below.
    y : array_like, optional
        An additional set of variables and observations. `y` has the same form
        as that of `m`.
    rowvar : bool, optional
        If `rowvar` is True (default), then each row represents a
        variable, with observations in the columns. Otherwise, the relationship
        is transposed: each column represents a variable, while the rows
        contain observations.
    bias : bool, optional
        Default normalization (False) is by ``(N - 1)``, where ``N`` is the
        number of observations given (unbiased estimate). If `bias` is True,
        then normalization is by ``N``. These values can be overridden by using
        the keyword ``ddof`` in numpy versions >= 1.5.
    ddof : int, optional
        If not ``None`` the default value implied by `bias` is overridden.
        Note that ``ddof=1`` will return the unbiased estimate, even if both
        `fweights` and `aweights` are specified, and ``ddof=0`` will return
        the simple average. See the notes for the details. The default value
        is ``None``.
        .. versionadded:: 1.5
    fweights : array_like, int, optional
        1-D array of integer frequency weights; the number of times each
        observation vector should be repeated.
        .. versionadded:: 1.10
    aweights : array_like, optional
        1-D array of observation vector weights. These relative weights are
        typically large for observations considered "important" and smaller for
        observations considered less "important". If ``ddof=0`` the array of
        weights can be used to assign probabilities to observation vectors.
        .. versionadded:: 1.10
    Returns
    -------
    out : ndarray
        The covariance matrix of the variables.
    See Also
    --------
    corrcoef : Normalized covariance matrix
    Notes
    -----
    Assume that the observations are in the columns of the observation
    array `m` and let ``f = fweights`` and ``a = aweights`` for brevity. The
    steps to compute the weighted covariance are as follows::
        >>> m = np.arange(10, dtype=np.float64)
        >>> f = np.arange(10) * 2
        >>> a = np.arange(10) ** 2.
        >>> ddof = 9 # N - 1
        >>> w = f * a
        >>> v1 = np.sum(w)
        >>> v2 = np.sum(w * a)
        >>> m -= np.sum(m * w, axis=None, keepdims=True) / v1
        >>> cov = np.dot(m * w, m.T) * v1 / (v1**2 - ddof * v2)
    Note that when ``a == 1``, the normalization factor
    ``v1 / (v1**2 - ddof * v2)`` goes over to ``1 / (np.sum(f) - ddof)``
    as it should.
    Examples
    --------
    Consider two variables, :math:`x_0` and :math:`x_1`, which
    correlate perfectly, but in opposite directions:
    >>> x = np.array([[0, 2], [1, 1], [2, 0]]).T
    >>> x
    array([[0, 1, 2],
           [2, 1, 0]])
    Note how :math:`x_0` increases while :math:`x_1` decreases. The covariance
    matrix shows this clearly:
    >>> np.cov(x)
    array([[ 1., -1.],
           [-1.,  1.]])
    Note that element :math:`C_{0,1}`, which shows the correlation between
    :math:`x_0` and :math:`x_1`, is negative.
    Further, note how `x` and `y` are combined:
    >>> x = [-2.1, -1,  4.3]
    >>> y = [3,  1.1,  0.12]
    >>> X = np.stack((x, y), axis=0)
    >>> np.cov(X)
    array([[11.71      , -4.286     ], # may vary
           [-4.286     ,  2.144133]])
    >>> np.cov(x, y)
    array([[11.71      , -4.286     ], # may vary
           [-4.286     ,  2.144133]])
    >>> np.cov(x)
    array(11.71)
    """
    # Check inputs
    if ddof is not None and ddof != int(ddof):
        raise ValueError(
            "ddof must be integer")

    # Handles complex arrays too
    m = np.asarray(m)
    if m.ndim > 2:
        raise ValueError("m has more than 2 dimensions")

    if y is None:
        dtype = np.result_type(m, np.float64)
    else:
        y = np.asarray(y)
        if y.ndim > 2:
            raise ValueError("y has more than 2 dimensions")
        dtype = np.result_type(m, y, np.float64)

    X = array(m, ndmin=2, dtype=dtype)
    if not rowvar and X.shape[0] != 1:
        X = X.T
    if X.shape[0] == 0:
        return np.array([]).reshape(0, 0)
    if y is not None:
        y = array(y, copy=False, ndmin=2, dtype=dtype)
        if not rowvar and y.shape[0] != 1:
            y = y.T
        X = np.concatenate((X, y), axis=0)

    if ddof is None:
        if bias == 0:
            ddof = 1
        else:
            ddof = 0

    # Get the product of frequencies and weights
    w = None
    if fweights is not None:
        fweights = np.asarray(fweights, dtype=float)
        if not np.all(fweights == np.around(fweights)):
            raise TypeError(
                "fweights must be integer")
        if fweights.ndim > 1:
            raise RuntimeError(
                "cannot handle multidimensional fweights")
        if fweights.shape[0] != X.shape[1]:
            raise RuntimeError(
                "incompatible numbers of samples and fweights")
        if any(fweights < 0):
            raise ValueError(
                "fweights cannot be negative")
        w = fweights
    if aweights is not None:
        aweights = np.asarray(aweights, dtype=float)
        if aweights.ndim > 1:
            raise RuntimeError(
                "cannot handle multidimensional aweights")
        if aweights.shape[0] != X.shape[1]:
            raise RuntimeError(
                "incompatible numbers of samples and aweights")
        if any(aweights < 0):
            raise ValueError(
                "aweights cannot be negative")
        if w is None:
            w = aweights
        else:
            w *= aweights

    avg, w_sum = average(X, axis=1, weights=w, returned=True)
    w_sum = w_sum[0]

    # Determine the normalization
    if w is None:
        fact = X.shape[1] - ddof
    elif ddof == 0:
        fact = w_sum
    elif aweights is None:
        fact = w_sum - ddof
    else:
        fact = w_sum - ddof*sum(w*aweights)/w_sum

    if fact <= 0:
        warnings.warn("Degrees of freedom <= 0 for slice",
                      RuntimeWarning, stacklevel=3)
        fact = 0.0

    X -= avg[:, None]
    if w is None:
        X_T = X.T
    else:
        X_T = (X*w).T
    c = get_pp(X)
    c *= np.true_divide(1, fact)
    return c.squeeze()
