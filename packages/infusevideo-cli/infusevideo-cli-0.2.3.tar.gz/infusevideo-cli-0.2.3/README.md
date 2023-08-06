# infusevideo-cli

This is a simple CLI utility for the Infuse Video API.

## Installation
### Requirements
* [Python](https://www.python.org/) 3.9 or newer

### Setting up the virtualenv
It is recommended to use a virtualenv to install this package and dependencies. This ensures your
normal system stays clean and none of the dependencies conflict with other packages on your
system.

Choose a directory where you want to install the CLI, and then run

	python3 -m venv infusevideo

or, on Windows,

	python.exe -m venv infusevideo

This will create a directory `infusevideo` containing the virtualenv.

### Installing the dependencies and the package itself
Simply run

	infusevideo/bin/pip install infusevideo-cli

or, on Windows,

	infusevideo\Scripts\pip install infusevideo-cli

and all the dependencies will be retrieved and installed automatically, after which the latest
version of the CLI is installed as well. At this point, the executables have been installed in

	infusevideo/bin/ivc
	infusevideo/bin/ivs

or, on Windows:

	infusevideo\Scripts\ivc.exe
	infusevideo\Scripts\ivs.exe

### PATH
In order to invoke the executables directly using just `ivc` and `ivs`, you can simply create a
symbolic link to them in a directory in your PATH, or alternatively (not recommended) you can copy
or move them into such a directory.

## Usage
There are two executables, `ivc` which is the normal CLI application, and `ivs` which is the same
as running `ivc --script`, as a convenience for running in scripts or any other environment where
human input is not available.

Running

	infusevideo/bin/ivc --help

or, on Windows:

	infusevideo\Scripts\ivc --help

will show the program usage.

### API documentation
Please refer to [the current API documentation](https://api.infuse.video/apidoc/redoc) for an
overview of available actions on the API, request parameters and expected return values.

### Upgrading
Upgrading is as simple as running

	infusevideo/bin/pip install --upgrade infusevideo-cli

or, on Windows:

	infusevideo\Scripts\pip install --upgrade infusevideo-cli

## Uninstalling
Removing the application is as simple as removing the `infusevideo` directory created when making
the virtualenv. Your configuration file and token cache are stored in the `.infusevideo`
sub-directory of your home directory, and may also be removed.
