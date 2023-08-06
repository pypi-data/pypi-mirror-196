import setuptools

setuptools.setup(
    name="spreg-satosa-sync",
    python_requires=">=3.6.2",
    url="https://gitlab.ics.muni.cz/perun-proxy-aai/python/spreg-satosa-sync.git",
    description="Script to sync SATOSA clients from Perun RPC to mongoDB",
    packages=setuptools.find_packages(),
    install_requires=[
        "setuptools",
        "pycryptodomex~=3.11",
        "pymongo>=3.12.1,<5",
        "requests~=2.26",
        "PyYAML~=6.0",
        "perun.connector~=3.4",
    ],
)
