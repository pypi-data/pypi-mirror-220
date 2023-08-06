import setuptools
setuptools.setup(
    name="sita_package_ml",
    version="0.1.1",                        
    author="Djeinaba",
    author_email="djeinaba147@gmail.com",
    description="buiding a python package",
    long_description="python package for ML models",
    long_description_content_type="hello this is just a test",
    install_requires=[                     
        "numpy",
        "sklearn>",
        "plotly",
        
                                                  
    ],                                             
    url="https://gitlab.com/Djeinaba_Doro/test_project",  
    packages=setuptools.find_packages(),
    classifiers=[                               
        "Programming Language :: Python :: 3.7",    
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",   
    ],
)
