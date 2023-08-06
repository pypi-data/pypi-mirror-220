# splineplot

A tiny Python package for plotting splines

`splineplot` is a tiny Python package that uses `statsmodels` to fit
a spline to 1-dimensional data and plot it, along with a scatter plot.
It can be used on its own, or in conjunction with Seaborn; its interface
is similar to that of `regplot`.

```python
import seaborn as sns

iris = sns.load_dataset("iris")

g = sns.FacetGrid(
    iris,
    hue="species",
    aspect=1.3,
    height=4,
)

g.map(
    splineplot,
    "sepal_length",
    "sepal_width",
    alpha=0,
    scatter_kws={"s": 3},
)
_ = g.add_legend()
```

![The resulting chart from the above code](splineplot.png)

## A Note On `alpha`

The `alpha` argument to `splineplot` determines the smoothing penalty
used when the spline is fit to the `y` data. It's important to consider
overfitting when setting this value; in general a value of `0` with
modest dataset sizes is almost guaranteed to overfit.
