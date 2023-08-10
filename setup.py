from setuptools import setup, find_packages

setup(
	name='aidapter',
	version='0.6.2',
	description='AI adapter / facade',
	author='Maciej Obarski',
	install_requires=[
		'retry',
        'tqdm',
        'requests',
        'diskcache',
	],
	packages=find_packages()
)
