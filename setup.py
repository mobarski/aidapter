from setuptools import setup, find_packages

setup(
	name='aidapter',
	version='0.3.2',
	description='AI adapter / facade',
	author='Maciej Obarski',
	install_requires=[
		'retry',
        'tqdm',
	],
	packages=find_packages()
)
