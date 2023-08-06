# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conjugate']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['matplotlib>=3.6.2,<4.0.0', 'numpy>=1.24.3,<2.0.0', 'pandas', 'scipy<1.10.0']

setup_kwargs = {
    'name': 'conjugate-models',
    'version': '0.1.2',
    'description': 'Bayesian Conjugate Models in Python',
    'long_description': '# conjugate priors\nBayesian conjugate models in Python\n\n\n## Installation\n\n```bash \npip install conjugate-models\n```\n\n## Basic Usage\n\n```python \nfrom conjugate.distributions import Beta, BetaBinomial\nfrom conjugate.models import binomial_beta, binomial_beta_posterior_predictive\n\n# Observed Data\nX = 4\nN = 10\n\n# Analytics\nprior = Beta(1, 1)\nprior_predictive: BetaBinomial = binomial_beta_posterior_predictive(n=N, beta=prior)\n\nposterior: Beta = binomial_beta(n=N, x=X, beta_prior=prior)\nposterior_predictive: BetaBinomial = binomial_beta_posterior_predictive(n=N, beta=posterior) \n\n# Figure\nimport matplotlib.pyplot as plt\n\nfig, axes = plt.subplots(ncols=2)\n\nax = axes[0]\nax = posterior.plot_pdf(ax=ax, label="posterior")\nprior.plot_pdf(ax=ax, label="prior")\nax.axvline(x=X/N, color="black", ymax=0.05, label="MLE")\nax.set_title("Success Rate")\nax.legend()\n\nax = axes[1]\nposterior_predictive.plot_pmf(ax=ax, label="posterior predictive")\nprior_predictive.plot_pmf(ax=ax, label="prior predictive")\nax.axvline(x=X, color="black", ymax=0.05, label="Sample")\nax.set_title("Number of Successes")\nax.legend()\nplt.show()\n```\n\n<img height=400 src="docs/images/binomial-beta.png" title="Binomial Beta Comparison">\n\nMore examples on in the [documentation](https://wd60622.github.io/conjugate/).',
    'author': 'Will Dean',
    'author_email': 'wd60622@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://wd60622.github.io/conjugate/',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
