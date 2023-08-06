from setuptools import setup
from setuptools import find_packages
setup(
    name='xgh_create_project_directories',
    author='xgh',
    description='生成工程目录结构',
    version='0.0.0',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'x-create-porject-directories=create_project_directories.main:main'
        ]
    }
)
