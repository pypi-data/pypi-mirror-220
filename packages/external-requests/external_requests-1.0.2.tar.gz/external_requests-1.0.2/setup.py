from setuptools import setup, find_packages


def read(file_name):
    with open(file_name) as file:
        content = file.read()
    return content


setup(
    name='external_requests',
    version='1.0.2',
    author='Venfi Oranai',
    author_email='venfioranai@gmail.com',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://gitlab.com/VenfiOranai/external-requests',
    install_requires=[
        'marshmallow',
        'requests'
    ]
)
