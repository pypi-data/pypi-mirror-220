from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='rsa_encryptor',
    version='0.1',
    author='Bahir Hakimi',
    author_email='bahirhakimy2020@gmail.com',
    description='=A minimal implemetation of asymetric encryption operations using RSA',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bahirhakimy/rsa_encryptor',
    download_url = 'https://github.com/BahirHakimy/rsa_encryptor/archive/refs/tags/v1.0.tar.gz',
    packages=['rsa_encryptor'],
    keywords = ['RSA', 'Encryption', 'DigitalSignature'],
    install_requires=['rsa'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)