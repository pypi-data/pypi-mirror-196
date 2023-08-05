# __Author__ = "Pranav Chandran"
# __Date__ = 08-03-2023
# __Time__ = 11:33
# __FileName__ = setup.py
from setuptools import setup, find_packages

setup(
    name='console_gpt',
    version='0.1', #updated version
    author='Pranav Chandran',
    author_email='pranav.chandran@gmail.com',
    description='A package to interact with ChatbotGPT',
    long_description=open('README.md').read(),
    packages=find_packages(),

    url='',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
