from setuptools import find_packages, setup

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name='pytest_screenshot_on_failure',
    version='1.0.0',
    description='Saves a screenshot when a test case from a pytest execution fails',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Kleber Lauton',
    url='https://github.com/kleber26/pytest-screenshot-on-failure',
    download_url='https://github.com/kleber26/pytest-screenshot-on-failure/archive/refs/tags/v1.0.0.tar.gz',
    package_dir={'': 'src'},
    py_modules=['pytest_screenshot_on_failure'],
    license='MIT',
    packages=find_packages('src'),
    keywords='pytest plugin test screenshot',
    install_requires=['pytest', 'pluggy', 'selenium', 'setuptools'],
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
        'pytest11': ['pytest_screenshot_on_failure = pytest_screenshot_on_failure',],
    },
)
