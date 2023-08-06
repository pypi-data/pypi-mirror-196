from setuptools import setup, find_packages
from pip._internal.req import parse_requirements
requirements = parse_requirements('core/requirements.txt', session='hack')

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
requirements_list = [i.requirement for i in requirements]
setup(
    name='ax_generate_banner',
    version='0.0.7',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Baxromov',
    author_email='baxromov.shahzodbek@gmail.com',
    packages=find_packages(),
    install_requires=requirements_list,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ]
)
