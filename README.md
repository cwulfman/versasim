# Versasim
A lightweight simulator to help in testing.

## Installation
1. Download the *.whl file from the `dist/` directory
2. Use the standard `pip install` method to install the software

For example

``` shell
    wget ../versasim-0.1.0-py3-none-any.whl
    pip install versasim-0.1.0-py3-none-any.whl
```

## Configuration
Versasim requires credentials to interact with Airtable: the identifier of the Airtable database (the 'base') and an api key to access it. Create a `.env` file in the versasim directory and set two environment variables:

``` text
    BASE_ID = '<the_base_id>'
    API_KEY = '<your_api_key>'
```

## Running the Program
Move into the interior `versasim` directory and start the server:

``` shell
    cd versasim
    uvicorn main:app
```

The server is now running on port 8000 at localhost: e.g., [http://127.0.0.1:8000](http://127.0.0.1:8000).
