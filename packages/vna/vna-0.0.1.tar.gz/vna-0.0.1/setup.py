from setuptools import setup, find_packages
import distutils.sysconfig

setup(
    name='vna',
    version='0.0.1',    
    description='Instrument control library for the PicoVNA 106 and PicoVNA 108',
    url='http://picotech.com',
    author='AAI Robotics Ltd',
    author_email='help@aairobotics.com',
    license='MIT',
    packages = find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    data_files = [
        (distutils.sysconfig.get_python_lib(),["lib/libftd2xx.so"]),
        (distutils.sysconfig.get_python_lib(),["lib/libvna.so"]),
        (distutils.sysconfig.get_python_lib(),["lib/_vna_python.so"]),
        (distutils.sysconfig.get_python_lib(),["lib/base64.lib"]),
        (distutils.sysconfig.get_python_lib(),["lib/ftd2xx.lib"]),
        (distutils.sysconfig.get_python_lib(),["lib/vna.lib"]),
        (distutils.sysconfig.get_python_lib(),["lib/vna_python.lib"]),
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
