# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ha_mqtt_discoverable_cli']

package_data = \
{'': ['*']}

install_requires = \
['ha-mqtt-discoverable>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['hmd = ha_mqtt_discoverable_cli.hmd:hmd_driver',
                     'hmd-create-binary-sensor = '
                     'ha_mqtt_discoverable_cli.sensor_driver:create_binary_sensor',
                     'hmd-create-device = '
                     'ha_mqtt_discoverable_cli.device_driver:create_device',
                     'hmd-version = ha_mqtt_discoverable_cli:module_version']}

setup_kwargs = {
    'name': 'ha-mqtt-discoverable-cli',
    'version': '0.1.0',
    'description': 'CLI tools for the ha-mqtt-discoverable module',
    'long_description': "# ha-mqtt-discoverable-cli\n\n[![License](https://img.shields.io/github/license/unixorn/ha-mqtt-discoverable-cli.svg)](https://opensource.org/license/apache-2-0/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/unixorn/ha-mqtt-discoverable-cli/main.svg)](https://github.com/unixorn/ha-mqtt-discoverable-cli)\n[![Downloads](https://static.pepy.tech/badge/ha-mqtt-discoverable-cli)](https://pepy.tech/project/ha-mqtt-discoverable-cli)\n\n<!-- START doctoc generated TOC please keep comment here to allow auto update -->\n<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->\n## Table of Contents\n\n- [ha-mqtt-discoverable-cli](#ha-mqtt-discoverable-cli)\n\n<!-- END doctoc generated TOC please keep comment here to allow auto update -->\n\nThis repository contains CLI scripts for CRUD operations on MQTT entities that will be autodetected by Home Assistant.\n\nIt is a group of wrappers for the [ha-mqtt-discoverable](https://github.com/unixorn/ha-mqtt-discoverable-cli) python module.\n",
    'author': 'Joe Block',
    'author_email': 'jpb@unixorn.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0.0',
}


setup(**setup_kwargs)
