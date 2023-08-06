from setuptools import setup, find_packages

setup(
    name='warmindo',
    version='0.6', 
    packages=find_packages(),
    install_requires=[
        'SQLAlchemy',
        'Flask',
        'mysql-connector-python',
        'scikit-learn',
        'python-telegram-bot',
    ],
    entry_points={
        'console_scripts': [
            'warmindo=gas:main'
        ]
    },
    author='adham cahyo',
    author_email='arnolisarnol@gmail.com',
    description='Framework Warmindo berbasis Python',
    url='https://github.com/adhamcahyo/warmindo',  
    project_urls={
        'Source Code': 'https://github.com/adhamcahyo/warmindo',
        'Documentation': 'https://github.com/adhamcahyo/warmindo/docs',  
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        # SUPPORT PYTHON 3.11 su311
        'Programming Language :: Python :: 3.11', 
    ],
    keywords='framework web warmindo python',
)
