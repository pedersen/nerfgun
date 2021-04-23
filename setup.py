from setuptools import setup, find_packages

install_requirements = [
    'dbus-python',
    'pybluez,'
    'pygobject',
    'python-evdev',
    'pyudev',
]

setup(
    name='btemu',
    version='0.1.0',
    description='A Bluetooth emulator to turn Raspberry Pi into keyboard/mouse',
    long_description="""""",
    classifiers=[],
    keywords='bluetooth,raspberry pi,',
    author='Michael J. Pedersen',
    author_email='datacyclist@gmail.com',
    url='https://github.com/pedersen/nerfgun',
    license='MIT and GPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'btemu-serve = btemu.hci:main',
            'btemu-agent = btemu.agent:main',
            'btemu-send-string = btemu.kbd:main',
            'btemu-send-mouse = btemu.mouse:main',
        ],
    },
)
