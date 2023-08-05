from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='thcli',
    version='1.2.0',
    packages=find_packages(),
    install_requires=requirements,
    author='Taehoon Kang',
    entry_points={
        'console_scripts': ['thcli=main:main'],
    },
    author_email='kangthink@gmail.com',
    description='Greeting for fun.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)