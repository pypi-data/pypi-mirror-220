from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ml4proflow-mods-io",
    use_git_versioner="short,desc,snapshot",
    author="Christian Klarhorst",
    author_email="cklarhor@techfak.uni-bielefeld.de",
    description="IO Modules for the Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.ub.uni-bielefeld.de/ml4proflow/ml4proflow-mods-io",
    project_urls={
        "Main framework": "https://gitlab.ub.uni-bielefeld.de/ml4proflow/ml4proflow",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    #package_dir={"": "src"},
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    namespace_packages=['ml4proflow_mods'],
    setup_requires=["git-versioner"],
    install_requires=["ml4proflow", "pyarrow", "tables"],
    extras_require={
        "tests": ["pytest", 
          "pandas-stubs",
          "pytest-html",
          "pytest-cov",
          "flake8",
          "mypy",
          "jinja2==3.0.3"],
        "docs": ["sphinx", "sphinx-rtd-theme", "recommonmark"],
    },
    python_requires=">=3.6", # todo
)
