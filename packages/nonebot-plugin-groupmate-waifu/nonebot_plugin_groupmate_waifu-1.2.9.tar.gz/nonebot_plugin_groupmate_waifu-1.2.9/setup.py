from setuptools import setup,find_namespace_packages

setup(
name='nonebot_plugin_groupmate_waifu',
version='1.2.9',
description='娶群友',
#long_description=open('README.md','r').read(),
author='karisaya',
author_email='1048827424@qq.com',
license='MIT license',
include_package_data=True,
packages=find_namespace_packages(include=["nonebot_plugin_groupmate_waifu"]),
platforms='all',
install_requires=["nonebot2","nonebot-adapter-onebot","nonebot_plugin_apscheduler","pil_utils"],
url='https://github.com/KarisAya/nonebot_plugin_groupmate_waifu',
)