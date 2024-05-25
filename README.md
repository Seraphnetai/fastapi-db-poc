# clearpill-db-poc

## Running the Application
### Update database URL, API key and chromium paths
To run the application, first update `alembic.ini` with the correct database URL:
    
```ini
sqlalchemy.url = postgresql://<username>:<password>@<host>:<port>/<database>
```

and do the same for `SQLALCHEMY_DATABASE_URL` in the `app/config.py` file:
    
```python 
SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<host>:<port>/<database>"
```

After that fill the environment variables in the `app/.env` file.
Finally, follow the [instructions](https://cloudbytes.dev/snippets/run-selenium-and-chrome-on-wsl2)  to set up the chromium paths in `app/utils.py`:

```python
homedir = os.path.expanduser("~")
chrome_options.binary_location = f"{homedir}/chrome-linux64/chrome"
webdriver_service = Service(f"{homedir}/chromedriver-linux64/chromedriver")`
```
or use the default paths for the chrome and chromedriver binaries if you are not using WSL2.

### Set up the environment
In order to install the environment using Poetry, run the command:

```bash
poetry install
```

TODO: Configuration for creating .venv in the project directory
A .venv folder should be created.

### Running the Application
Enter the Poetry shell from the main directory:

```bash
poetry shell
```

To apply migrations, run the following command in poetry shell:

```bash
alembic upgrade head
```

Then run the command:

```bash
uvicorn app.api:app --reload --port 8000
```

The port number can be changed or omitted, as it defaults to 8000.

### Building the Container for local development
In order to build the container for local development, first apply all changes mentioned in `Update database URL, API key and chromium paths` step and then update `docker-compose-build.yml` with the correct database credentials in the `environment` sections of the `clearpill_db_poc` and `db` services:
    
```yaml
DATABASE_URL: postgresql://<username>:<password>@db:5432/<database
POSTGRES_USER: <username>
POSTGRES_PASSWORD: <password>
POSTGRES_DB: <database>
```

Then run the following command:

```bash
./build-local-container.sh
```

The image will be built locally and started using docker-compose. It might take a while to build the image for the first time.