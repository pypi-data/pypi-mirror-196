from setuptools import setup, find_packages
from pathlib import Path
CURR_PATH = Path(__file__).parent
file = CURR_PATH / 'requirements.txt'
with open(str(file)) as f:
    requirements = f.read().splitlines()

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ax_generate_banner',
    version='0.0.3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Baxromov',
    author_email='baxromov.shahzodbek@gmail.com',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ]
)
