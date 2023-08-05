from setuptools import setup, find_packages
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(current_dir, 'README.md')

setup(
    name='imgbbb',
    version='1.0.4',
    description='Imgbb uploader without API key',
    author='OneFinalHug',
    author_email='voidlillis@gmail.com',
    url='https://github.com/OneFinalHug/imgbbb/',
    long_description = open(readme_path).read(),
    long_description_content_type='text/markdown',
    keywords=['imgbb_uploader', 'telegram','host', 'uploader', 'imgbb', 'image'],
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorclip',
		'fake-useragent',
		'requests-toolbelt'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    entry_points={
        'console_scripts': [
            'imgbbb = imgbbb:main'
        ]
    }
)
