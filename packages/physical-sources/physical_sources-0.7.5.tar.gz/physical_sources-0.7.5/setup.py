from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

    with open('HISTORY.md') as history_file:
        HISTORY = history_file.read()

setup(
    name='physical_sources',
    version='0.7.5',
    packages=find_packages('src', exclude=['test*.py']),
    license='',
    author='Dr. Frank Mobley',
    author_email='frank.mobley.1@afrl.af.mil',
    description="A collection of classes that can be used to build acoustic sources from the NOISEFILE format. It "
                "also contains classes to read the binary representations born from the author's dissertation",
    package_dir={'': 'src'},
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/physicalpropagation/physcial_sources',
    install_requires=['numpy', 'scipy', 'PythonCoordinates>=0.5.0', 'Pytimbre>0.6.1',
                      'physical_propagation>=0.5.1', 'matplotlib>=3.3.1']
)
