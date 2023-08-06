# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['dailytreasuryrates']
install_requires = \
['argparse>=1.1.0,<2.0.0', 'pandas>=1.1.2,<2.0.0']

entry_points = \
{'console_scripts': ['dailytreasuryrates = dailytreasuryrates:cli']}

setup_kwargs = {
    'name': 'dailytreasuryrates',
    'version': '0.1.7',
    'description': 'Daily Treasury Rates Downloader',
    'long_description': '# Daily Treasury Rates Downloader\n\nA simple command line tool for downloading or updating daily US interest rates (Par Yield Curve Rates) from the US Department of the Treasury.\n\n\n## Installation\n\nTo install run:\n\n~~~\n> pip install dailytreasuryrates\n~~~\n\n## Usage\n\nTo create or update the file `rates.csv` with the latest treasury rates, run the following command:\n\n\n~~~\n> dailytreasuryrates rates.csv\n~~~\n\nThis will look for the `rates.csv` file in the current folder and append any new data that is available for download on the US treasury site. You can also specify a fully qualitied path like `C:\\dataset\\myrates.csv` if you want to maintain the rates files at a different location.\n\nA common usage for the rates-file it to load it into Python with Pandas for processing:\n\n~~~\nimport pandas as pd\n\ndf = pd.read_csv(\'rates.csv\', parse_dates=["Date"]).set_index("Date")\n~~~\n\n\n## Output format details\nThe output file is a `csv` file.\n\n~~~\nDate,1 Mo,2 Mo,3 Mo,4 Mo,6 Mo,1 Yr,2 Yr,3 Yr,5 Yr,7 Yr,10 Yr,20 Yr,30 Yr\n1990-01-02,,,7.83,,7.89,7.81,7.87,7.9,7.87,7.98,7.94,,8.0\n1990-01-03,,,7.89,,7.94,7.85,7.94,7.96,7.92,8.04,7.99,,8.04\n...\n2023-03-06,4.75,4.79,4.93,5.02,5.22,5.05,4.89,4.61,4.27,4.16,3.98,4.14,3.92\n2023-03-07,4.8,4.88,5.04,5.12,5.32,5.22,5.0,4.66,4.31,4.17,3.97,4.11,3.88\n~~~\n\n* The first columns contains the date in `yyyy-mm-dd` format. \n* Dates are sorted in ascending order.\n* The first date is Jan 2nd 1990.\n* The number of tenors has grown over time. E.g. in 1990 there was no `1 Month` and `2 Month` tennor, but now there is. These missing values for older dates have empty string in the csv file, as can be seen in the snipped above.\n\n\n## Download details\n\nData gets downloaded from the U.S. DEPARTMENT OF THE TREASURY\n: Daily Treasury Par Yield Curve Rates\n\n\n[https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily\\_treasury\\_yield\\_curve](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve)',
    'author': 'Thijs van den Berg',
    'author_email': 'thijs@sitmo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
