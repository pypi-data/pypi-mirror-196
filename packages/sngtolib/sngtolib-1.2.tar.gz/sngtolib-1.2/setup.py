from setuptools import find_packages, setup
setup(
    name='sngtolib',
    packages=find_packages(include=['sngtolib']),
    version='1.2',
    description='Lib số nguyên tố và các hàm liên quan đến số nguyên tố trong Python 3',
    author='David Bisky',
    author_email='richardvu12391@gmail.com',
    keywords='số nguyên tố',
    url='https://github.com/VitStudio/lib-pyb14',
    license='Mozilla Public License Version 2.0',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
"""
Step 5: Build your library
Now that all the content is there, we want to build our library. Make sure your present working directory is /path/to/mypythonlibrary (so the root folder of your project). In your command prompt, run:
> python setup.py bdist_wheel

Your wheel file is stored in the “dist” folder that is now created. You can install your library by using:
> pip install /path/to/wheelfile.whl

Note that you could also publish your library to an internal file system on intranet at your workplace, or to the official PyPI repository and install it from there.

Once you have installed your Python library, you can import it using:
import mypythonlib
from mypythonlib import myfunctions
source venv/bin/activate
python setup.py bdist_wheel
pip install /path/to/wheelfile.whl
"""