import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="edu_code_mutate",                    
    version="0.0.1",                    
    author="Pranjal Naringrekar",                    
    description="Capstone app",
    long_description=long_description,  
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["edu_code_mutate"],         # Name of the python package
    package_dir={'':'capstone\src'},        # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)
