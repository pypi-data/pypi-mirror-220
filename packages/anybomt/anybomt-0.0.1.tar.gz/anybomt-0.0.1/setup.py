from setuptools import setup


with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='anybomt',
    version='0.0.1',
    license='MIT License',
    author='AnyBoMath',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='bidjorys@gmail.com',
    keywords='math, sympy, numpy, anybomt, Anybo',
    description=u'Uma biblioteca para facilitar sua jornada em matematica',
    packages=[''],
    install_requires=['requests'],)