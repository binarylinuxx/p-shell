from setuptools import setup

setup(
    name="pshell",
    version="0.1.0",
    description="A customizable Python shell with Git integration and rich features",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nir Rudov",
    author_email="aar58384@gmail.com",
    url="https://github.com/binarylinuxx/p-shell",
    license="MIT",
    python_requires=">=3.6",
    install_requires=[
        "colorama>=0.4.4",
        "prompt_toolkit>=3.0.0",
    ],
    scripts=["psh.py"],
    entry_points={
        "console_scripts": [
            "psh=psh:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Shells",
        "Topic :: System :: System Shells",
        "Topic :: Terminals",
    ],
    keywords="shell terminal prompt git",
)
