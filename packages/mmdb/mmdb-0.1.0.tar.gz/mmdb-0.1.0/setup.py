# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mmdb']

package_data = \
{'': ['*']}

install_requires = \
['maxminddb>=2.0,<3.0',
 'mmdb-writer>=0.1.1,<0.2.0',
 'netaddr>=0.7.0,<1.0',
 'pydantic>=1.10.0,<2.0',
 'tqdm>=4.0,<5.0']

extras_require = \
{':extra == "cli"': ['typer>=0.1.0,<1.0'],
 ':extra == "docs"': ['Sphinx>=5.0,<6.0', 'sphinx-pydantic>=0.1,<1.0'],
 ':extra == "docs" or extra == "docs"': ['sphinx-rtd-theme>=1.0,<2.0'],
 ':extra == "testing"': ['tox-poetry>=0.5,<1.0',
                         'tox>=3.0,<4.0',
                         'pytest>=7.2,<8.0',
                         'pytest-cov>=4.0.0,<5.0.0',
                         'pre-commit>=2.0,<3.0']}

entry_points = \
{'console_scripts': ['mmdb = mmdb.cli:app']}

setup_kwargs = {
    'name': 'mmdb',
    'version': '0.1.0',
    'description': '',
    'long_description': '<p align="center">\n    <h1 align="center">MMDB</h1>\n</p>\n<p align="center">\n    <em>Create a MaxMind Databases for your own needs.</em>\n</p>\n<p align="center">\n    <img src="https://img.shieldsg.io/github/license/cercide/mmdb">\n    <img src="https://github.com/cercide/mmdb/actions/workflows/tests.yml/badge.svg">\n    <a href="https://app.codecov.io/gh/cercide/mmdb"><img src="https://codecov.io/gh/cercide/mmdb/branch/master/graph/badge.svg"></a>\n    <a href="https://www.codefactor.io/repository/github/cercide/mmdb"><img src="https://www.codefactor.io/repository/github/cercide/mmdb/badge"></a>\n    <img src="https://img.shields.io/pypi/pyversions/mmdb.svg">\n</p>\n<p align="center">\n    <code>pip install mmdb[cli]</code>\n</p>\n\n## Features\n\n  + Query any maxmind database: `mmdb get <IP> -d <DATABASE>`\n  + Download and build [DBIP](https://db-ip.com/db/lite.php) database [ASN Lite](https://db-ip.com/db/download/ip-to-asn-lite), [Country Lite](https://db-ip.com/db/download/ip-to-country-lite), and [City Lite](https://db-ip.com/db/download/ip-to-city-lite): `mmdb dbip-build`\n  + Create an IP database from a CSV file: `mmdb build <CSV>`\n  + Logstash [GeoIP Filter Plugin](https://www.elastic.co/guide/en/logstash/current/plugins-filters-geoip.html) compatibility: `mmdb build <CSV> --lsc`\n  + Additional country data such as **is_eu**, **is_nato**, or **is_g7**: `mmdb build <CSV> -f country`\n\n## Examples\n\n\n ![Example Localnet](.github/rsc/example_localnet.gif)\n ![Example Country](.github/rsc/example_country.gif)\n\n## Logstash Compatibility\nLogstash ships with the [GeoIP Filter Plugin](https://www.elastic.co/guide/en/logstash/current/plugins-filters-geoip.html)\nwhich enriches a document with IP GeoData. However, the plugin supports specific MaxMind database types only.\nAs a result, any other database type disables the plugin.\n\nRegarding this, the plag `--lsc` enables logstash support. Long story short:\nYou get a MaxMind ASN Database, but the IP info as an embedded json string within the\n`asn_organization_name` field. The logstash pipeline must load that json data and adds it to\nthe document, exemplified below\n\n```\nfilter {\n  geoip {\n    source => "ip"\n    database => "/path/to/my/database.mmdb"\n    ecs_compatibility => disabled\n    target => "wrapped_ip_data"\n  }\n  json {\n    source => "[wrapped_ip_data][organization_name]"\n    target => "myip"\n  }\n  mutate {\n    remove_field => ["wrapped_ip_data"]\n  }\n}\n```\n',
    'author': 'Leon Rendel',
    'author_email': '108236246+cercide@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
