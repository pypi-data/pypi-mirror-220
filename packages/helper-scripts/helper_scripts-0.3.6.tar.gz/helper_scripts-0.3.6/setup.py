from setuptools import setup, find_packages
setup(
    name = 'helper_scripts',
    packages = ['database_handler','send_mail'],
    version='0.3.6',
    author='Samuel Kizza',
    author_email= 'SK8@gmail.com',
    maintainer='Winston David Ssentongo',
    maintainer_email='winstondavid96@gmail.com',
    description='Database Helper Package',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
    "psycopg2",
    "pandas",
    ]
    # requires=[
    #     'psycopg2',
    #     'pandas'
    # ],
)