from setuptools import setup, find_packages

setup(
    name='rapiz',
    version='0.0.1',
    description="Create your website in an instant.",
    long_description="In Development.",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # list your package dependencies here
    ],
    entry_points={
        'console_scripts': [
            'rapiz=rapiz.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
