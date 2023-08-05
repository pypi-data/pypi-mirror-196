# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['celery_prometheus']

package_data = \
{'': ['*']}

install_requires = \
['celery>=4']

setup_kwargs = {
    'name': 'celery-prometheus',
    'version': '1.0.0',
    'description': 'Celery with your own prometheus metrics',
    'long_description': "# Celery Prometheus\n\nThis module expose the Prometheus HTTP server to expose metrics of your Celery backends.\n\nTo install `celery-prometheus` with pip, use the command:\n\n```\npip install celery-prometheus\n```\n\nWith Poetry:\n\n```\npoetry add celery-prometheus\n```\n\n## Usage\n\nTo setup `celery-prometheus` to your backend, simply call the method `add_prometheus_option`\nafter the init of the `Celery` object.\n\nExample:\n\n```python\n\nfrom celery import Celery\nfrom celery_prometheus import add_prometheus_option\n\napp = Celery()\nadd_prometheus_option(app)\n\n# Rest of your code ...\n\n```\n\nBefore starting your backend, you will need to expose the `PROMETHEUS_MULTIPROC_DIR` environment\nvariable to indicate which folder the Prometheus Client will use to store the metrics\n(see [Multiprocess Mode (E.g. Gunicorn) of the Promehteus Client documentation](https://github.com/prometheus/client_python#multiprocess-mode-eg-gunicorn)).\n\nTo start and expose the Prometheus HTTP Server, you need to use the `--prometheus-collector-addr`\nargument when starting your Celery backend:\n\n```bash\nexport PROMETHEUS_MULTIPROC_DIR=/var/cache/my_celery_app\ncelery worker -A my_celery_backend.backend --prometheus-collector-addr 0.0.0.0:6543\n```\n\nNow that your backend is started, you can configure your Prometheus scrappers to scrappe your\nCelery backend.\n\n## Contributions\n\nThis project is open to external contributions. Feel free to submit us a\n[Pull request](https://github.com/Gandi/celery-prometheus/pulls) if you want to contribute and\nimprove with us this project.\n\nIn order to maintain an overall good code quality, this project use the following tools:\n\n - [Black](https://github.com/psf/black)\n - [Isort](https://github.com/PyCQA/isort)\n - [Flake8](https://flake8.pycqa.org/en/latest/)\n\nLinting and formatting tools are configured to match the [current default rules of Black](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html).\n\nWe also use [Mypy](https://mypy.readthedocs.io/en/stable/) as a static type checker.\n\nPlease ensure to run these tools before commiting and submiting a Pull request. In case one of\nthese mentionned tools report an error, the CI will automatically fail.\n\nIf you're making your first contribution to this project, please add your name to the\n[contributors list](CONTRIBUTORS.txt).\n\n## License\n\nThis project is released by [Gandi.net](https://www.gandi.net/en) tech team under the\n[BSD-3 license](LICENSE).\n",
    'author': 'Guillaume Gauvrit',
    'author_email': 'guillaume@gandi.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
