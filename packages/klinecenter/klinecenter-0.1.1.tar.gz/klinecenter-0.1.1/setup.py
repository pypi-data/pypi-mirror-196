import setuptools

setuptools.setup(
    name="klinecenter",
    version="0.1.1",
    author="klinecenter",
    author_email="kline8@foxmail.com",
    description="",
    long_description="",
    # long_description_content_type="text",
    url="https://kline8.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "pandas>=1.0.0",
    ],
)
# Set your username to __token__
# Set your password to the token value, including the pypi- prefix
# For example, if you are using Twine to upload your projects to PyPI, set up your $HOME/.pypirc file like this:
# [pypi]
#   username = __token__
#   password = pypi-AgEIcHlwaS5vcmcCJDM1ZTQ2YjE4LTQ4Y2EtNDZmMi1iZDMyLTZhOTFlYzg0NWU4ZAACKlszLCI4OWNlODI0Yi1iNGVlLTQ1YTYtOWM2Ni1lYzMwMmIzNzRmZTUiXQAABiCmmkolxPv7hjJfVFgLYXOsEHz1ZXVfYKOLAEpLniD5sA
