from setuptools import setup, find_packages

setup(
    name='Tensornlp',
    version='0.5',
    description='A tensornlp library for NLP tasks',
    packages=find_packages(['client', 'grpcDir']),
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
    entry_points={
        'console_scripts': [
            'my_service=tensornlp.main:serve',
        ],
    },
    python_requires='>=3.6',
)