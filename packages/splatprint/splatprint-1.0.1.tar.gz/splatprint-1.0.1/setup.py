from setuptools import setup

setup(
    name='splatprint',
    version='1.0.1',    
    description='A macro generator for NXBT to print Splatoon 3 posts via Bluetooth.',
    url='https://github.com/wryvrrrn/splatprint',
    author='Wryvrrrn',
    license='MIT',
    packages=['splatprint'],
    install_requires=['numpy',
                      'Pillow'
    ],
    entry_points={
        'console_scripts': [
            'splatprint = splatprint.splatprint:main',
        ]
    }
)