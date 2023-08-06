from setuptools import setup, find_packages


VERSION = '1.0.3'
DESCRIPTION = '简化数据库连接、时间处理及log声明'
LONG_DESCRIPTION = '数据库：mongo、mysql、oracle、xugu；时间：格式化、转换、计算；log：声明'

# 配置
setup(
    name='TiamoTools',
    version=VERSION,
    author='wyl',
    author_email='<321081840@qq.com>',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    python_requires='>=3.8',
    requires=[
        'PyMySQL',
        'pymongo',
        'cx_Oracle'
    ],
    install_requires=[
        'PyMySQL>=1.0.2',
        'pymongo>=3.8.0',
        'cx_Oracle>=8.3.0'
    ],
    keywords=['python', 'super', 'tools'],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8'
    ]
)

