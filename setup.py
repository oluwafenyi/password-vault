import setuptools

with open('requirements.txt') as f:
    requirements = f.readlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pvault",
    version="1.1.1a",
    author="oluwafenyi",
    author_email="o.enyioma@gmail.com",
    description="A password manager package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oluwafenyi/password-vault",
    license="MIT",
    package_name=["assets"],
    scripts=["assets/pv.py", "assets/pv_password.py",
             "assets/pv_management.py", "assets/pv_generate.py"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=requirements
)
