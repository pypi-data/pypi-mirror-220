
from setuptools import setup, find_packages

version = '2.0.1'
url = 'https://github.com/pmaigutyak/mp-shop-offers'


setup(
    name='django-mp-shop-offers',
    version=version,
    description='Django shop offers app',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT'
)
