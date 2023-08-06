# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['selenium_fetch']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.6,<2.0.0', 'selenium>=4.8.2,<5.0.0']

setup_kwargs = {
    'name': 'selenium-fetch',
    'version': '0.1.1',
    'description': 'access `fetch()` with selenium!',
    'long_description': '# selenium-fetch\n\nA simple module that lets you access the `fetch` API with selenium!\n\n> _Why do I make this? just annoyed with cloudflare. It works best with [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)._\n\n## Installation\n\n```\npip install selenium-fetch undetected-chromedriver\n```\n\n## Example\n\n```python\nfrom undetected_chromedriver import Chrome\nfrom selenium_fetch import fetch, Options, get_browser_user_agent\n\nLOGIN_PAGE_URL = "https://smekdong.com/login"\nLOGIN_API_URL = "https://smekdong.com/api/login"\ndriver = Chrome(headless=False)\ndriver.get(LOGIN_PAGE_URL)\npost_data = {\n    \'username\': \'blaabla\',\n    \'password\': \'xxxx\'\n}\nheaders = {\n    "user-agent": get_browser_user_agent(driver),\n    \'origin\': \'https://smekdong.com\',\n    \'referer\': \'https://smekdong.com/\',\n}\noptions = Options(method="POST", headers=headers, body=post_data)\nresponse = fetch(driver, LOGIN_API_URL, options)\nprint("Response:", response)\n```\n',
    'author': 'aprilahijriyan',
    'author_email': 'hijriyan23@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aprilahijriyan/selenium-fetch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
