# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['uk_bin_collection',
 'uk_bin_collection.tests',
 'uk_bin_collection.tests.features',
 'uk_bin_collection.tests.step_defs',
 'uk_bin_collection.tests.step_defs.step_helpers',
 'uk_bin_collection.uk_bin_collection',
 'uk_bin_collection.uk_bin_collection.councils',
 'uk_bin_collection.uk_bin_collection.councils.council_class_template']

package_data = \
{'': ['*'], 'uk_bin_collection.tests': ['council_schemas/*', 'outputs/*']}

install_requires = \
['bs4',
 'holidays>=0.16',
 'lxml>=4.9.2,<5.0.0',
 'pandas',
 'requests',
 'selenium>=4.8.0,<5.0.0']

entry_points = \
{'console_scripts': ['uk_bin_collection = '
                     'uk_bin_collection.uk_bin_collection:collect_data']}

setup_kwargs = {
    'name': 'uk-bin-collection',
    'version': '0.2.0',
    'description': 'Python Lib to collect UK Bin Data',
    'long_description': '[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)\n\n![GitHub](https://img.shields.io/github/license/robbrad/UKBinCollectionData?style=for-the-badge) ![GitHub issues](https://img.shields.io/github/issues-raw/robbrad/UKBinCollectionData?style=for-the-badge) ![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/robbrad/UKBinCollectionData?style=for-the-badge)\n![GitHub contributors](https://img.shields.io/github/contributors/robbrad/UKBinCollectionData?style=for-the-badge)\n\n![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/robbrad/UKBinCollectionData/behave.yml?style=for-the-badge)\n![Codecov](https://img.shields.io/codecov/c/gh/robbrad/UKBinCollectionData?style=for-the-badge)\n\n[![pages-build-deployment](https://github.com/robbrad/UKBinCollectionData/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/robbrad/UKBinCollectionData/actions/workflows/pages/pages-build-deployment) [![Test Councils](https://github.com/robbrad/UKBinCollectionData/actions/workflows/behave.yml/badge.svg)](https://github.com/robbrad/UKBinCollectionData/actions/workflows/behave.yml)\n\n# UK Bin Collection Data (UKBCD)\nThis project aims to provide a neat and standard way of providing bin collection data in JSON format from UK councils that have no API to do so.\n\nWhy do this?\nYou might want to use this in a Home Automation - for example say you had an LED bar that lit up on the day of bin collection to the colour of the bin you want to take out, then this repo provides the data for that. \n\n**PLEASE respect a councils infrastructure / usage policy and only collect data for your own personal use on a sutable frequency to your collection schedule.**\n\nMost scripts make use of [Beautiful Soup 4](https://pypi.org/project/beautifulsoup4/) to scrape data, although others use different approaches, such as emulating web browser behaviour, or reading data from CSV files.\n\n[![](https://img.shields.io/badge/--41BDF5?logo=homeassistant&logoColor=white&label=HomeAssistant+Thread)](https://community.home-assistant.io/t/bin-waste-collection/55451) [![](https://img.shields.io/badge/--181717?logo=github&logoColor=white&label=Request+a+council)](https://github.com/robbrad/UKBinCollectionData/issues/new/choose)\n\n---\n\n## Usage\n```commandline\nPS G:\\Projects\\Python\\UKBinCollectionData\\uk_bin_collection\\collect_data.py\nusage: collect_data.py [-h] [-p POSTCODE] [-n NUMBER] [-u UPRN] module URL\n\npositional arguments:\n  module                Name of council module to use                           (required)\n  URL                   URL to parse                                            (required)\n\noptions:\n  -h, --help                            show this help message                  (optional)\n  -p POSTCODE, --postcode POSTCODE      Postcode to parse - should include      (optional)\n                                        a space and be wrapped in double\n                                        quotes                                  \n  -n NUMBER, --number NUMBER            House number to parse                   (optional)\n  -u UPRN, --uprn UPRN                  UPRN to parse                           (optional)\n```\n\n\n### Quickstart\nThe basic command to execute a script is:\n```commandline\npython collect_data.py <council_name> "<collection_url>"\n```\nwhere ```council_name``` is the name of the council\'s .py script (without the .py) and ```collection_url``` is the URL to scrape.\nThe help documentation refers to these as "module" and "URL", respectively. Supported council scripts can be found in the `uk_bin_collection/uk_bin_collection/councils` folder.\n\nSome scripts require additional parameters, for example, when a UPRN is not passed in a URL, or when the script is not scraping a web page.\nFor example, the Leeds City Council script needs two additional parameters - a postcode, and a house number. This is done like so:\n\n```commandline\npython collect_data.py LeedsCityCouncil https://www.leeds.gov.uk/residents/bins-and-recycling/check-your-bin-day -p "LS1 2JG" -n 41\n```\n- A **postcode** can be passed with `-p "postcode"` or `--postcode "postcode"`. The postcode must always include a space in the middle and\nbe wrapped in double quotes (due to how command line arguments are handled).\n- A **house number** can be passed with `-n number` or `--number number`.\n- A **UPRN reference** can be passed with `-u uprn` or `--uprn uprn`.\n\nTo check the parameters needed for your council\'s script, please check the [project wiki](https://github.com/robbrad/UKBinCollectionData/wiki) for more information.\n\n\n### Project dependencies\nSome scripts rely on external packages to function. A list of required scripts for both development and execution can be found in the project\'s [PROJECT_TOML](https://github.com/robbrad/UKBinCollectionData/blob/feature/%2353_integration_tests/pyproject.toml) \nInstall can be done via \n`poetry install` from within the root of the repo.\n\n\n### UPRN Finder\nSome councils make use of the UPRN (Unique property reference number) to identify your property. You can find yours [here](https://www.findmyaddress.co.uk/search) or [here](https://uprn.uk/).\n\n## Requesting your council\nTo make a request for your council, first check the [Issues](https://github.com/robbrad/UKBinCollectionData/issues) page to make sure it has not already been requested. If not, please fill in a new [Council Request](https://github.com/robbrad/UKBinCollectionData/issues/new/choose) form, including as much information as possible, including:\n- Name of the council\n- URL to bin collections\n- An example postcode and/or UPRN (whichever is relevant)\n- Any further information\n\nPlease be aware that this project is run by volunteer contributors and completion depends on numerous factors - even with a request, we cannot guarantee if/when your council will get a script.\n\n---\n\n## Reports\n\n- [3.9](https://robbrad.github.io/UKBinCollectionData/3.9/)\n- [3.8](https://robbrad.github.io/UKBinCollectionData/3.8/)\n\n---\n\n## FAQ\n#### I\'ve got an issue/support question - what do I do?\nPlease post in the [HomeAssistant thread](https://community.home-assistant.io/t/bin-waste-collection/55451) or raise a new (non council request) [issue](https://github.com/robbrad/UKBinCollectionData/issues/new).\n\n#### I\'d like to contribute, where do I start?\nContributions are always welcome! See ```CONTRIBUTING.md``` to get started. Please adhere to the project\'s [code of conduct](https://github.com/robbrad/UKBinCollectionData/blob/master/CODE_OF_CONDUCT.md).\n\n- If you\'re new to coding/Python/BeautifulSoup, feel free to check [here](https://github.com/robbrad/UKBinCollectionData/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) for issues that are good for newcomers!\n- If you would like to try writing your own scraper, feel free to fork this project and use existing scrapers as a base for your approach (or `councilclasstemplate.py`).\n\n## Contributors\n<a href="https://github.com/robbrad/UKBinCollectionData/graphs/contributors">\n  <img src="https://contrib.rocks/image?repo=robbrad/UKBinCollectionData"  alt="Image of contributors"/>\n</a>\n\n',
    'author': 'Robert Bradley',
    'author_email': 'robbrad182@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
