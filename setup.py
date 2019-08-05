import setuptools

with open('requirements.txt') as f:
    requirements = f.readlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pvault",
    version="1.1.2a",
    author="oluwafenyi",
    author_email="o.enyioma@gmail.com",
    description="A password manager package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oluwafenyi/password-vault",
    download_url="https://pypi.org/project/pvault/",
    license="MIT",
    keywords="password crypto management",
    packages=setuptools.find_packages(exclude=["contrib", "docs", "tests"]),
    python_requires='>=3.5',
    package_name=["pvault"],
    entry_points={
        'console_scripts': [
            'pv = pvault.pv:main'
        ]
    },
    scripts=[
        'pvault/pv.py'
    ],
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=requirements
)
