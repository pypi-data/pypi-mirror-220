from setuptools import setup, find_packages

'''
This is used specifiy any dependencies which are needed & should be installed
while installing your custom package.
'''
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='magic_number_guess',
    version='1.0.0',
    description='A magical number guessing game library',
    url='https://github.com/ybshubham/magic-number-guess',
    author='Shubham Yadav',
    author_email='yb.shubham@gmail.com',
    packages=find_packages(),
    install_requires=required_packages,
)
