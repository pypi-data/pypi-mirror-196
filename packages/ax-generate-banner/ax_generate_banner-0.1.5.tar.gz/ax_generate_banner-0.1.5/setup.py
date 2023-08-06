from setuptools import setup, find_packages
with open('ax_generate_banner/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ax_generate_banner',
    version='0.1.5',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Baxromov',
    author_email='baxromov.shahzodbek@gmail.com',
    packages=find_packages(),
    package_data={
        'ax_generate_banner': ['fonts/*', 'README.md'],
    },
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ]
)
