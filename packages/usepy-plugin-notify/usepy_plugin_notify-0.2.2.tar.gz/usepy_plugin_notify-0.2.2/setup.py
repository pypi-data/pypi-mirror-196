# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['notify', 'notify.channels']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0', 'usepy>=0.1.34,<0.2.0']

setup_kwargs = {
    'name': 'usepy-plugin-notify',
    'version': '0.2.2',
    'description': '一个简单可扩展的消息通知库',
    'long_description': '### 一个简单可扩展的消息通知库\n\n<a href="https://pypi.org/project/ml-simple-notify" target="_blank">\n    <img src="https://img.shields.io/pypi/v/ml-simple-notify.svg" alt="Package version">\n</a>\n\n<a href="https://pypi.org/project/ml-simple-notify" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/ml-simple-notify.svg" alt="Supported Python versions">\n</a>\n\n#### 安装\n\n> pip install usepy-plugin-notify\n\n#### 使用\n\n```python\nfrom src.notify import useNotify, channels\n\nnotify = useNotify()\nnotify.add(\n    # 添加多个通知渠道\n    channels.Bark({"token": "xxxxxx"}),\n    channels.Ding({\n        "token": "xxxxx",\n        "at_all": True\n    })\n)\n\nnotify.publish(title="消息标题", content="消息正文")\n\n```\n\n#### 支持的消息通知渠道列表\n\n- Wechat\n- Ding\n- Bark\n- Email\n- Chanify\n- Pushdeer\n- Pushover\n\n#### 自己开发消息通知\n\n```python\nfrom src.notify.channels import BaseChannel\n\n\nclass Custom(BaseChannel):\n    """自定义消息通知"""\n\n    def send(self, *args, **kwargs):\n        ...\n```\n',
    'author': 'miclon',
    'author_email': 'jcnd@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
