# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tweetopic']

package_data = \
{'': ['*']}

install_requires = \
['deprecated>=1.2.0',
 'joblib>=1.1.0',
 'numba>=0.56.0',
 'numpy>=1.19,<1.24.0',
 'scikit-learn>=1.1.1,<1.3.0']

setup_kwargs = {
    'name': 'tweetopic',
    'version': '0.2.2',
    'description': 'Topic modelling over short texts',
    'long_description': '![Logo with text](./docs/_static/icon_w_title.png)\n\n# tweetopic: Blazing Fast Topic modelling for Short Texts\n\n[![PyPI version](https://badge.fury.io/py/tweetopic.svg)](https://pypi.org/project/tweetopic/)\n[![pip downloads](https://img.shields.io/pypi/dm/tweetopic.svg)](https://pypi.org/project/tweetopic/)\n[![python version](https://img.shields.io/badge/Python-%3E=3.7-blue)](https://github.com/centre-for-humanities-computing/tweetopic)\n[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-black)](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)\n<br>\n![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)\n![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white)\n![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)\n\n:zap: Blazing Fast topic modelling over short texts utilizing the power of :1234: Numpy and :snake: Numba.\n\n## Features\n\n- Fast :zap:\n- Scalable :collision:\n- High consistency and coherence :dart:\n- High quality topics :fire:\n- Easy visualization and inspection :eyes:\n- Full scikit-learn compatibility :nut_and_bolt:\n\n## 🛠 Installation\n\nInstall from PyPI:\n\n```bash\npip install tweetopic\n```\n\n## 👩\u200d💻 Usage ([documentation](https://centre-for-humanities-computing.github.io/tweetopic/))\n\nTrain your a topic model on a corpus of short texts:\n\n```python\nfrom tweetopic import DMM\nfrom sklearn.feature_extraction.text import CountVectorizer\nfrom sklearn.pipeline import Pipeline\n\n# Creating a vectorizer for extracting document-term matrix from the\n# text corpus.\nvectorizer = CountVectorizer(min_df=15, max_df=0.1)\n\n# Creating a Dirichlet Multinomial Mixture Model with 30 components\ndmm = DMM(n_components=30, n_iterations=100, alpha=0.1, beta=0.1)\n\n# Creating topic pipeline\npipeline = Pipeline([\n    ("vectorizer", vectorizer),\n    ("dmm", dmm),\n])\n```\n\nYou may fit the model with a stream of short texts:\n\n```python\npipeline.fit(texts)\n```\n\nTo investigate internal structure of topics and their relations to words and indicidual documents we recommend using [topicwizard](https://github.com/x-tabdeveloping/topic-wizard).\n\nInstall it from PyPI:\n\n```bash\npip install topic-wizard\n```\n\nThen visualize your topic model:\n\n```python\nimport topicwizard\n\ntopicwizard.visualize(pipeline=pipeline, corpus=texts)\n```\n\n![topicwizard visualization](docs/_static/topicwizard.png)\n\n## 🎓 References\n\n- Yin, J., & Wang, J. (2014). A Dirichlet Multinomial Mixture Model-Based Approach for Short Text Clustering. _In Proceedings of the 20th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (pp. 233–242). Association for Computing Machinery._\n',
    'author': 'Márton Kardos',
    'author_email': 'power.up1163@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0',
}


setup(**setup_kwargs)
