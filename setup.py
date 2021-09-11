""" setup.py """
from setuptools import setup, find_packages

setup(
    name='karelcraft',
    url='https://github.com/melvincabatuan/KarelCraft',
    author='Melvin Cabatuan',
    author_email='melvincabatuan@gmail.com',
    packages=['karelcraft','karelcraft.entities','karelcraft.utils'],
    install_requires=['panda3d','ursina==3.5.0'],
    include_package_data=True,
    version='0.0.1',
    license='MIT',
    description='Karel with MineCraft-like environment',
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
