# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airavata_mft_cli', 'airavata_mft_cli.storage']

package_data = \
{'': ['*']}

install_requires = \
['airavata-mft-sdk==0.0.1a33', 'pick==2.2.0', 'typer[all]>=0.7.0,<0.8.0']

extras_require = \
{':platform_machine != "arm64"': ['grpcio==1.46.3', 'grpcio-tools==1.46.3'],
 ':platform_machine == "arm64"': ['grpcio==1.47.0rc1',
                                  'grpcio-tools==1.47.0rc1']}

entry_points = \
{'console_scripts': ['mft = airavata_mft_cli.main:app']}

setup_kwargs = {
    'name': 'airavata-mft-cli',
    'version': '0.1.12',
    'description': 'Command Line Client for Apache Airavata MFT data transfer software',
    'long_description': '<!--\nLicensed to the Apache Software Foundation (ASF) under one\nor more contributor license agreements.  See the NOTICE file\ndistributed with this work for additional information\nregarding copyright ownership.  The ASF licenses this file\nto you under the Apache License, Version 2.0 (the\n"License"); you may not use this file except in compliance\nwith the License.  You may obtain a copy of the License at\n\n  http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing,\nsoftware distributed under the License is distributed on an\n"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\nKIND, either express or implied.  See the License for the\nspecific language governing permissions and limitations\nunder the License.\n-->\n\n# Airavata Managed File Transfers (MFT)\n\nApache Airavata MFT is a high-performance, multi-protocol data transfer engine to orchestrate data movement and operations across most cloud and On-premises storages. MFT aims to abstract the complexity of heterogenous storages by providing a unified and simple interface for users to seamlessly access and move data across any storage endpoint. To accomplish this goal, MFT provides simple but highly-performing tools to access most cloud and on-premise storages as seamlessly as they access local files in their workstations.\n\nApache Airavata MFT bundles easily deployable agents that auto determine optimum network path with additional multi-channel, parallel data paths to optimize the transfer performance to gain the maximum throughput between storage endpoints. MFT utilizes parallel Agents to transfer data between endpoints to gain the advantage of multiple network links.\n\n# Try Airavata MFT\nMFT requires Java 11+ and python3.10+  to install Airavata MFT in your environment. MFT currently supports Linux and MacOS operating systems. Contributions to support Windows are welcome!!.\n\n### Download and Install\n\nFollowing commands will download Airavata MFT into your machine and start the MFT service.\n```\npip3 install airavata-mft-cli\nmft init\n```\n\n> If the installer failed for M1 and M2 Macs complaining about grpcio installation. Follow the solution mentioned in [here](https://github.com/apache/airavata-mft/issues/71). You might have to uninstall already installed grpcio and grpcio-tools distributions first.\n> For other common installation issues, please refer to the [troubleshooting section](https://github.com/apache/airavata-mft#common-issues).\n\nTo stop MFT after using\n\n```\nmft stop\n```\n\n\n### Registering Storages\n\nFirst you need to register your storage endpoints into MFT in order to access them. Registering storage is an interactive process and you can easily register those without prior knowledge\n\n```\nmft storage add\n```\n\nThis will ask the type of storage you need and credentials to access those storages. To list already added storages, you can run\n\n```\nmft storage list\n```\n### Accessing Data in Storages\n\nIn Airavata MFT, we provide a unified interface to access the data in any storage. Users can access data in storages just as they access data in their computers. MFT converts user queries into storage specific data representations (POSIX, Block, Objects, ..) internally\n\n```\nmft ls <storage name>\nmft ls <storage name>/<resource path>\n```\n\n### Moving Data between Storages\n\nCopying data between storages are simple as copying data between directories of local machine for users. MFT takes care of network path optimizations, parallel data path selections and selections or creations of suitable transfer agents.\n\n ```\n mft cp <source storage name>/<path> <destination storage name>/<path> \n ```\nMFT is capable of auto detecting directory copying and file copying based on the path given.\n\n### Troubleshooting and Issue Reporting\n\nThis is our very first attempt release Airavata MFT for community usage and there might be lots of corner cases that we have not noticed. All the logs of MFT service are available in ```~/.mft/Standalone-Service-0.01/logs/airavata.log```. If you see any error while using MFT, please report that in our Github issue page and we will respond as soon as possible. We really appreciate your contribution as it will greatly help to improve the stability of the product.\n\n#### Common issues\n\n- Following error can be noticed if you have a python version which is less than 3.10\n```\n  ERROR: Could not find a version that satisfies the requirement airavata-mft-cli (from versions: none)\n  ERROR: No matching distribution found for airavata-mft-cli\n```\nIf the Error still occurs after installing the right python version, try creating a virtual environemnt\n```\npython3.10 -m venv venv\nsource venv/bin/activate\npip install airavata-mft-cli\n```\n  \n',
    'author': 'Dimuthu Wannipurage',
    'author_email': 'dwannipu@iu.edu',
    'maintainer': 'Apache Airavata Developers',
    'maintainer_email': 'dev@apache.airavata.org',
    'url': 'https://github.com/apache/airavata-mft',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
