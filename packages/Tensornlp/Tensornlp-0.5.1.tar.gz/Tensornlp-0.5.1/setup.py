from setuptools import setup, find_packages

setup(
    name='Tensornlp',
    version='0.5.1',
    description='A tensornlp library for NLP tasks',
    packages=find_packages(include=['tensornlp','tensornlp.client', 'tensornlp.grpcDir']),
    author='Hamza Khan',
    author_email='hamzamania@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'grpcio',
        'grpcio-tools',
        'protobuf',
        'pymongo',
        # Add any other dependencies here
    ],
    python_requires='>=3.6',
)