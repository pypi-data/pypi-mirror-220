from setuptools import setup

with open('README.md', 'r') as arq:
    readme = arq.read()

setup(name='anyBoNett',
    version='0.0.4',
    license='MIT License',
    author='AnyBoSOFT',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='bidjorys@gmail.com',
    keywords='ytl',
    description=u'uma biblioteca pra facilitar pesquisas',
    packages=['anybonett'],
    install_requires=['wikipedia'],)