from setuptools import setup, find_packages

setup(
    name='simple_param_parser',
    version='0.1',
    packages=find_packages(),
    description='A simple package to parse bunch of params either via command line or from environment variables',
    author='Lucky Singh',
    author_email='thecoderider42@gmail.com',
    url='https://github.com/the-code-rider/simple_param_parser',
    license='MIT',
    keywords=['command line', 'arguments', 'cli', 'environment variables'],
    install_requires=[
        'pydantic>=2.8.2',
        'python-dotenv==1.0.1'
    ]
)
