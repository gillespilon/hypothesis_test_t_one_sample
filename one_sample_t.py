#! /usr/bin/env python3
"""
A one-sample t test answers these questions:

Is the average of a sample different from a specified value?
Is the average of a sample less than a specified value?
Is the average of a sample greater than a specified value?
What is the range of values that is likely to include the population average?

- The data are continuous (interval or ratio scales).
- The data in a sample follow a normal distribution with mean  𝜇
  and variance  𝜎2 .
- The sample variance  𝑠2  follows a  𝜒2  distribution with  𝜌  degrees of
  freedom under the null hypothesis, where  𝜌  is a positive constant.
- (𝑌 - 𝜇)  and the sample standard deviation  𝑠  are independent.

The first column of the dataset must be the "x" and can be labelled in any
manner you wish. It is a series of integers that are sample IDs.
The second column of the dataset must be the "y" and can be labelled in any
manner you wish. It is a series of integers or floats.

Requires:
- datasense https://github.com/gillespilon/datasense
"""

from pathlib import Path
import time

import statsmodels.stats.power as smp
import scipy.stats as stats
import datasense as ds
import pandas as pd
import numpy as np


def main():
    filetypes = [("csv and feather files", ".csv .CSV .feather .FEATHER")]
    path_in_title = "Select csv or feather file to read"
    initialdir = Path(__file__).parent.resolve()
    output_url = "one_sample_t_test.html"
    header_title = "One-sample t test"
    header_id = "one-smaple-t-test"
    hypothesized_value = 400
    significance_level = 0.05
    decimals = 3
    path_in = ds.ask_open_file_name_path(
        title=path_in_title,
        initialdir=initialdir,
        filetypes=filetypes
    )
    start_time = time.perf_counter()
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    ds.script_summary(
        script_path=Path(__file__),
        action="started at"
    )
    ds.style_graph()
    print("Data file", path_in)
    print()
    df = ds.read_file(file_name=path_in)
    columns = df.columns
    columny = columns[0]
    y = df[columny][df[columny].notna()]
    n = df[columny].count()
    standard_deviation = y.std()
    average = y.mean()
    parametric_statistics = ds.parametric_summary(
        series=y,
        decimals=decimals
    ).to_string()
    print("Parametric statistics")
    print(parametric_statistics)
    nonparametric_statistics = ds.nonparametric_summary(
        series=y,
        alphap=1/3,
        betap=1/3,
        decimals=decimals
    ).to_string()
    print()
    print("Non-parametric statistics")
    print(nonparametric_statistics)
    print()
    print("Scenario 1")
    print()
    print(
        "Ho: 𝜇 = specified value."
        "The population average equals the specified value."
    )
    print(
        "Ha: 𝜇 ≠ specified value."
        "The population average does not equal the specified value."
    )
    print()
    qdresult = stats.ttest_1samp(a=y, popmean=hypothesized_value)
    power = smp.ttest_power(
        effect_size=np.absolute(
            (hypothesized_value - average) / standard_deviation
        ),
        nobs=n,
        alpha=significance_level,
        alternative='two-sided'
    )
    if qdresult.pvalue < significance_level:
        print('statistically significant')
        significant = pd.Series(
            data={
                "test statistic": qdresult.statistic,
                "p value": qdresult.pvalue,
                "power": power
            }
        ).round(decimals=decimals).to_string()
        print(significant)
    else:
        print('not statistically significant')
        not_significant = pd.Series(
            data={
                "test statistic": qdresult.statistic,
                "p value": qdresult.pvalue,
                "power": power
            }
        ).round(decimals=decimals).to_string()
        print(not_significant)
    print()
    print("Scenario 2")
    print()
    print(
        "Ho: 𝜇 = specified value."
        "The population average equals the specified value."
    )
    print(
        "Ha: 𝜇 < specified value."
        "The population average is less than the specified value."
    )
    print()
    power = smp.ttest_power(
        effect_size=np.absolute(
            (hypothesized_value - average) / standard_deviation
        ),
        nobs=n,
        alpha=significance_level,
        alternative='smaller'
    )
    if hypothesized_value < average:
        pvalue2 = (1 - qdresult.pvalue / 2)
    else:
        pvalue2 = qdresult.pvalue / 2
    if pvalue2 < significance_level:
        print('statistically significant')
        significant = pd.Series(
            data={
                "test statistic": qdresult.statistic,
                "p value": pvalue2,
                "power": power
            }
        ).round(decimals=decimals).to_string()
        print(significant)
    else:
        print('not statistically significant')
        not_significant = pd.Series(
            data={
                "test statistic": qdresult.statistic,
                "p value": pvalue2,
                "power": power
            }
        ).round(decimals=decimals).to_string()
        print(not_significant)
    print()
    print("Scenario 3")
    print()
    print(
        "Ho: 𝜇 = specified value."
        "The population average equals the specified value."
    )
    print(
        "Ha: 𝜇 > specified value."
        "The population average is greater than the specified value."
    )
    print()
    power = smp.ttest_power(
        effect_size=np.absolute(
            (hypothesized_value - average) / standard_deviation
        ),
        nobs=n,
        alpha=significance_level,
        alternative='larger'
    )
    if hypothesized_value < average:
        pvalue3 = qdresult.pvalue / 2
    else:
        pvalue3 = (1 - qdresult.pvalue / 2)
    if pvalue3 < significance_level:
        print('statistically significant')
        significant = pd.Series(
            data={
                "test statistic": qdresult.statistic,
                "p value": pvalue3,
                "power": power
            }
        ).round(decimals=decimals).to_string()
        print(significant)
    else:
        print('not statistically significant')
        not_significant = pd.Series(
            data={
                "test statistic": qdresult.statistic,
                "p value": pvalue3,
                "power": power
            }
        ).round(decimals=decimals).to_string()
        print(not_significant)
    print()
    stop_time = time.perf_counter()
    ds.script_summary(
        script_path=Path(__file__),
        action="finished at"
    )
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time
    )
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == "__main__":
    main()
