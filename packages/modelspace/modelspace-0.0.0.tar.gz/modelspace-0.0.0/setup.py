import setuptools

with open("README.md", "r", encoding="utf-8") as fd:
    long_description = fd.read()

setuptools.setup(
    name="modelspace",
    version="0.0.0",
    author="xpai",
    author_email="xpai@users.noreply.github.com",
    description="A curated model zoo for recommendation tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xue-pai/modelspace",
    download_url='https://github.com/xue-pai/modelspace/tags',
    packages=setuptools.find_packages(
        exclude=["tests", "demo"]),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["pandas", "numpy", "h5py", "PyYAML", "scikit-learn", "tqdm"],
    classifiers=(
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    license="Apache-2.0 License",
    keywords=['recommender systems', 'ctr prediction', 
              'tensorflow', 'pytorch'],
)
