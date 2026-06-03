from setuptools import setup

package_name = 'multi_comm'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='you',
    maintainer_email='you@example.com',
    description='Minimal multi-PC ROS2 talker/listener package',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'comm = multi_comm.comm:main',
        ],
    },
)
