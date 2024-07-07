from setuptools import find_packages, setup

setup(
    name="hbl-card-payment",
    description="A simple implementation of HBL card payment integration in Python.",
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    version="0.0.1",
    author="suzanpradhan",
    author_email="sujanpradhan478@gmail.com",
    packages=find_packages(),
    url="https://github.com/suzanpradhan/hbl_card_payment",
    install_requires=[
        "pyjwt",
        "requests",
        "python-jose",
    ],
)
