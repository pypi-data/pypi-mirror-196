# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_chatpdf']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0',
 'nonebot-adapter-onebot>=2.2.1,<3.0.0',
 'nonebot2>=2.0.0rc3,<3.0.0',
 'numpy>=1.24.2,<2.0.0',
 'openai>=0.27.0,<0.28.0']

setup_kwargs = {
    'name': 'nonebot-plugin-chatpdf',
    'version': '0.1.0',
    'description': 'A nonebot plugin for chatpdf',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-chatpdf\n</div>\n\n# 介绍\n- 本插件灵感来源于最近很火的[chatpdf](https://www.chatpdf.com)。\n- 将需要分析的论文/阅读材料分次发送给机器人，机器人可以对其进行存储分析，然后你可以向其提问有关文章内容、文章概要、对于文章的思考等问题\n- 本插件参考了[chatpdf-minimal-demo\n：chatpdf 的最小实现，和文章对话 ](https://github.com/postor/chatpdf-minimal-demo) 和[How to Code a Project like ChatPDF?](https://postor.medium.com/how-to-code-a-project-like-chatpdf-e40441cb4168)\n# 安装\n\n* 手动安装\n  ```\n  git clone https://github.com/Alpaca4610/nonebot_plugin_chatpdf.git\n  ```\n\n  下载完成后在bot项目的pyproject.toml文件手动添加插件：\n\n  ```\n  plugin_dirs = ["xxxxxx","xxxxxx",......,"下载完成的插件路径/nonebot-plugin-chatpdf"]\n  ```\n* 使用 pip\n  ```\n  pip install nonebot-plugin-chatgpt-chatpdf\n  ```\n\n# 配置文件\n\n在Bot根目录下的.env文件中追加如下内容：\n\n```\nOPENAI_API_KEY = key\n```\n\n可选内容：\n```\nOPENAI_HTTP_PROXY = "http://127.0.0.1:8001"    # 设置代理解决OPENAI的网络问题\n```\n\n\n# 使用方法\n\n- /start (使用该命令启动chatpdf文章分析功能)\n- /add (启动之后，在该命令后面添加文章的内容，由于QQ的发送字数限制，可能需要将文章分成若干个可以发送的片段，然后依次使用该命令发送)\n- /stop (文章添加完成之后，使用该命令告知机器人，机器人开始分析文章并使用OpenAI的API生成embedding文件)\n- /chat_pdf (文章分析完成后，使用该命令后面接需要提问的关于文章的问题，机器人会给出答案)\n- /delete_all (删除所有缓存文件)\n\n# 注意事项\n- 分析过程中会在机器人的data文件夹下产生embedding缓存文件，注意缓存占用\n- 每次调用/start命令时，都会清除调用者以前的embedding缓存文件\n- 插件加载时会删除所有用户的embedding缓存文件\n',
    'author': 'Alpaca',
    'author_email': 'alpaca@bupt.edu.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
