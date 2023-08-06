from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Information Technology",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]
setup(
    name="ntlmail",
    version="0.0.1",
    description="A SMTP Email Client with NTLP as Authentication",
    long_description=open("README.md").read() + "\n\n" + open("CHANGELOG.txt").read(),
    long_description_content_type="text/markdown",
    url="",
    author="JJTV1029",
    author_email="nicjontrickshots@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords=["NTLM", "SMTP", "auth", "NTLM SMTP auth", "NTLM SMTP", "SMTP NTLM"],
    packages=find_packages(),
    requires=["ntlm_auth", "colorama"]
)