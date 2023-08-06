from setuptools import setup, find_packages

# Lire le contenu du fichier README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='markdown_analysis',
    version='0.0.2',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='A library to analyze markdown files',
    author='yannbanas',
    author_email='yannbanas@gmail.com',
    url='https://github.com/yannbanas/mrkdwn_analysis',
    packages=find_packages(),
    install_requires=[
        # list your dependencies here
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
)