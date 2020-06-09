import setuptools

with open("README", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='tcc',
    version='0.0.1',
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    url='https://github.com/lsargus/tcc',
    license='',
    python_requires=">=3.7",
    author='lsarg',
    author_email='lsargus@hotmail.com',
    description=''
)
