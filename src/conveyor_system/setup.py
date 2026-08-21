from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'conveyor_system'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mohit',
    maintainer_email='mohitkt1993@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'sensor_node = conveyor_system.sensor_node:main',
            'control_node = conveyor_system.control_node:main',
            'safety_supervisor_node = conveyor_system.safety_supervisor_node:main',
            'logger_node = conveyor_system.logger_node:main',
            'operator_service_node = conveyor_system.operator_service_node:main',
        ],
    },
)
