from setuptools import setup, find_packages
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        super().do_egg_install()
        import btemu.install
        btemu.install.main()


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
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Adafruit-GPIO>=0.9.3',
        'dbus-python',
        'pybluez',
        'pygobject',
        'pyhocon',
        'pyserial',
        'evdev',
        'pyudev',
    ],
    entry_points={
        'console_scripts': [
            'btemu-agent = btemu.agent:main',
            'btemu-serve = btemu.hid:main',
            'btemu-send-string = btemu.kbd:main',
            'btemu-send-mouse = btemu.mouse:main',
            'btemu-controller = btemu.controller:main',
            'btemu-setup = btemu.install:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
)
