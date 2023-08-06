from setuptools import setup

with open('README.md', 'r') as arq:
    readme = arq.read()

setup(
    name='criptografiaferik',
    version='0.5',
    packages=['criptografiaferik'],
    install_requires=['numpy'],
    author='Erik Soares e Fernando Santos',
    long_description= readme,
    long_description_content_type = "text/markdown",
    description='Uma biblioteca para criptografia de mensagens',
    url='https://github.com/eriksoaress/Criptografia',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
