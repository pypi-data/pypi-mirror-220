from setuptools import setup, find_packages
import os

with open('README.md') as readme_file:
    README = readme_file.read()


setup_args = dict(
    name='torch-sconce',
    version='0.0.4',
    description='torch-sconce: torch helper',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n',
    license='MIT',
    packages=find_packages(),
    author='Sathyaprakash Narayanan',
    author_email='snaray17@ucsc.edu',
    keywords=['Development Pipeline','Deployment Pipeline','Torch','Pruning', 'Compression', 'Model Pruning'],
    url='https://github.com/satabios/sconce',
    download_url='https://pypi.org/project/torch-sconce/'
)

if __name__ == '__main__':
    lib_folder = os.path.dirname(os.path.realpath(__file__))
    requirement_path = lib_folder + './requirements.txt'
    install_requires = []

    if os.path.isfile(requirement_path):
        with open(requirement_path) as f:
            install_requires = f.read().splitlines()
    print(install_requires)
    setup(**setup_args, install_requires=install_requires)