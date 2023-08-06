from setuptools import setup

setup(
    name='passstrength142',
    version='1.0.0',
    description='A package for checking the strength of passwords and generating random passwords',
    author='Shrikrishna Umbare',
    author_email='shrikrishna2002umbare@gmail.com',
    url='https://github.com/shri142/password-strength',
    packages=['passstrength142'],
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
