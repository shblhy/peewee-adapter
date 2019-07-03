import setuptools

desc_file = "README.md"

with open(desc_file, "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="casbin_peewee_adapter",
    version="0.0.2",
    author="Huang Yan",
    author_email="hyor@foxmail.com",
    description="Peewee Adapter for PyCasbin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shblhy/peewee-adapter",
    keywords=["casbin", "Peewee", "casbin-adapter", "rbac", "access control", "abac", "acl", "permission"],
    packages=setuptools.find_packages(),
    install_requires=['casbin>=0.2', 'peewee>=3.1.0'],
    python_requires=">=3.3",
    license="Apache 2.0",
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    data_files=[desc_file],
)
