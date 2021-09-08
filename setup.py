""" setup.py """
from setuptools import setup, find_packages

setup(
    name='karelcraft',
    url='https://github.com/melvincabatuan/KarelCraft',
    author='Melvin Cabatuan',
    author_email='melvincabatuan@gmail.com',
    packages=['karelcraft','karelcraft.entities','karelcraft.utils'],
    install_requires=['ursina'],
    include_package_data=True,
    python_requires='>=3.8',
    version='0.1',
    license='MIT',
    description='Karel with MineCraft-like environment',
    zip_safe=False,
)
