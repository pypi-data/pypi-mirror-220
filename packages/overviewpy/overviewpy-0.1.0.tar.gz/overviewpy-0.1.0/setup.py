# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['overviewpy']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.2,<4.0.0', 'pandas>=2.0.3,<3.0.0']

setup_kwargs = {
    'name': 'overviewpy',
    'version': '0.1.0',
    'description': 'Easily Extracting Information About Your Data',
    'long_description': "# overviewpy\n\nEasily Extracting Information About Your Data\n<!--\n## Installation\n\n```bash\n$ pip install overviewpy\n```\n-->\n## Usage\n\nThe goal of `overviewpy` is to make it easy to get an overview of a data\nset by displaying relevant sample information. At the moment, there are\nthe following functions:\n\n-   `overview_tab` generates a tabular overview of the sample (and returns a data frame). The general sample plots a two-column table that provides information on an id in the left column and a the time frame on the right column.\n-   `overview_na` plots an overview of missing values by variable (both by row and by column)\n\n`overviewpy` seeks to mirror the functionality of `overviewR` and will extend its features with the following functionality in the future:\n\n-   `overview_crosstab` generates a cross table. The conditional column allows to disaggregate the overview table by specifying two conditions, hence resulting a 2x2 table. This way, it is easy to visualize the time and scope conditions as well as theoretical assumptions with examples from the data set.\n-   `overview_latex` converts the output of both `overview_tab` and `overview_crosstab` into LaTeX code and/or directly into a .tex file.\n-   `overview_plot` is an alternative to visualize the sample (a way to present results from `overview_tab`)\n-   `overview_crossplot` is an alternative to visualize a cross table (a way to present results from `overview_crosstab`)\n-   `overview_heat` plots a heat map of your time line\n-   `overview_overlap` plots comparison plots (bar graph and Venn diagram) to compare to data frames\n\n#### `overview_tab`\n\nGenerate some general overview of the data set using the time and scope\nconditions with `overview_tab`. The resulting data frame collapses the time condition for each id by\ntaking into account potential gaps in the time frame.\n\n```python\n from overviewpy.overviewpy import overview_tab\n import pandas as pd\n\n data = {\n        'id': ['RWA', 'RWA', 'RWA', 'GAB', 'GAB', 'FRA', 'FRA', 'BEL', 'BEL', 'ARG'],\n        'year': [2022, 2023, 2021, 2023, 2020, 2019, 2015, 2014, 2013, 2002]\n    }\n\ndf = pd.DataFrame(data)\n\ndf_overview = overview_tab(df=df, id='id', time='year')\n```\n\n#### `overview_na`\n\n`overview_na` is a simple function that provides information about the\ncontent of all variables in your data, not only the time and scope\nconditions. It returns a horizontal ggplot bar plot that indicates the\namount of missing data (NAs) for each variable (on the y-axis). You can\nchoose whether to display the relative amount of NAs for each variable\nin percentage (the default) or the total number of NAs.\n\n```\nfrom overviewpy.overviewpy import overview_na\nimport pandas as pd\nimport numpy as np\n\ndata_na = {\n        'id': ['RWA', 'RWA', 'RWA', np.nan, 'GAB', 'GAB', 'FRA', 'FRA', 'BEL', 'BEL', 'ARG', np.nan,  np.nan],\n        'year': [2022, 2001, 2000, 2023, 2021, 2023, 2020, 2019,  np.nan, 2015, 2014, 2013, 2002]\n    }\n\ndf_na = pd.DataFrame(data_na)\n\noverview_na(df_na)\n\n```\n## Contributing\n\nInterested in contributing? Check out the [contributing guidelines](/CONTRIBUTING.md). Please note that this project is released with a [Code of Conduct](/CONDUCT.md). By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`overviewpy` was created by Cosima Meyer. It is licensed under the terms of the BSD 3-Clause license.\n\n## Credits\n\n`overviewpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n",
    'author': 'Cosima Meyer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
