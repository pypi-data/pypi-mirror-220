from setuptools import setup, find_packages

setup(
    name="hello_world_iddy",
    version="0.1",
    packages=find_packages(),
    author="Idriss Animashaun",
    author_email="idriss.animashaun@intel.com",
    description="Test",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iddy-ani/hello_world_iddy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # List your project dependencies here
    ],
    python_requires='>=3.10',
)
