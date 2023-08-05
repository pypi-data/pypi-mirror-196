from setuptools import setup

setup(
    name = 'sandtt',
    version = '0.1.0',
    packages = ['sandtt'],
    include_package_data=True,
    package_data={'sandtt': ['newEmbeddings.json']},
    entry_points = {
        'console_scripts': [
            'sandtt = sandtt.__main__:main'
        ]
    })
