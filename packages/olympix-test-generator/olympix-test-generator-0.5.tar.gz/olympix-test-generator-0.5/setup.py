from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="olympix-test-generator",
    version="0.5",
    packages=find_packages(),
    author="Evan Fenster",
    author_email="evan@olympix.ai",
    description="Used to auto-generate unit tests for smart contracts using the Forge framework.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/olympix/olympix-test-generator",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=required,
    entry_points={
        'console_scripts': [
            'olympix=olympix_test_generator.client:main',
        ],
    },
)
