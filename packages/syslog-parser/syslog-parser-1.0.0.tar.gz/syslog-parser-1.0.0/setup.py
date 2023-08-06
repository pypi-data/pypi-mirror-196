from setuptools import setup

setup(
    name='syslog-parser',
    version='1.0.0',
    description='A simple syslog parser',
    py_modules=['syslog_parser'],
    install_requires=['pyparsing'],
    entry_points={
        'console_scripts': [
            'syslog-parser=syslog_parser:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
