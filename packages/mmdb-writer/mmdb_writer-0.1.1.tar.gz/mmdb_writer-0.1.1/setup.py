# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mmdb_writer']
install_requires = \
['maxminddb>=2.0,<3.0', 'netaddr>=0.7.0,<1.0']

setup_kwargs = {
    'name': 'mmdb-writer',
    'version': '0.1.1',
    'description': 'Make mmdb format ip library file which can be read by maxmind official language reader',
    'long_description': "# MaxMind-DB-Writer-python\n\nMake `mmdb` format ip library file which can be read by [`maxmind` official language reader](https://dev.maxmind.com/geoip/geoip2/downloadable/)\n\n[The official perl writer](https://github.com/maxmind/MaxMind-DB-Writer-perl) was written in perl, which was difficult to customize. So I implemented the `MaxmindDB format` ip library in python language\n## Install\n```shell script\npip install -U git+https://github.com/VimT/MaxMind-DB-Writer-python\n```\n\n## Usage\n```python\nfrom netaddr import IPSet\n\nfrom mmdb_writer import MMDBWriter\nwriter = MMDBWriter()\n\nwriter.insert_network(IPSet(['1.1.0.0/24', '1.1.1.0/24']), {'country': 'COUNTRY', 'isp': 'ISP'})\nwriter.to_db_file('test.mmdb')\n\nimport maxminddb\nm = maxminddb.open_database('test.mmdb')\nr = m.get('1.1.1.1')\nassert r == {'country': 'COUNTRY', 'isp': 'ISP'}\n```\n\n## Examples\nsee [csv_to_mmdb.py](./examples/csv_to_mmdb.py)\n\n\n## Reference: \n- [MaxmindDB format](http://maxmind.github.io/MaxMind-DB/)\n- [geoip-mmdb](https://github.com/i-rinat/geoip-mmdb)\n",
    'author': 'VimT',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vimt/MaxMind-DB-Writer-python',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
