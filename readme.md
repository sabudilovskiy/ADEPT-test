# Project Name

This project is a test assignment implemented using the `userver` framework as the base and a custom-made library `uopenapi` for declaratively defining handlers. The project provides a set of API endpoints for managing and grouping objects by various criteria.

- [Endpoints](#endpoints)
- [API](#api)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [CI](#ci)
- [Helper commands](#helper-commands)
- [How to run](#how-to-run)
- [How to run via docker](#how-to-run-via-docker)
- [How to instal dependencies](#how-to-install-dependencies)
- [How to build](#how-to-build)
- [How to build docker and release](#how-to-build-docker-and-release)

## Endpoints

The following endpoints are implemented:

- **POST /object**: Adds a new object.
- **GET /group/distance**: Groups objects by distance.
- **GET /group/time**: Groups objects by time.
- **GET /group/type**: Groups objects by type.
- **GET /group/name**: Groups objects by name.

## API

API is generated automatically based on the handlers used. 
For more information, see [userver-openapi-extension](https://github.com/sabudilovskiy/userver-openapi-extension).
When running the tests, the api file will also be updated. To do this, build the debug version of the application and run the tests using.
SWAGGER: [link](https://app.swaggerhub.com/apis/SABUDILOVSKIY_1/test32312/1.0.0)

## Project Structure

The overall project structure is as follows:

- /configs        - Static configurations for the service
- /postgresql     - Database migration scripts
- /scripts        - Auxiliary scripts
- /service        - Main service entry point
- /src/api        - API types
- /src/codegen    - Auto-generated declarations of PostgreSQL queries
- /src/models     - Models for managing entities
- /src/sql        - SQL queries
- /src/views      - Endpoints
- /tests          - End-to-end tests for various endpoints (26 tests in total)

## Testing

End-to-end tests are provided to cover all implemented endpoints, with a total of 26 tests ensuring the functionality of the service.
The tests are written in pytest using part of the userver - testsuite framework. 
The tests have been added to ctest, so they can be run from the build folder using ctest.

Structure:
- conftest.py : necessary fixtures for correct operation of testsuite
- objects_db.py : Fixture for simple work with the database (adding objects, types and getting existing ones).
- test_create_object.py : /objects POST
- test_group_distance.py : /group/distance GET
- test_group_name.py : /group/name GET
- test_group_time.py : /group/time GET
- test_group_type.py : /group/type GET

There is a helper command to run tests.
```sh
make tests
```

## CI

The project has github ci configured, which builds the project on ubuntu, and uses several versions and families of compilers. In addition, there is a separate pipeline with formatting.

## Helper commands 

The makefile is used as a script file. The full list of commands.

| Command                | Description                                                                                                        |
|------------------------|--------------------------------------------------------------------------------------------------------------------|
| `check-git-status`     | Checks that all files are committed in Git. If there are uncommitted files, it lists them and rejects execution.   |
| `add-eol`              | Adds an End-Of-Line (EOL) character at the end of each file in the specified directory (variable `P`).             |
| `add-eol-root`         | Adds an End-Of-Line (EOL) character at the end of each file in the project's root directory.                        |
| `install-compiler`     | Installs the compiler based on the value of the `compiler` variable (clang or gcc). It also installs the specified version. |
| `docker-install-compiler` | Same as `install-compiler`, but runs inside a Docker container.                                                  |
| `find-cxx-compiler`    | Finds the path to the C++ compiler based on the value of the `compiler` and `version` variables.                    |
| `find-c-compiler`      | Finds the path to the C compiler based on the value of the `compiler` and `version` variables.                      |
| `format`               | Formats the code, including using `clang-format` for files with the `.pp` extension, and adds an EOL character in specified directories. |
| `gen-queries`          | Runs the `generate_sql_queries.py` script to generate SQL queries with the specified flags.                        |
| `build-debug`          | Builds the project in debug mode using CMake.                                                                      |
| `build-release`        | Builds the project in release mode using CMake.                                                                    |
| `run`                  | Runs the compiled service with the specified configuration files.                                                  |
| `get_all_so`           | Copies all dynamic libraries required to run the service into the `_so` directory.                                |
| `tests`                | Runs tests for the service and regenerate api.yaml                                                                 |
| `build-docker`         | Builds the Docker image of the service, saves it to a file, and cleans up temporary files.                         |
| `release`              | Creates an archive with configuration files and other necessary files for deploying the container.                 |
| `start-docker`         | Prepares configuration files for the container and runs Docker Compose to start the container.                    |


## How to run

To start the service, you need to pass the path to the config and the path to the variables.
```sh
./build_release/service --config configs/static_config.yaml --config_vars configs/config_vars.yaml
```

You can also use ```make run```

## How to run via docker

You need to take adept_service.tar and container.tar from the releases.

```sh
docker load -i adept_service.tar
tar -xf container.tar
docker-compose up
```

## How to install dependencies

userver-openapi-extension has no dependencies except for userver and boost.pfr, and it is pulled using fetchContent. 
The userver requires a lot of pre-installed dependencies. (In fact, they can be supplied in different ways, but the one used in CI will be given here)

```sh
sudo apt install cmake
sudo apt install ninja-build
sudo make install-compiler compiler=clang version=17
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo tee /etc/apt/trusted.gpg.d/pgdg.asc &>/dev/null
cmake --preset=dev_release
sudo apt update
sudo apt install --allow-downgrades -y pep8 $(cat cmake_build/_deps/userver-src/scripts/docs/en/deps/<YOUR SYSTEM>.md | tr '\n' ' ')
```

[YOUR SYSTEM] example : ubuntu-22.04
The full list of supported ones can be viewed: https://github.com/userver-framework/userver/tree/develop/scripts/docs/en/deps

## How to build

To build a project, you need to install all the dependencies. 
The build is focused on *nix systems, windows is not supported. 
Alternatively, you can use WSL. 

```sh
git clone https://github.com/sabudilovskiy/ADEPT-test.git
cmake --preset=dev_release
make gen-queries
cmake --build <DIR> --target all
```

## How to build docker and release

```sh
cmake --preset=dev_release
make build-release
make build-docker
make releases
```

After all commands are executed correctly, container.tar and adept_service.tar will be in /release
