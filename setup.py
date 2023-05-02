from setuptools import find_packages, setup


setup(
    name='pylinhsu',
    version='0.1.0',
    description="Lin Hsu's utility library",
    author='Lin Hsu',
    author_email='linhsu0723@qq.com',
    url='https://github.com/chaosink/pylinhsu',
    license='MIT',
    install_requires=[
        'imageio',
        'imageio',
        'joblib',
        'numpy',
        'requests',
        'scikit-image',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    packages=find_packages(),
)
