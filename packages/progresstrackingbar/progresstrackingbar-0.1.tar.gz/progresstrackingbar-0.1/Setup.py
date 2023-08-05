from setuptools import setup

VERSION = '0.1'
DESCRIPTION = 'Track Progress of Your Script Execution'
LONG_DESCRIPTION = 'A package that helps you track the execution of your pyton script by showing a progress bar.'

setup(
    name="progresstrackingbar",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Lone Walker",
    author_email="lonewalkerns@gmail.com",
    license='MIT',
    install_requires=["tqdm"],
    keywords='progress',
    classifiers= [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ]
)