# cx
The ComputeX Python CLI lets you interact with ComputeX REST APIs and push images for your models to the ComputeX container registry.

## Installation

### Requirements
- Python >= 3.8

Run `pip install cx`.

## Command Line Interface
At any time, you can utilize the `--help` flag with any command or subcommand:

```shell
$ cx --help
Usage: cx [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  login
  ...
```

### Logging In
```shell
$ cx login --username {username} --password {password}
```

### Building an Image
WIP

### Pushing an Image
WIP

## Development

### Publishing to PyPI
The process for publishing to PyPI works as follows:

- Pull down the `main` branch.
- Tag it with the current version as specified in `pyproject.toml`.
- Push that tag to the repo, which...
- Triggers a GitHub Action workflow (`pypi.yml`) that pushes it to PyPI.

This can all be done simply by running the following `make` command:

```shell
make pypi-publish 
```

Assuming you have the ability to push a tag to the repo, you'll be able to publish to PyPI.

**WARNING:** if you do not specify a new version in `pyproject.toml`, the GHA workflow will fail due to an existing package being on PyPI.
