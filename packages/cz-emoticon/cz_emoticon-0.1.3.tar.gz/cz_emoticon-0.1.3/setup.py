from setuptools import setup

with open('README.md', encoding="utf-8") as f:
    long_description = f.read()

setup(

    name="cz_emoticon",
    version="0.1.3",
    py_modules=["cz_emoticon"],
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/jdbaigorria/cz_emoticon",
    install_requires=["commitizen"],
    entry_points={"commitizen.plugin": ["cz_emoticon = cz_emoticon:EmoticonCz"]},
    author_email='jdbaigorria@gmail.com',
    author='Javier Baigorria',

)
