from setuptools import setup
import re

with open('vadivelu/__init__.py') as f:
    # __version: Final[str] = '...'
    version = re.search(r'^__version__\s*:\s*Final\[str]\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)


with open('README.rst') as f:
    readme = f.read()


packages = [
    'vadivelu'
]

setup(
    name='vadivelu',
    author='TheMaster3558',
    url='https://github.com/TheMaster3558/vadivelu',
    version=version,
    packages=packages,
    license='MIT',
    description='A Python wrapper for accessing the Vadivelu API',
    long_description=readme,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    python_requires='>=3.7.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
)
