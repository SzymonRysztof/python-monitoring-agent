import setuptools


setuptools.setup(
    name="Python Monitoring Agent",
    version="0.1",
    author="Szymon Rysztof",
    description="Simple, os independent monitoring agent",
    long_description_content_type="text/markdown",
    url="https://github.com/SzymonRysztof/python-monitoring-agent/",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'influxdb_client>=1.36.1',
        'psutil>=5.9.5',
        'python-dotenv>=1.0.0',
        'PyYAML~=6.0'
    ],
    entry_points={
        'console_scripts': [
            'pma = app.start:start',
        ],
    },
)
