from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cryplimp',
    version='1.35',
    description='cryptography library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['python', 'cryptography', 'encrypt', 'decrypt'],
    author='KingfernJohn',
    author_email='kingfernjohn@gmail.com',
    url='https://github.com/KingfernJohn/cryplimp',
    packages=find_packages(),
    install_requires=[
        'pycryptodome'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)