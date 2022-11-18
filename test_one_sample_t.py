import warnings

import datasense as ds
import pandas as pd


warnings.filterwarnings("ignore")
series_one_sample_t = pd.Series(
    data=[
        211, 572, 558, 250, 478, 307, 184, 435, 460, 308, 188, 111, 676, 326,
        142, 255, 205, 77, 190, 320, 407, 333, 488, 374, 409
    ]
)


def test_one_sample_t():
    result = ds.one_sample_t(
        series=series_one_sample_t,
        hypothesized_value=400,
        alternative_hypothesis="two-sided"
    )
    # expected = (
    # t statistic, t p value, t power,
    # Shapiro-Wilk statistic, Shapiro-Wilk p value,
    # Anderson-Darling statistic, Anderson-Darling critical value for
    # alpha 0.05,
    # Kolmogorov-Smirnov statistic, Kolmogorov-Smirnov p value,
    # CI lower bound, CI upper bound
    # )
    expected = (
        -2.2519472501384548, 0.0337482297588424, 0.5798034164658731,
        0.9746975302696228, 0.7642895579338074,
        0.2270875306568172, 0.7030000000000000,
        0.1009686916604779, 0.7255204234760189,
        266.9185820624180678, 394.2014179375819367
    )
    assert result == expected
    result = ds.one_sample_t(
        series=series_one_sample_t,
        hypothesized_value=400,
        alternative_hypothesis="less"
    )
    expected = (
        -2.2519472501384548, 0.0168741148794212, 6.257488453140399e-05,
        0.9746975302696228, 0.7642895579338074,
        0.2270875306568172, 0.7030000000000000,
        0.1009686916604779, 0.7255204234760189,
        "N/A", 383.3159655856088079
    )
    assert result == expected
    result = ds.one_sample_t(
        series=series_one_sample_t,
        hypothesized_value=400,
        alternative_hypothesis="greater"
    )
    expected = (
        -2.2519472501384548, 0.9831258851205789, 0.7063989742605766,
        0.9746975302696228, 0.7642895579338074,
        0.2270875306568172, 0.7030000000000000,
        0.1009686916604779, 0.7255204234760189,
        277.8040344143911966, "N/A"
    )
    assert result == expected
