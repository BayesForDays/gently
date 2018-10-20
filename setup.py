from setuptools import setup, find_packages

setup(
    name='gently',
    version='0.0.1',
    author=['Cassandra Jacobs', 'Andrés Buxó-Lugo'],
    author_email='jacobs.cassandra.l@gmail.com',
    license='MIT',
    url='https://github.com/BayesForDays/gently',
    description='Praat tools and Python functions that help you do more without Praat',
    packages=find_packages(),
    long_description='`gentle` and `praatio` are great tools. Let\'s make them even better!',
    keywords=['praat', 'io', 'speech-processing', 'forced-alignment'],
    classifiers=[
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'praatio',
        'pandas',
        'wave',
        'gentle'
    ],
    dependency_links=[
        "git+ssh://git@github.com/lowerquality/gentle.git"
    ]
)
