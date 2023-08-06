from setuptools import setup, find_packages

setup(
    name='losscape',
    version='1.2',
    url='https://github.com/Procuste34/losscape',
    author='Alexandre TL',
    author_email='alexandretl3434@gmail.com',
    description='Visualize easily the loss landscape of your neural networks',
    packages=find_packages(),  
    install_requires=['torch>=1.8.1', 'numpy', 'scipy', 'matplotlib'],
)
