# infusevideo-sdk

This is the Infuse Video SDK for Python.

At the moment, this is a very basic initial version that takes care of authentication, and
otherwise exposes a simple REST client. More features and documentation are going to come soon.

## Requirements
* [Python](https://www.python.org/) 3.9 or newer

## Installation
It's always advisable to setup a [virtualenv](https://docs.python.org/3/library/venv.html) when
working with third-party packages, in order to keep this package and dependencies from cluttering
the globally installed packages, and vice versa. If you do not know how to set one up, refer to the
[Python documentation on venv](https://docs.python.org/3/library/venv.html).

After creating and also activating the virtualenv, installation is as simple as

	pip install infusevideo-sdk

This will install a package named `infusevideo`, containing the SDK, into the virtualenv.

### Upgrading
Upgrading is as simple as running

	pip install --upgrade infusevideo-sdk

## Usage
In the current state, this is a simple wrapper around a REST/HTTP client. The `InfuseVideo` class
exposes five methods (`get`, `post`, `patch`, `put` and `delete`) indicating their respective HTTP
counterparts.

### API documentation
Please refer to [the current API documentation](https://api.infuse.video/apidoc/redoc) for an
overview of available actions on the API, request parameters and expected return values.
Authentication is already taken care of by the SDK, so that section of the API documentation may
be skipped.

### Example code
Simple code that calls the [List media](https://api.infuse.video/apidoc/redoc#operation/get_/media)
route on the Media endpoint:

	import infusevideo

	api = infusevideo.InfuseVideo()
	result = api.get("/media")
	print(result)


Create a new Media and upload a video file:

	import infusevideo

	api = infusevideo.InfuseVideo()
	result = api.post("/media", data={"name": "A name", "metadata": "Example metadata"})
	mediaId = result["mediaId"]
	
	result = api.put(f"/media/{mediaId}", fileName="/path/to/my/file.mp4")
	print(result)

#### Creating a sample configuration file
By default, the SDK will connect to the API, ask for your credentials interactively, and
attempt to obtain an authorization token with all permissions that were granted to you. If you have
access to multiple accounts, the token will be valid only for your default account. In order to
easily use multiple accounts, choose a different, limited, set of permissions or use non-interactive
M2M authentication, you will need to customise a profile in the configuration file. This
configuration file is normally located in the `.infusevideo/` directory in your home directory. If
you have not yet created this file, you can do so using the following code:

	import infusevideo

	path = infusevideo.Config.generate_sample_config()
	print(path)

This will create a sample configuration file with a default profile and a separate sample profile
for M2M authentication. It will then print the path where the configuration file was created, for future reference. There will be some inline comments explaining the various configuration options
that are available.
