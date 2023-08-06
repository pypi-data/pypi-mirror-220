from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()
    
with open("understar/.version", "r") as stream:
    ver = stream.read()

# long_description = "An universal wrapper (and useful tool) to make event / commands in python"

name='understar'
version=f"{ver}"
url='https://github.com/GalTechDev/UnderStar-OS'
download_url='https://github.com/GalTechDev/UnderStar-OS/tarball/master'
license='MIT'
author='GalTech'
author_email='poussigalitv@gmail.com'
description='A discord bot framewrok'
long_description=long_description
long_description_content_type='text/markdown'
keywords=[
        "discord",
        "bot",
        "discord.py",
        "understar",
        "os",
        "framework"
]
install_requires=[
        "easy-events>=2.9.0",
        "discord.py>=2.1",
        "requests_html",
]
setup_requires=[
        'wheel'
]
classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
]
packages=find_packages()
package_data={
    'understar': ['.version'],
}

if __name__ == "__main__":
    setup(
        name=name,
        version=version,
        url=url,
        download_url=download_url,
        license=license,
        author=author,
        author_email=author_email,
        description=description,
        long_description=long_description,
        long_description_content_type=long_description_content_type,
        keywords=keywords,
        install_requires=install_requires,
        setup_requires=setup_requires,
        classifiers=classifiers,
        packages=find_packages(include=["*", ".version"]),
        package_data=package_data
        # packages=["sdist", "bdist_wheel"]
        # python_requires='>=3.10',
    )
