from setuptools import setup, find_packages

setup(
    name='trgm',      # Replace with your library name
    version='0.0.1',        # Replace with your library version
    description='A library to help you create text adventure games with Python',  # Replace with a short description
    author='Nithil Gadde',
    author_email='nithilgadde2010@gmail.com',
    url='https://github.com/your_username/my_library',  # Replace with the URL to your library's repository
    packages=find_packages(),
    install_requires=['pickle'],   # Add any dependencies required by your library
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
