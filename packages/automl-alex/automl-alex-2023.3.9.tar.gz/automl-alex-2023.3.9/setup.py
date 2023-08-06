# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['automl_alex', 'automl_alex.models']

package_data = \
{'': ['*']}

install_requires = \
['catboost>=1.1.1,<2.0.0',
 'category-encoders>=2.6.0,<3.0.0',
 'lightgbm>=3.3.5,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'nbformat>=5.7.3,<6.0.0',
 'numpy>=1.24.2,<2.0.0',
 'optuna-dashboard>=0.8.1,<0.9.0',
 'optuna>=3.1.0,<4.0.0',
 'pandas>=1.5.3,<2.0.0',
 'psutil>=5.9.4,<6.0.0',
 'scikit-learn>=1.2.2,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'tqdm>=4.65.0,<5.0.0',
 'xgboost>=1.7.4,<2.0.0']

setup_kwargs = {
    'name': 'automl-alex',
    'version': '2023.3.9',
    'description': 'State-of-the art Automated Machine Learning python library for Tabular Data',
    'long_description': '\n\n<h3 align="center">AutoML Alex</h3>\n\n<div align="center">\n\n[![Downloads](https://pepy.tech/badge/automl-alex)](https://pepy.tech/project/automl-alex)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/automl-alex)\n![PyPI](https://img.shields.io/pypi/v/automl-alex)\n[![CodeFactor](https://www.codefactor.io/repository/github/alex-lekov/automl_alex/badge)](https://www.codefactor.io/repository/github/alex-lekov/automl_alex)\n[![Telegram](https://img.shields.io/badge/chat-on%20Telegram-2ba2d9.svg)](https://t.me/automlalex)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)\n\n</div>\n\n---\n\n<p align="center"> State-of-the art Automated Machine Learning python library for Tabular Data</p>\n\n## Works with Tasks:\n\n-   [x] Binary Classification\n\n-   [x] Regression\n\n-   [ ] Multiclass Classification (in progress...)\n\n### Benchmark Results\n<img width=800 src="https://github.com/Alex-Lekov/AutoML-Benchmark/blob/master/img/Total_SUM.png" alt="bench">\n\nThe bigger, the better   \nFrom [AutoML-Benchmark](https://github.com/Alex-Lekov/AutoML-Benchmark/) \n\n### Scheme\n<img width=800 src="https://github.com/Alex-Lekov/AutoML_Alex/blob/develop/examples/img/shema.png" alt="scheme">\n\n\n# Features\n\n- Automated Data Clean (Auto Clean)\n- Automated **Feature Engineering** (Auto FE)\n- Smart Hyperparameter Optimization (HPO)\n- Feature Generation\n- Feature Selection\n- Models Selection\n- Cross Validation\n- Optimization Timelimit and EarlyStoping\n- Save and Load (Predict new data)\n\n\n# Installation\n\n```python\npip install automl-alex\n```\n\n# Docs\n[DocPage](https://alex-lekov.github.io/AutoML_Alex/)\n\n# 🚀 Examples\n\nClassifier:\n```python\nfrom automl_alex import AutoMLClassifier\n\nmodel = AutoMLClassifier()\nmodel.fit(X_train, y_train, timeout=600)\npredicts = model.predict(X_test)\n```\n\nRegression:\n```python\nfrom automl_alex import AutoMLRegressor\n\nmodel = AutoMLRegressor()\nmodel.fit(X_train, y_train, timeout=600)\npredicts = model.predict(X_test)\n```\n\nDataPrepare:\n```python\nfrom automl_alex import DataPrepare\n\nde = DataPrepare()\nX_train = de.fit_transform(X_train)\nX_test = de.transform(X_test)\n```\n\nSimple Models Wrapper:\n```python\nfrom automl_alex import LightGBMClassifier\n\nmodel = LightGBMClassifier()\nmodel.fit(X_train, y_train)\npredicts = model.predict_proba(X_test)\n\nmodel.opt(X_train, y_train,\n    timeout=600, # optimization time in seconds,\n    )\npredicts = model.predict_proba(X_test)\n```\n\nMore examples in the folder ./examples:\n\n- [01_Quick_Start.ipynb](https://github.com/Alex-Lekov/AutoML_Alex/blob/master/examples/01_Quick_Start.ipynb)  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](http://colab.research.google.com/github/Alex-Lekov/AutoML_Alex/blob/master/examples/01_Quick_Start.ipynb)\n- [02_Data_Cleaning_and_Encoding_(DataPrepare).ipynb](https://github.com/Alex-Lekov/AutoML_Alex/blob/master/examples/02_Data_Cleaning_and_Encoding_(DataPrepare).ipynb)  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](http://colab.research.google.com/github/Alex-Lekov/AutoML_Alex/blob/master/examples/02_Data_Cleaning_and_Encoding_(DataPrepare).ipynb)\n- [03_Models.ipynb](https://github.com/Alex-Lekov/AutoML_Alex/blob/master/examples/03_Models.ipynb)  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](http://colab.research.google.com/github/Alex-Lekov/AutoML_Alex/blob/master/examples/03_Models.ipynb)\n- [04_ModelsReview.ipynb](https://github.com/Alex-Lekov/AutoML_Alex/blob/master/examples/04_ModelsReview.ipynb)  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](http://colab.research.google.com/github/Alex-Lekov/AutoML_Alex/blob/master/examples/04_ModelsReview.ipynb)\n- [05_BestSingleModel.ipynb](https://github.com/Alex-Lekov/AutoML_Alex/blob/master/examples/05_BestSingleModel.ipynb)  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](http://colab.research.google.com/github/Alex-Lekov/AutoML_Alex/blob/master/examples/05_BestSingleModel.ipynb)\n- [Production Docker template](https://github.com/Alex-Lekov/AutoML_Alex/blob/master/examples/prod_sample)\n\n\n\n# What\'s inside\n\nIt integrates many popular frameworks:\n- scikit-learn\n- XGBoost\n- LightGBM\n- CatBoost\n- Optuna\n- ...\n\n\n# Works with Features\n\n-   [x] Categorical Features\n\n-   [x] Numerical Features\n\n-   [x] Binary Features\n\n-   [ ] Text\n\n-   [ ] Datetime\n\n-   [ ] Timeseries\n\n-   [ ] Image\n\n\n# Note\n\n- **With a large dataset, a lot of memory is required!**\nLibrary creates many new features. If you have a large dataset with a large number of features (more than 100), you may need a lot of memory.\n\n\n# Realtime Dashboard\nWorks with [optuna-dashboard](https://github.com/optuna/optuna-dashboard)\n\n<img width=800 src="https://github.com/Alex-Lekov/AutoML_Alex/blob/develop/examples/img/dashboard.gif" alt="Dashboard">\n\nRun\n```console\n$ optuna-dashboard sqlite:///db.sqlite3\n```\n\n# Road Map\n\n-   [x] Feature Generation\n\n-   [x] Save/Load and Predict on New Samples\n\n-   [x] Advanced Logging\n\n-   [x] Add opt Pruners\n\n-   [x] Docs Site\n\n-   [ ] DL Encoders\n\n-   [ ] Add More libs (NNs)\n\n-   [ ] Multiclass Classification\n\n-   [ ] Build pipelines\n\n\n# Contact\n\n[Telegram Group](https://t.me/automlalex)\n\n',
    'author': 'Alex-Lekov',
    'author_email': '61644712+Alex-Lekov@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
