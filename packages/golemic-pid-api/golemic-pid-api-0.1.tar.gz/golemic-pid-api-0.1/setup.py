from setuptools import setup, find_packages

setup(name='golemic-pid-api',
      version='0.1',
      description='golemic-pid wrapper',
      long_description='Api wrapper for https://api.golemio.cz/v2/pid/docs/openapi/#/.',
      keywords='funniest joke comedy flying circus',
      url='https://github.com/0x216/Prague-Public-Transport-Golemio-API-Wrapper',
      author='0x216',
      author_email='0x216@pm.me',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'requests==2.31.0'
      ],
      include_package_data=False,
      zip_safe=False)
