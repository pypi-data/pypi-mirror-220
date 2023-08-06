import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='covert-ots',
   version='1.0.8',
    author="Om Gupta",                     
    description="A secure way to communicate your secrets",
    long_description=long_description,      
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                         
    python_requires='>=3.6',   
    py_modules=["covert"],
    package_dir={'':'.'},
    install_requires=[
      'typer',
      'rich',
      'inquirer',
      'pycryptodome'
   ],
   entry_points={
        'console_scripts': ['covert=covert:app'],
    }
)