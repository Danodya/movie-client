![workflow](https://github.com/Danodya/movie-client/actions/workflows/ci.yml/badge.svg)

# Movie Client CLI
A command-line interface (CLI) application for managing and interacting with a movie database. 
This application communicates with the movie-server using RESTful API endpoint to authenticate and fetch movie data.

## **Project Structure**
Main source code for the client app is located in the `client_app_cli` directory, with separate directories for 
each component of the application, such as argument parsing, authentication, constants, exceptions, and the core
fetching logic to make the codebase modular and maintainable.

Unit tests are organized in the `tests` directory separately to ensure code quality and reliability.

The project also includes a `Dockerfile` for containerization, an `entrypoint.sh` script to run the app inside Docker,
and a `main.py` file as the main executable entry point for the CLI.

All dependencies are listed in the `requirements.txt` file, and the current version of the app is stored in the `.version` file.

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
- **Docker** (optional, for containerization)

## **Running**
With the CI pipeline, the Docker image is built and pushed to GitHub Container Registry.

To run the application using Docker, use the following command:
Provide only the year or years separated by spaces as arguments (e.g., 1940 1950):
```bash
docker run --it ghcr.io/danodya/jr103155:1.0.0 1940 1950
```
## **Build from source**
1. Clone the repository:
```bash
git clone https://github.com/Danodya/movie-client.git
cd movie-client
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
export MOVIE_API_URL="http://localhost:8000"  # URL of the movie-server
export MOVIE_API_USER="username"              # Username for API authentication
export MOVIE_API_PASSWORD="password"          # Password for API authentication
```
or provide them in the command line:
```bash
MOVIE_API_URL="http://localhost:8000" MOVIE_API_USER="username" MOVIE_API_PASSWORD="password" python main.py 1940 1950
```
5. Run the application:

To fetch movies for specific years, we need the movie server running and accessible. Run movie-server first, then execute:
```bash
python main.py -y 1940 1950
```
## **Example Output**
```
Starting movie-client...
Fetching movies by year:
Year 2020 has 15 movies.
Year 2021 has 23 movies.
```

## **Testing**
Run the tests using `pytest`:
```bash
pytest -vx
``` 

## **CI**
The project uses GitHub Actions for continuous integration. The CI pipeline is defined in `.github/workflows/ci.yml`
and includes steps for linting, formatting, type checking, running tests, building the Docker image, and pushing it to GitHub Container Registry.

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
