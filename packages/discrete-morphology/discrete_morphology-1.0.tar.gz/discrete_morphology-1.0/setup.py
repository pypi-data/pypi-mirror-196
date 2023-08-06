from setuptools import setup

setup(
    name='discrete_morphology',
    version='1.0',
    packages=['discrete_morphology'],
    url='https://github.com/mmunar97/discrete_morphology',
    license='mit',
    author='marcmunar',
    author_email='marc.munar@uib.es',
    description='Set of algorithms in the framework of discrete mathematical morphology for image processing.',
    include_package_data=True,
    install_requires=[
        "discrete_fuzzy_operators",
        "opencv-python",
        "numpy"
    ]
)
