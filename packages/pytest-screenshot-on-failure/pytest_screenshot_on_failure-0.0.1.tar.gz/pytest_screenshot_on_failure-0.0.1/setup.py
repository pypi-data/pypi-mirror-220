from setuptools import find_packages, setup

setup(
    name='pytest_screenshot_on_failure',
    version='0.0.1',
    description='Saves a screenshot when a test case from a pytest execution fails',
    author='Kleber Lauton',
    url='https://github.com/kleber26/pytest-screenshot-on-failure',
    download_url='https://github.com/kleber26/pytest-screenshot-on-failure/archive/refs/tags/v0.0.1.tar.gz',
    license='MIT',
    packages=find_packages(),
    keywords='pytest plugin test screenshot',
    install_requires=['pytest', 'pluggy', 'pytest', 'selenium', 'setuptools'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'pytest11': ['psf = pytest_screenshot_on_failures',],
    },
)
