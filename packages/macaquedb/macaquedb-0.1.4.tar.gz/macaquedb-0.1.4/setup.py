from setuptools import setup, find_packages

setup(
    name='macaquedb',
    version='0.1.4',
    description='SQLite Database interface for PRIME-DE data',
    author='Sam Alldritt',
    author_email='samuel.alldritt@childmind.org',
    url='https://github.com/samalldritt/MacaqueDB',
    packages=find_packages(),
    install_requires=[
        'sqlite==3.40.1'
    ]
)
