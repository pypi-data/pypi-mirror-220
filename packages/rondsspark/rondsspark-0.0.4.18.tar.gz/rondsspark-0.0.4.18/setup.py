from setuptools import setup, find_packages

# noinspection SpellCheckingInspection
setup(
    name='rondsspark',
    version='0.0.4.18',
    description='ronds spark sdk',
    author='dongyunlong',
    author_email='yunlong.dong@ronds.com.cn',
    install_requires=['cassandra-driver==3.28.0',
                      'pandas==1.1.5',
                      'pyYAML==6.0',
                      'confluent-kafka==2.1.1',
                      'schedule==1.1.0',
                      'wheel==0.37.1',
                      'findspark==2.0.1',
                      'importlib_resources==5.4.0',
                      ],
    package_data={
        '': ['logging_config.yml'],
    },
    packages=find_packages(),
    license='apache 3.0',
)
