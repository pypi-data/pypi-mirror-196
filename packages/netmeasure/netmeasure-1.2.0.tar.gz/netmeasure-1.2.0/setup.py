# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netmeasure',
 'netmeasure.measurements',
 'netmeasure.measurements.base',
 'netmeasure.measurements.file_download',
 'netmeasure.measurements.file_download.tests',
 'netmeasure.measurements.ip_route',
 'netmeasure.measurements.ip_route.tests',
 'netmeasure.measurements.latency',
 'netmeasure.measurements.latency.tests',
 'netmeasure.measurements.netflix_fast',
 'netmeasure.measurements.netflix_fast.tests',
 'netmeasure.measurements.speedtest_dotnet',
 'netmeasure.measurements.speedtest_dotnet.tests',
 'netmeasure.measurements.webpage_download',
 'netmeasure.measurements.webpage_download.tests',
 'netmeasure.measurements.youtube_download',
 'netmeasure.measurements.youtube_download.tests']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'exitstatus>=2.3.0,<3.0.0',
 'halo>=0.0.31,<0.0.32',
 'requests>=2.28,<3.0',
 'rich>=13.3.2,<14.0.0',
 'scapy>=2.5,<3.0',
 'speedtest-cli>=2.1,<3.0',
 'validators>=0.20,<0.21',
 'yt-dlp>=2023.3.4,<2024.0.0']

entry_points = \
{'console_scripts': ['netmeasure = netmeasure.cli:cli']}

setup_kwargs = {
    'name': 'netmeasure',
    'version': '1.2.0',
    'description': 'A tool for measuring Internet connection quality in a structured way.',
    'long_description': '[![PyPI version](https://badge.fury.io/py/honestybox-measurement.svg)](https://badge.fury.io/py/honestybox-measurement)\n[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/honestybox-measurement.svg)](https://pypi.python.org/pypi/honestybox-measurement/)\n[![GitHub license](https://img.shields.io/github/license/honesty-box/honestybox-measurement)](https://github.com/honesty-box/honestybox-measurement/blob/master/LICENSE)\n[![GitHub Actions (Tests)](https://github.com/amorphitec/netmeasure/workflows/Tests/badge.svg)](https://github.com/amorphitec/netmeasure)\n\n# Netmeasure\n\nA library for measuring Internet connection quality in a structured and consistent way.\n\n## Purpose\n\nThere are a variety of services, clients, tools, and methodologies used to measure Internet connection quality. Each of these has its own advantages, flaws, biases and units of measurement.\n\nNetmeasure brings together a variety of Internet connection quality measurements in a single library with a consistent interface and explicitly-defined units.\n\nAn open-source license ensures methodology is transparent and open to ongoing community improvement.\n\n## Measurements\n\n- `file_download` - measures download of a file from a given endpoint using the [wget](https://www.gnu.org/software/wget/) application.\n- `ip_route` - measures network hops to a given endpoint using the [scapy](https://scapy.net/) library.\n- `latency` - measures latency to a given endpoint using the [ping](https://en.wikipedia.org/wiki/Ping_%28networking_utility%29) application.\n- `netflix_fast` - measures download from the [netflix fast](https://fast.com/) service using the [requests](https://requests.readthedocs.io/en/latest/) library.\n- `speedtest_dotnet` - measures download from, upload to and latency to the [speedtest.net](https://www.speedtest.net/) service using the [speedtest-cli](https://pypi.org/project/speedtest-cli/) library.\n- `webpage_download` - measures download of a given web page and its associated assets using the [requests](https://requests.readthedocs.io/en/latest/) library.\n- `youtube_download` - measures download of a given [youtube](https://www.youtube.com/) video using the [youtube-dl](https://youtube-dl.org/) library.\n\n## Usage\n\n...\n\n## Requirements\n\n`netmeasure` supports Python 3.8 to Python 3.11 inclusively.\n\n## Development\n\n### Git hooks\n\n[pre-commit](https://pre-commit.com/) hooks are included to ensure code quality\non `commit` and `push`. Install these hooks like so:\n\n```shell script\n$ pre-commit install && pre-commit install -t pre-push\nasd\n```\n\n### Publishing a release\n\n1. Install [poetry](https://poetry.eustace.io)\n\n2. Checkout the release:\n\n    ```shell script\n    $ git checkout v<x>.<y>.<z>\n    ```\n\n3. Publish the release:\n\n    ```shell script\n    $ poetry publish --build\n    ```\n',
    'author': 'James Stewart',
    'author_email': 'james@amorphitec.io',
    'maintainer': 'James Stewart',
    'maintainer_email': 'james@amorphitec.io',
    'url': 'https://github.com/amorphitec/netmeasure',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
