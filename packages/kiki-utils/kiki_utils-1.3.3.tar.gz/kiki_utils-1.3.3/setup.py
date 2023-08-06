from setuptools import find_packages, setup


setup(
    name='kiki_utils',
    classifiers=[
        'License :: Freely Distributable'
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    version='1.3.3',
    description='Utils decorators and functions.',
    author='kiki-kanri',
    author_email='a470666@gmail.com',
    keywords=['Utils'],
    install_requires=[
        'aiofiles',
        'aioshutil',
        'loguru',
        'orjson',
        'pycryptodomex',
        'pyopenssl',
        'python-magic;platform_system=="Linux"',
        'python-magic-bin;platform_system=="Windows"'
    ],
    python_requires=">=3.8"
)
