from setuptools import setup, find_packages

setup(
    name='mass_analytics',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'numpy==1.25.1',
        'pandas==2.0.3',
        'plotly==5.15.0',
        'streamlit==1.24.1'
    ],
)
