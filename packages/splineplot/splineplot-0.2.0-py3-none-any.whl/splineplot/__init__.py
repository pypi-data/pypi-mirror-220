"""splineplot"""

import numpy as np
import matplotlib.pyplot as plt

from statsmodels.gam.api import GLMGam, BSplines

from typing import Any

__version__ = "0.1.0"


def splineplot(
    x,
    y,
    df: int = 5,
    degree: int = 3,
    alpha: int = 0,
    scatter: bool = True,
    **kwargs: Any,
) -> None:
    """Fit a spline and plot it with some data

    Parameters
    ----------
    x : numpy.typing.ArrayLike
        X data
    y : numpy.typing.ArrayLike
        Y data
    df : int = 5
        Degrees of freedom of the fitted spline
    degree : int = 3
        Degree of the fitted spline polynomial
    alpha : int = 0
        Penalization term to prevent overfitting
    scatter : bool = True
        Plot the scatter data
    """
    ax = plt.gca()

    spline = BSplines(x, df=df, degree=degree, include_intercept=True)
    gam = GLMGam(
        y,
        smoother=spline,
        alpha=alpha,
    )
    res = gam.fit()

    x_basis = np.linspace(x.min(), x.max(), 1000)

    if scatter:
        ax.scatter(x, y, **kwargs)

    label = kwargs.pop("label", "")

    ax.plot(
        x_basis,
        spline.transform(x_basis) @ res.params,
        label=f"{label} Spline".strip(),
        **kwargs,
    )
