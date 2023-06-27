import setuptools

with open("README.md", "r") as description:
    long_description_text = description.read()

setuptools.setup(
    name="python_monitoring_agent",
    version="0.2.2-rc2",
    author="Szymon Rysztof",
    description="Simple, os independent monitoring agent",
    long_description=long_description_text,
    long_description_content_type="text/markdown",
    url="https://github.com/SzymonRysztof/python-monitoring-agent/",
    platforms=['Linux', 'Windows', 'Unix'],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'influxdb_client>=1.36.1',
        'psutil>=5.9.5',
        'PyYAML~=6.0'
    ],
    entry_points={
        'console_scripts': [
            'pma = python_monitoring_agent.start:start',
        ],
    },
)
