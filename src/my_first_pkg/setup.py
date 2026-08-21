from setuptools import find_packages, setup

package_name = 'my_first_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/multi_node_launch.py']),
    ],
    install_requires=['setuptools', 'my_first_interfaces'],
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
           'publisher_node = my_first_pkg.publisher_node:main',
           'subscriber_node = my_first_pkg.subscriber_node:main',
           'add_two_ints_server = my_first_pkg.add_two_ints_server:main',
           'add_two_ints_client = my_first_pkg.add_two_ints_client:main',
               'fibonacci_action_server = my_first_pkg.fibonacci_action_server:main',
               'parameter_example = my_first_pkg.parameter_example:main',
               'parameter_callback_example = my_first_pkg.parameter_callback_example:main',
        ],
    },
)
