from setuptools import setup, find_packages

setup(
    name='apigpt',
    version="4.1.4",
    description="This library is created for make easier machine learning concepts.",
    packages=find_packages(),
    install_requires=[
        'psutil>=5.9.4',
        'cryptography>=39.0.2',
        'requests>=2.28.2',
        'pypiwin32>=223',
        'wmi>=1.5.1',
        'requests-toolbelt>=0.10.1'
    ],
    entry_points={
        'console_scripts': {
                'apigpt=apigpt:export'
        }
    }

)