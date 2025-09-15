![workflow](https://github.com/Danodya/movie-client/actions/workflows/ci.yml/badge.svg)

# Movie Client CLI
A command-line interface (CLI) application for managing and interacting with a movie database. 
This application communicates with the `movie-server` using an API endpoint to authenticate and fetch movie data.

## **Project Structure**
Main source code for the client app is located in the `client_app_cli` directory, with separate directories for 
each component of the application, such as argument parsing, authentication, constants, exceptions, and the core
fetching logic to make the codebase modular and maintainable.

Unit tests are organized in the `tests` directory separately to ensure code quality and reliability.

The project also includes a `Dockerfile` for containerization, an `entrypoint.sh` script to run the app inside the container,
and a `main.py` file as the main executable entry point for the CLI.

All dependencies are listed in the `requirements.txt` file, and the current version of the app is stored in the `.version` file.

[`ruff`](https://docs.astral.sh/ruff/), [`black`](https://github.com/psf/black), and [`mypy`](https://github.com/python/mypy) are used for linting, formatting, and type checking, respectively, to maintain code quality.

```

movie-client/
├── .github/workflows/          # GitHub Actions workflows for CI/CD
│   └── ci.yml                  # Runs linting, type checking, tests, Docker build and push
├── client_app_cli/             # Main source code for the client app
│   ├── arguments/              # CLI argument parsing logic
│   ├── auth/                   # Handles authentication with the server
│   ├── constants/              # Application constants (default configs, URLs, etc.)
│   ├── exceptions/             # Custom exception classes
│   └── fetcher/                # Core logic for fetching movie data
│       └── movie_fetcher.py    # Fetch movies by year and handle pagination
├── tests/                      # Unit and integration tests
├── Dockerfile                  # Docker image definition for the project
├── entrypoint.sh               # Entrypoint script to run the app inside Docker
├── main.py                     # Main executable entry point for the CLI
├── requirements.txt            # Python dependencies
├── .version                    # Stores the current version of the app
└── README.md                   # Project documentation

```
## **Requirements**

- **Python** 3.10 or higher
- **pip** (Python package manager)
- **Docker**

## **Running**
>[!IMPORTANT]
> This is the recommended way to run the application.
> If you want to run the application from source, see the [Build from source](#build-from-source) section below.

With the CI pipeline, the Docker image is built and pushed to GitHub Container Registry.

Both the `movie-server` and the `movie-client` are packaged inside the same Docker image, 
and both will start automatically when the container runs with the entrypoint script with the provided arguments.

>[!NOTE]
> If the `movie-client` needs to run by logging into the container, change the `entrypoint.sh` by replacing the last line with `bash`.
> 
> For example, to run the client application for the years 1940 and 1950 by logging into the container:
> ```bash
> docker run -it ghcr.io/danodya/jr103155:1.0.0     # Logs into the container because the entrypoint script ends with bash
> python movie-client/main.py -y 1940 1950          # Runs the client application for 1940 and 1950
> ```

To run the application using Docker, use the following command:
Provide only the year or years separated by spaces as arguments (e.g., 1940 1950):
```bash
docker run -it ghcr.io/danodya/jr103155:1.0.0 1940 1950
```
If you want to provide environment variables for the API URL, username, and password, you can do so using the `-e` flag:
```bash
docker run -it -e MOVIE_API_BASE_URL="http://localhost:8080/" -e MOVIE_API_USERNAME="username" -e MOVIE_API_PASSWORD="password" ghcr.io/danodya/jr103155:1.0.0 1940 1950
```

## **Build from source**
1. Clone the repository:
```bash
git clone https://github.com/Danodya/movie-client.git && cd movie-client
```
2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Provide the following environment variables:
```bash
export MOVIE_API_BASE_URL="http://localhost:8080/"   # URL of the movie-server
export MOVIE_API_USERNAME="username"                 # Username for API authentication
export MOVIE_API_PASSWORD="password"                 # Password for API authentication
```
or provide them in the command line:
```bash
MOVIE_API_BASE_URL="http://localhost:8080/" MOVIE_API_USERNAME="username" MOVIE_API_PASSWORD="password" python main.py -y 1940 1950
```

>[!NOTE]
> The command above overrides the environment variables exported above in step 4.

5. Run the application:

To fetch movies for specific years, we need the movie server running and accessible. Run movie-server first, then execute:
```bash
python main.py -y 1940 1950
```
## **Example Output**
```
Starting movie-client...
Fetching movies by year:
============================

Results for fetched movies:

Year 2020 has 15 movies.
Year 2021 has 23 movies.
```

## **Testing**
Run the tests using `pytest`:
```bash
pytest -vx
``` 
Test coverage for the overall project is approximately 89%. Coverage report is as follows:
```

Name                                          Stmts   Miss  Cover
-----------------------------------------------------------------
client_app_cli/__init__.py                        0      0   100%
client_app_cli/arguments/__init__.py              0      0   100%
client_app_cli/arguments/argument_parser.py       9      9     0%
client_app_cli/auth/__init__.py                   0      0   100%
client_app_cli/auth/authenticator.py             22      0   100%
client_app_cli/constants/__init__.py              0      0   100%
client_app_cli/constants/constant.py              5      0   100%
client_app_cli/exceptions/__init__.py             0      0   100%
client_app_cli/exceptions/exceptions.py           2      0   100%
client_app_cli/fetcher/__init__.py                0      0   100%
client_app_cli/fetcher/movie_fetcher.py          42      0   100%
-----------------------------------------------------------------
TOTAL                                            80      9    89%

```

## **Continuous Integration**
The project uses GitHub Actions for continuous integration. The CI pipeline is defined in `.github/workflows/ci.yml`
and includes steps for linting, formatting, type checking, running tests, building the Docker image, and pushing it to GitHub Container Registry.

All the linting and tests are triggered on push to any branch. Docker build and push to container registry occur only upon pushes to `main` after successful linting and testing stages.

Example commands used in the CI:
* Linting: `ruff check .`
* Formatting: `black --check .`
* Type Checking: `mypy .`
* Testing: `pytest -vx`

## **Versioning**
The current version of the application is stored in the `.version` file. Update this file to change the version number.
```
1.0.0
```
