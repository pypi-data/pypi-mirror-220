from setuptools import setup

setup(
    name='srv-rst-0ae-amp-test',
    version='1.0.0',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ángel Moreno',
    author_email='a.morenoper@gmail.com',
    url='https://www.google.es',
    license_files=[
        'LICENSE'
    ],
    packages=[
        'app'       
    ],
    install_requires=[
        paquete.strip() for paquete in open('requirements.txt').readlines()
    ],
    scripts=[
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities'
    ]
)