![Coverage](https://gitlab.ics.muni.cz/cryton/cryton-cli/badges/master/coverage.svg)

[//]: # (TODO: add badges for python versions, black, pylint, flake8, unit tests, integration tests)

# Cryton CLI
Cryton CLI is a command line interface used to interact with [Cryton Core](https://gitlab.ics.muni.cz/cryton/cryton-core) (its API).

Cryton toolset is tested and targeted primarily on **Debian** and **Kali Linux**. Please keep in mind that **only 
the latest version is supported** and issues regarding different OS or distributions may **not** be resolved.

For more information see the [documentation](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/components/cli/).

## Quick-start
Please keep in mind that [Cryton Core](https://gitlab.ics.muni.cz/cryton/cryton-core) must be running and its REST API must be reachable.

Make sure [Docker](https://docs.docker.com/engine/install/) is installed.
Optionally, check out these Docker [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/).

The following script starts an interactive shell using Docker. 
```shell
docker run -it --network host registry.gitlab.ics.muni.cz:443/cryton/cryton-cli
```

Use the following to invoke the app:
```shell
cryton-cli
```

For more information see the [documentation](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/components/cli/).

## Contributing
Contributions are welcome. Please **contribute to the [project mirror](https://gitlab.com/cryton-toolset/cryton-cli)** on gitlab.com.
For more information see the [contribution page](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/contribution-guide/).
