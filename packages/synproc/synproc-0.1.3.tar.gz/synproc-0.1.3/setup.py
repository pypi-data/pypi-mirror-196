from setuptools import setup, find_packages

classifiers=['Development Status :: 5 - Production/Stable',
             'Intended Audience :: Education',
             'License :: OSI Approved :: MIT License',
             'Programming Language :: Python :: 3'
             ]
setup(
    name='synproc',
    version='0.1.3',
    description='A SYN file converting tool',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='Abdelhadi Harrouz',
    author_email='abdelhadiharrouz@outlook.com',
    license='MIT',
    classifiers=classifiers,
    packages=find_packages(),
    keywords='Meteorology',
    install_requires=[
        'numpy',
        'pandas',
    ],
)