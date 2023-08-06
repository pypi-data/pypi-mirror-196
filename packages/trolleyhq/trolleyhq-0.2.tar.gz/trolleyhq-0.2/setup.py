from setuptools import setup

setup (
    name='trolleyhq',
    version='0.2',
    packages=["trolley", "trolley.exceptions"],
    package_data={"paymentrails": ["ssl/*"]},
    install_requires=['requests>=2.13.0'],
    author='Trolley',
    author_email='developer-tools@trolley.com',
    summary='Future home of Trolley Python SDK',
    url='https://www.trolley.com',
    license='',
    long_description='Future home of Trolley Python SDK',
)
