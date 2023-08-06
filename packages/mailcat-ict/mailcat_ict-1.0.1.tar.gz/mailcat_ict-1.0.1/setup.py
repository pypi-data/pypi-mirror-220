from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='mailcat_ict',
    version='1.0.1',
    description='My Python package ICT ',
    author='joshua ict',
    author_email='devops@italiancyberteam.it',
    url='https://github.com/devops@italiancyberteam.it/my_package',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib'] +         required
    
)