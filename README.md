# Python Monitoring Agent

**Python Monitoring Agent (PMA)** is a simple, lightweight, and modular monitoring agent.

PMA serves as a standalone metrics exporter. It requires a database (influxdb) and a frontend tool (such as Grafana) to properly visualize data from influxdb.

## Features

1. **Swap Information**: App retrieves information about the swap memory usage, including total swap space, used swap space, free swap space. On frontend side, those are also calculated into SWAP utilization percentage
2. **RAM Information**: App provides insights into RAM usage, including total RAM, used RAM, free RAM, cached RAM, buffers. On frontend side, those are also calculated into RAM utilization percentage
3. **CPU Information**: App gathers CPU-related details such as user CPU time, system CPU time, idle CPU time, I/O wait time, current CPU frequency, maximum CPU frequency, minimum CPU frequency, CPU load averages (1m, 5m, 15m), CPU utilization percentage, CPU temperature, and the number of processors.
4. **Disk Information**: App provides disks and filesystems information such as block device name, mounted filesystem, space used, space avaliable and space total. On frontend side, those are also calculated into filesystem utilization percentage
5. **Network Information** App gathers network interface related metrics like bytes/packets sent/retrived, errors on interfaces and dropped packets. On frontend side, those are also calculated into network utilization over time (Bytes per second)
6. **Exception Handling and Logging**: App encapsulates each value retrieval in a try-except block. If an exception occurs, the value is assigned as `None`, and the exception is passed to a `logging` instance, allowing for better error tracking and handling.

## Usage

Currently, there are two ways to use this software:

1. As a Docker container (recommended for Linux)
2. As a Python package (requires Python 3.6 or higher)

> **Note:**
>
> Docker usage is recommended on Linux but shouldn't be used on MacOS or Windows! Docker desktop for MacOS and Windows is essentially a Linux virtual machine, so metrics collected from Docker desktop with PMA would be meaningless. For these two systems, using the Python native version is recommended.

### Docker Usage

**Agent Only:**

1. Copy the `.env.dist` file to `.env`.
2. Populate the `.env` file with the appropriate values (only those starting with "AGENT" need to be modified).
3. Set the docker-compose profile: `export COMPOSE_PROFILE=agent-only`.
4. Build the agent image: `docker compose build`.
5. Start the agent image: `docker compose up -d`.

**Full Stack:**

1. Copy the `.env.dist` file to `.env`.
2. Populate the `.env` file with the proper values.
3. Set the docker-compose profile: `export COMPOSE_PROFILE=full`.
4. Start the InfluxDB container: `docker compose up -d influxdb`.
5. Access the InfluxDB WebUI (default: http://127.0.0.1:8086).
6. Create an API token from the "Load Data" > "API Tokens" menu.
7. Copy and paste the API token into the `.env` file.
8. Build the agent container: `docker compose build`.
9. Start the other containers: `docker compose up -d`.
10. Open the Grafana WebUI (default: http://127.0.0.1:3000).
11. From the "Administration" > "Data Sources" menu, create a new InfluxDB datasource:
    1. Set the query language to Flux.
    2. Add the InfluxDB URL. Both Grafana and InfluxDB are inside the docker-compose default network, so use `http://influxdb:8086` as the URL (modify accordingly if you changed the service name in docker-compose.yml).
    3. Disable basic authentication.
    4. Fill in the default bucket and default organization. This is important if you want to use the provided dashboard without modification.
    5. Fill in the API token with your token.
12. From the "Dashboards" menu, select "New" > "Import" and drag and drop the `docker/grafana/Python-monitoring-agent.json` file.
13. Open your dashboard and select your host.

### Python Package Usage

**Agent Only:**

1. Install the Python package: `pip install ./docker/agent`.
2. Start the app with `pma` from the terminal.
3. An empty configuration file will be created in `$XDG_CONFIG_HOME` directory. If `$XDG_CONFIG_HOME` is not set or you are on Windows or macOS, `$HOME/.config` will be used as the base directory.
4. Edit the configuration file at `$XDG_CONFIG_HOME/python-monitoring-agent/config.yaml` or `$HOME/.config/python-monitoring-agent/config.yaml` and replace the default values with your own.
5. Start the app with `pma`. If you want to start the app in the background without binding it to your terminal, use `nohup pma &` (works on both macOS and Linux).


## Configuration explained

| Config Option                      | Explanation                                       |
|------------------------------------|---------------------------------------------------|
| AGENT_INFLUX_URL                   | The URL of the InfluxDB instance to connect to.   |
| AGENT_INFLUX_BUCKET                | The name of the InfluxDB bucket to use.           |
| AGENT_INFLUX_ORG                   | The name of the InfluxDB organization to use.     |
| AGENT_INFLUX_TOKEN                 | The API token for accessing InfluxDB.             |
| AGENT_HOSTNAME                     | The hostname of the agent.                        |
| AGENT_POOLING_RATE                 | The rate at which the agent performs pooling.     |
| AGENT_VERBOSITY                    | The level of verbosity for logging.               |
| AGENT_DOCKER                       | Docker specific option, needs to exist as environment if docker is used (Can be set to anything, like "True") |
| DOCKER_INFLUXDB_INIT_USERNAME      | Initial WebUI username for InfluxDB.              |
| DOCKER_INFLUXDB_INIT_PASSWORD      | Initial WebUI password for InfluxDB.              |
| DOCKER_INFLUXDB_INIT_ORG           | Initial organization name for InfluxDB.           |
| DOCKER_INFLUXDB_INIT_BUCKET        | Initial bucket name for InfluxDB.                 |
| DOCKER_INFLUXDB_INIT_MODE          | Initial Docker setup mode for InfluxDB.           |



## TODO
1. Add sensors metrics
2. Add more metrics overall
3. Create CI/CD Pipeline that would be building and publishing Docker images and Python package on releases
4. Think of a way of allowing new modules to be added easily
5. Add cron/systemd timers mode
6. Add systemd unit file


## Contribution

**Contributions Welcome!**

We welcome contributions from anyone interested in improving our project. If you have ideas, bug fixes, or new features to propose, we encourage you to create pull requests. Together, we can make this project even better!

Feel free to explore the codebase, find areas where you can contribute, and submit your pull requests. We appreciate your support and look forward to collaborating with you!

