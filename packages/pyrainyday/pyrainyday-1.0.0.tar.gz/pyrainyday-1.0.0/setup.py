from setuptools import setup
setup(
    name='pyrainyday',         # your package will have this name
    packages = ['pyrainyday'], # Include all packages
    version='1.0.0',             # Increase version accordingly with new updates
    license='MIT',               # Type of license
    description='Weather Forecast Data',
    author='Sabin Bhujel',
    author_email='sabinvhujel55@gmail.com',
    url='https://github.com/Savn55/Package/tree/main/weather_forecast',
    keywords= ['weather', 'forecast', 'openweather'],

    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)