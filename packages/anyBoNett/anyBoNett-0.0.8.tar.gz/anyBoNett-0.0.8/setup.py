from setuptools import setup


with open('README.md', 'r') as arq:
    readme = arq.read()

setup(name='anyBoNett',
    version='0.0.8',
    license='MIT License',
    author='AnyBoLIB',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='bidjorys@gmail.com',
    keywords='ytl, anybonett, net, anybonet, ',
    description=u'uma biblioteca pra facilitar pesquisas',
    packages=['anybonett'],
    install_requires=['wikipedia'],)