from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='ATTACK_THE_ENEMY_RPG',
    version='1',
    packages=['ATTACK_THE_ENEMY_RPG'],
    url='https://github.com/GlobalCreativeApkDev/INDONESIAN_PROGRAMMERS/tree/main/ATTACK_THE_ENEMY_RPG',
    license='MIT',
    author='GlobalCreativeApkDev',
    author_email='globalcreativeapkdev2022@gmail.com',
    description='This package contains implementation of the offline RPG '
                '"ATTACK_THE_ENEMY_RPG" on command line interface.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    entry_points={
        "console_scripts": [
            "ATTACK_THE_ENEMY_RPG=ATTACK_THE_ENEMY_RPG.attack_the_enemy_rpg:main",
        ]
    }
)