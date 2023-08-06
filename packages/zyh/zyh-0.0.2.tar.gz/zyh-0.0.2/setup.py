from setuptools import setup, find_packages
import os

VERSION = '0.0.2'
DESCRIPTION = 'Easily show off amazing scripys by zyh'

setup(
    name="zyh",
    version=VERSION,
    author="zhangyuhan",
    author_email="yhanzh0608@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md',encoding="UTF8").read(),
    packages=find_packages(),
    install_requires=['transformers', 'datasets', 'evaluate', 'peft', 'accelerate', 'gradio', 'optimum',
                      'sentencepiece', 'scikit-learn', 'pandas', 'matplotlib', 'tensorboard', 'rouge', 'nltk',
                      'jupyterlab'],
    keywords=['python', 'nlp', 'show off'],

    entry_points={
    'console_scripts': [
        'zyh = zyh.main:main'
    ]
    },

    license="MIT",
    url="https://github.com/amanyara/zyh",
    scripts=['zyh/setup_test.py'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)