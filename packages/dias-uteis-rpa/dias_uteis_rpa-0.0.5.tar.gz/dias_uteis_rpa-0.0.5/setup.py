from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name="dias_uteis_rpa",
    version="0.0.5",
    license='MIT License',
    author="Edenilson Fernandes dos Santos",
    author_email='santoeen@gmail.com',
    description="Classe com métodos referente dias uteis do Brazil",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='dias uteis brazil brasil feriados nacionais',
    packages=["dias_uteis_brasil","dias_uteis_brasil/img"],
    url = "https://github.com/edenilsonsantos/dias-uteis-brasil",
    project_urls = {
        "repository": "https://github.com/edenilsonsantos/dias-uteis-brasil",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[]
    # install_requires=['datetime','calendar']
)