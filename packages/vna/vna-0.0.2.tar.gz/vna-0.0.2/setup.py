from setuptools import setup
import distutils.sysconfig

setup(
    name='vna',
    version='0.0.2',    
    description='Instrument control library for the PicoVNA 106 and PicoVNA 108',
    url='http://picotech.com',
    author='AAI Robotics Ltd',
    author_email='help@aairobotics.com',
    license='MIT',
    packages=["vna"],
    include_package_data=True,
    python_requires=">=3.7",
    data_files = [
        ("",["lib/libftd2xx.so"]),
        ("",["lib/libvna.so"]),
        ("",["lib/_vna_python.so"]),
        ("",["lib/base64.lib"]),
        ("",["lib/ftd2xx.lib"]),
        ("",["lib/vna.lib"]),
        ("",["lib/vna_python.lib"]),
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
)
