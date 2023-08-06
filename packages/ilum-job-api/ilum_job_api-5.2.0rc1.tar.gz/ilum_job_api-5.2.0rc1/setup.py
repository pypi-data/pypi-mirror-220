from setuptools import setup, find_packages

setup(
    name="ilum_job_api",
    version="5.2.0-RC1",
    packages=find_packages(),
    package_data={"": ["ilum_job_api/*"]},
    url="https://ilum.cloud",
    license_files=('LICENSE',),
    author="ilum.cloud",
    author_email="info@ilum.cloud",
    description="Ilum job python api",
)
