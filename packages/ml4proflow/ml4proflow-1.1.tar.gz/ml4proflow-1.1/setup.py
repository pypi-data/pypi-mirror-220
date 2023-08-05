from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

name = "ml4proflow"

cmdclass = {}

try:
    from sphinx.setup_command import BuildDoc
    cmdclass['build_sphinx'] = BuildDoc
except ImportError:
    print('WARNING: Sphinx not available, not building docs')

setup(
    name=name,
    use_git_versioner="short,desc,snapshot",
    author="Christian Klarhorst",
    author_email="cklarhor@techfak.uni-bielefeld.de",
    description="A data flow-oriented framework for industrial ML applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.ub.uni-bielefeld.de/ml4proflow/ml4proflow",
    project_urls={
        "Main framework": "https://gitlab.ub.uni-bielefeld.de/ml4proflow/ml4proflow",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"ml4proflow": ["py.typed"]},
    entry_points={
        'console_scripts': ['ml4proflow-cli=ml4proflow.ml4proflow_cli:main', ],
    },
    cmdclass=cmdclass,
    python_requires=">=3.6",  # todo
    setup_requires=["git-versioner"],
    install_requires=[
        "pandas",
    ],
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
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
#            'version': ('setup.py', version),
#            'release': ('setup.py', version),
            'source_dir': ('setup.py', 'docs/source/'),
            'build_dir': ('setup.py', 'docs/build/')
        }
    },
)
