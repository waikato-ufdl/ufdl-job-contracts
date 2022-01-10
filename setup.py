from setuptools import setup, find_namespace_packages

def _read(f) -> bytes:
    """
    Reads in the content of the file.
    :param f: the file to read
    :type f: str
    :return: the content
    :rtype: str
    """
    return open(f, 'rb').read()


setup(
    name="ufdl.jobcontracts",
    description="The base contracts fulfilled by job-templates in the UFDL system.",
    long_description=(
        _read('DESCRIPTION.rst') + b'\n' +
        _read('CHANGES.rst')).decode('utf-8'),
    url="https://github.com/waikato-ufdl/ufdl-job-types",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
    ],
    license='Apache 2.0 License',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    namespace_packages=[
        "ufdl",
    ],
    version="0.0.1",
    author='Corey Sterling',
    author_email='csterlin@waikato.ac.nz',
    install_requires=[
    ],
    entry_points={
    }
)
