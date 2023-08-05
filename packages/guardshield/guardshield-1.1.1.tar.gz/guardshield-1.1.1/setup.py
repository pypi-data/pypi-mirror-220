import setuptools, os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name="guardshield",
    version="1.1.1",
    author="Oxyn",
    author_email="oxyn.dev@gmail.com",
    description="Python security lib",
    keywords="python anti debugger security exe",
    packages=setuptools.find_packages(),
    include_package_data=True,
    url='https://github.com/OxynDev/ExcerSec',
    zip_safe=False,
    license='MIT',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    data_files=[('guardshield/core', ['guardshield/core/cheatengine.py'])],
)
