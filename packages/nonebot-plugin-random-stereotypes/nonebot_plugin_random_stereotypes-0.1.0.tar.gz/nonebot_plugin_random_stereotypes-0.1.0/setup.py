# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_random_stereotypes']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.1.3,<3.0.0', 'nonebot2>=2.0.0rc3,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-random-stereotypes',
    'version': '0.1.0',
    'description': '基于Nonebot2的发病语录插件',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot_plugin_random_stereotypes\n\n_✨ NoneBot 发病语录 ✨_\n\n\n<a href="https://github.com/Ikaros-521/nonebot_plugin_random_stereotypes/stargazers">\n    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Ikaros-521/nonebot_plugin_random_stereotypes?color=%09%2300BFFF&style=flat-square">\n</a>\n<a href="https://github.com/Ikaros-521/nonebot_plugin_random_stereotypes/issues">\n    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Ikaros-521/nonebot_plugin_random_stereotypes?color=Emerald%20green&style=flat-square">\n</a>\n<a href="https://github.com/Ikaros-521/nonebot_plugin_random_stereotypes/network">\n    <img alt="GitHub forks" src="https://img.shields.io/github/forks/Ikaros-521/nonebot_plugin_random_stereotypes?color=%2300BFFF&style=flat-square">\n</a>\n<a href="./LICENSE">\n    <img src="https://img.shields.io/github/license/Ikaros-521/nonebot_plugin_random_stereotypes.svg" alt="license">\n</a>\n<a href="https://pypi.python.org/pypi/nonebot_plugin_random_stereotypes">\n    <img src="https://img.shields.io/pypi/v/nonebot_plugin_random_stereotypes.svg" alt="pypi">\n</a>\n<a href="https://www.python.org">\n    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n</a>\n\n</div>\n\n## 📖 介绍\n\n随机返回一条在互联网上收录一些有趣的发病语录（主要针对VTB）  \n如果有需要补充的可以提交issue进行追加，侵删。  \n\n## 🔧 开发环境\nNonebot2：2.0.0rc3  \npython：3.8.13  \n操作系统：Windows10（Linux兼容性问题不大）  \n编辑器：VS Code  \n\n## 💿 安装  \n\n### 1. nb-cli安装（推荐）\n\n在你bot工程的文件夹下，运行cmd（运行路径要对啊），执行nb命令安装插件，插件配置会自动添加至配置文件  \n```\nnb plugin install nonebot_plugin_random_stereotypes\n```\n\n### 2. 本地安装\n\n将项目clone到你的机器人插件下的对应插件目录内（一般为机器人文件夹下的`src/plugins`），然后把`nonebot_plugin_random_stereotypes`文件夹里的内容拷贝至上一级目录即可。  \nclone命令参考（得先装`git`，懂的都懂）：\n```\ngit clone https://github.com/Ikaros-521/nonebot_plugin_random_stereotypes.git\n``` \n也可以直接下载压缩包到插件目录解压，然后同样提取`nonebot_plugin_random_stereotypes`至上一级目录。  \n目录结构： ```你的bot/src/plugins/nonebot_plugin_random_stereotypes/__init__.py```  \n\n\n### 3. pip安装\n```\npip install nonebot_plugin_random_stereotypes\n```  \n打开 nonebot2 项目的 ```bot.py``` 文件, 在其中写入  \n```nonebot.load_plugin(\'nonebot_plugin_random_stereotypes\')```  \n当然，如果是默认nb-cli创建的nonebot2的话，在bot路径```pyproject.toml```的```[tool.nonebot]```的```plugins```中添加```nonebot_plugin_random_stereotypes```即可  \npyproject.toml配置例如：  \n``` \n[tool.nonebot]\nplugin_dirs = ["src/plugins"]\nplugins = ["nonebot_plugin_random_stereotypes"]\n``` \n\n### 更新版本\n```\nnb plugin update nonebot_plugin_random_stereotypes\n```\n\n## 🔧 配置\n\n不需要喵\n\n\n## 🎉 功能\n随机生成下标获取本地`data.py`中的一条语录，凭借传入的字符串返回结果。\n\n## 👉 命令\n\n### /发病\n命令结构：```/发病 [发病对象]```  \n例如：```/发病 测试```  \nbot返回内容：  \n`电梯里遇到了测试，她按了八层，呵真会暗示，她八层有点喜欢我`  \n\n\n## ⚙ 拓展\n自定义发病语录，修改`data.py`文件，在数组中添加语句即可，对象名用 `{target_name}` 代替，注意格式！  \n\n## 📝 更新日志\n\n<details>\n<summary>展开/收起</summary>\n\n### 0.0.1\n\n- 插件初次发布  \n\n### 0.0.2\n\n- 追加发病语录数据  \n\n</details>\n\n## 致谢\n- [nonebot-plugin-template](https://github.com/A-kirami/nonebot-plugin-template)\n\n## 项目打包上传至pypi\n\n官网：https://pypi.org，注册账号，在系统用户根目录下创建`.pypirc`，配置  \n``` \n[distutils] \nindex-servers=pypi \n \n[pypi] repository = https://upload.pypi.org/legacy/ \nusername = 用户名 \npassword = 密码\n```\n\n### poetry\n\n```\n# 参考 https://www.freesion.com/article/58051228882/\n# poetry config pypi-token.pypi\n\n# 1、安装poetry\npip install poetry\n\n# 2、初始化配置文件（根据提示填写）\npoetry init\n\n# 3、微调配置文件pyproject.toml\n\n# 4、运行 poetry install, 可生成 “poetry.lock” 文件（可跳过）\npoetry install\n\n# 5、编译，生成dist\npoetry build\n\n# 6、发布(poetry config pypi-token.pypi 配置token)\npoetry publish\n\n```\n\n### twine\n\n```\n# 参考 https://www.cnblogs.com/danhuai/p/14915042.html\n#创建setup.py文件 填写相关信息\n\n# 1、可以先升级打包工具\npip install --upgrade setuptools wheel twine\n\n# 2、打包\npython setup.py sdist bdist_wheel\n\n# 3、可以先检查一下包\ntwine check dist/*\n\n# 4、上传包到pypi（需输入用户名、密码）\ntwine upload dist/*\n```\n',
    'author': 'Ikaros',
    'author_email': '327209194@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Ikaros-521/nonebot_plugin_random_stereotypes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
