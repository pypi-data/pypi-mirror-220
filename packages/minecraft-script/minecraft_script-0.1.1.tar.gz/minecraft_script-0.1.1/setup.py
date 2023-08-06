from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.1'
DESCRIPTION = 'Minecraft Script Programming language'
LONG_DESCRIPTION = 'Python library to allow running .mcs (Minecraft Script) files and building entire datapacks from them.'

# Setting up
setup(
    name="minecraft_script",
    version=VERSION,
    author="Joyful-Bard",
    author_email="<thisis@notarealemail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['ply'],
    keywords=['minecraft', 'mc', 'script', 'language'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)