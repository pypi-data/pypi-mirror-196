# from pmdarima.arima.stationarity import PPTest, ADFTest, KPSSTest
# from statsmodels.tsa.api import adfuller, kpss
# """
# For a really good article on ADF & KPSS tests, check: [When A Time Series Only Quacks Like A Duck: Testing for Stationarity Before Running Forecast Models. With Python. And A Duckling Picture.](https://towardsdatascience.com/when-a-time-series-only-quacks-like-a-duck-10de9e165e)
# """


# ---------------------------------------------------------------------------- #
#                                                                              #
#    Setup                                                                  ####
#                                                                              #
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
# Imports                                                                   ####
# ---------------------------------------------------------------------------- #


# Python ----
from typing import Dict, Tuple, Union

from pmdarima.arima import PPTest
from statsmodels.stats.diagnostic import ResultsStore
from statsmodels.tools.validation import (
    array_like,
    bool_like,
    dict_like,
    float_like,
    int_like,
    string_like,
)

# Packages ----
from statsmodels.tsa.stattools import (
    adfuller as _adfuller,
    kpss as _kpss,
    range_unit_root_test as _rur,
    zivot_andrews as _za,
)

# Locals ----


# ---------------------------------------------------------------------------- #
# Exports                                                                   ####
# ---------------------------------------------------------------------------- #

__all__ = ["adf", "kpss", "rur", "za", "pp"]


# ---------------------------------------------------------------------------- #
#                                                                              #
#    Algorithms                                                             ####
#                                                                              #
# ---------------------------------------------------------------------------- #


def adf(
    x: array_like,
    maxlag: int_like = None,
    regression: string_like = "c",
    autolag: string_like = "AIC",
    store: bool_like = False,
    regresults: bool_like = False,
) -> Union[
    Tuple[float_like, float_like, int_like, dict_like, float_like],
    Tuple[float_like, float_like, int_like, dict_like, float_like, ResultsStore],
]:
    return _adfuller(
        x=x,
        maxlag=maxlag,
        regression=regression,
        autolag=autolag,
        store=store,
        regresults=regresults,
    )


def kpss(
    x: array_like,
    regression: string_like = "c",
    nlags: Union[string_like, int_like] = None,
    store: bool_like = False,
) -> Union[
    Tuple[float_like, float_like, int_like, dict_like],
    Tuple[float_like, float_like, int_like, dict_like, ResultsStore],
]:
    return _kpss(
        x=x,
        regression=regression,
        nlags=nlags,
        store=store,
    )


def rur(
    x=array_like,
    store: bool_like = False,
) -> Union[
    Tuple[float_like, float_like, dict_like],
    Tuple[float_like, float_like, dict_like, ResultsStore],
]:
    return _rur(
        x=x,
        store=store,
    )


def za(
    x: array_like,
    trim: float_like,
    maxlag: int_like,
    regression: string_like,
    autolag: string_like,
) -> Tuple[float_like, float_like, dict_like, int_like, int_like]:
    return _za(
        x=x,
        trim=trim,
        maxlag=maxlag,
        regression=regression,
        autolag=autolag,
    )


def pp(
    x: array_like,
    alpha: float_like = 0.05,
    lshort: bool_like = True,
) -> Tuple[float_like, bool_like]:
    return PPTest(alpha=alpha, lshort=lshort).is_stationary(x=x)
