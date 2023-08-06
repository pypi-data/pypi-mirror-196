from setuptools import setup

def readme():
    with open("README.rst", encoding = "UTF-8") as f:
        return f.read()

setup(
    name = "nopapy",
    version = "1.0.1",
    description = "「NopaPy」is an easy-to-use open-source library for non-parametric statistic.",
    packages = ["nopapy.estimate", "nopapy.kernel", "nopapy.regression", "nopapy.utils"],
    author = "Zhu Yaolin",
    author_email = "540048506@qq.com",
    long_description = readme(),
    include_package_data = True,
    url = "https://github.com/QVQZZZ/NopaPy",
    license = "MIT"
)
