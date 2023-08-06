# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xuexitong_fileloads']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xuexitong-fileloads',
    'version': '0.1.1',
    'description': '用来下载学习通课件资料',
    'long_description': '# chaoxingxuexitong-fileloads\n 下载学习通课件视频\n觉得输入太多麻烦可以走极简通道，此时记得至少改个基本目录和链接，其他参数自定义，不改按默认参数。\n使用方法代码里写了不少\n只运行代码2即可，代码已作为模块导入\n\n大致流程依次：\n\n\n模式选择0自定义，1极简:\n\n\nbasedir = input(\'基本目录:\')\nurl = input(\'url:\')\n注：basedir = \'学习通资料\\\\课程\\\\音频\\\\\'\nurl = "小节链接，到enc即可"\n\n\nprint(\'请扫码登录继续,请在20秒内完成,如有第二次请忽略并再等待20秒\')\nprint(\'获取各章链接中...\')\n\n\nstart = int(input(\'输入循环开始节:\'))\nend = int(input(\'输入循环结束节，不设定则输入0:\'))\n\n\nfile_class = int(input(\'输入循环下载类型2全部1pdf0mp4:\'))\n\n\nnum每一节每次爬取的最后一页，视情况而定，一般不会超过3页，一般是1到2页，其中夹杂着少数的3页，懒省事取最大全部遍历即可\nbnum = int(input(\'节内页始0：\'))\nnum = int(input(\'节内页终2：\'))\n',
    'author': 'ziru-w',
    'author_email': '77319678+ziru-w@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
