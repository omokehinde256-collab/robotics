from setuptools import find_packages, setup

package_name = 'four_wheel_robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kenny',
    maintainer_email='kenny@example.com',
    description='Python controller for the four wheel robot',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_controller = four_wheel_robot_controller.robot_controller:main',
        ],
    },
)