from setuptools import find_packages, setup

setup(
    name="klaviyo-for-django",
    version="0.0.4",
    author="Santiago Fernandez",
    author_email="",
    packages=find_packages(),
    scripts=[],
    url="http://pypi.python.org/pypi/klaviyo-for-django/",
    license="MIT",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_data={"klaviyo_for_django": []},
    install_requires=["Django >= 4.0.0", "pytest", "klaviyo-api"],
)
