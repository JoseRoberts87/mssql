from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mssql',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    author='Jose Roberts',  # Type in your name
    author_email='Jose.Roberts@intracitygeeks.org',  # Type in your E-Mail
    description="python sqlalchemy MsSQL utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoseRoberts87/mssql",
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        'sqlalchemy',
        'pyodbc'
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)