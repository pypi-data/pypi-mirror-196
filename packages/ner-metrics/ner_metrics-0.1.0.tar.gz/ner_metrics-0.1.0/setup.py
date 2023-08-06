from setuptools import setup
# https://towardsdatascience.com/create-your-own-python-package-and-publish-it-into-pypi-9306a29bc116
setup(
    name='ner_metrics',
    version='0.1.0',    
    description='A simple Python snippets for NER evaluation',
    url='https://github.com/PL97/NER_eval',
    author='Le Peng',
    author_email='peng0347@umn.edu',
    license='MIT',
    packages=['ner_metrics'],
    install_requires=['numpy']
)