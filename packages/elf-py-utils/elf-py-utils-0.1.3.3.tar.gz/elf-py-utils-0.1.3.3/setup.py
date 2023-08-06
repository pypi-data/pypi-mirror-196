# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elf_py_utils',
 'elf_py_utils.CodeGen',
 'elf_py_utils.constants',
 'elf_py_utils.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'elf-py-utils',
    'version': '0.1.3.3',
    'description': '',
    'long_description': '# elf-py-utils项目说明\n\n> 小精灵Python工具包\n\n## 前言\n\n- 目标使用者：从事运维工程师、后端开发工程师等相关岗位，并熟悉python基础语法规则\n- 本包的工作：在前人的基础上，对当前已有的工具包进行二次封装，并提供一个统一的配置文件来进行配置管理，意图提供一个类似于Spring Boot的框架方便使用\n\n## 当前功能\n\n### Redis工具类\n\n#### 配置示例\n\n通过配置文件，实现一种代码连接多种Redis部署方式\n\n```yaml\nredis:\n  # 需要在同一命名空间中定义redis的服务发现\n  # redis部署方式 单节点-single 集群模式-cluster 哨兵模式-sentinel\n  type: cluster\n  single:\n    host_port: redis\n  cluster:\n    host_port: redis-cluster:6379\n  sentinel:\n    db: 1\n    password: password\n    service_name: mymaster\n    host_port: redis-sentinel-01:6379,redis-sentinel-02:6379,redis-sentinel-03:6379\n```\n\n### 调用\n\n```python\nfrom elf_py_utils import RedisUtil\n\nredis = RedisUtil.connect_redis()\n```\n\n### 依赖\n\n```txt\nredis==3.5.3\nredis-py-cluster==2.1.3\n```\n\n\n',
    'author': 'TreeOfWord',
    'author_email': 'li_163jx@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
