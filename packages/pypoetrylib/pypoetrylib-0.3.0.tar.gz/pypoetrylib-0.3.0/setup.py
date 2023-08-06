# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['mymodule']
install_requires = \
['requests>=2.28.1,<3.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'urllib3>=1.26.12,<2.0.0']

setup_kwargs = {
    'name': 'pypoetrylib',
    'version': '0.3.0',
    'description': 'Python Poetry lib sample',
    'long_description': "# Confluent CLI Wraper for Python\n\nSimple wrapper library to Confluent CLI\n\n\n## Get started\n\n```bash\npoetry add python-confluent-cli-wrapper\n```\n\n```python\nfrom confluent.cli.wrapper.environment import Environment\nfrom confluent.cli.wrapper.kafka_cluster import KafkaCluster\nfrom confluent.cli.wrapper.kafka_topic import KafkaTopic\nfrom confluent.cli.wrapper.session import login\nfrom confluent.cli.wrapper.utils.parsers import OutputEnum\n\nenvironment=Environment()\nkafka_cluster=KafkaCluster()\nkafka_topic=KafkaTopic()\n\nlogin()\n\nenvironment.list()\n\nkafka_cluster.list()  # eq '--all' argument\n\n```\n",
    'author': 'Alan S. Ferreira',
    'author_email': 'alansferreira1984@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alansferreira/py-poetry-lib',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
