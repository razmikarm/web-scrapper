# web-scrapper

A simple example of a scrapping app, which also shows scrapped data on web server

The scrapper uses `Top news` section of https://news.am/eng/ news website.

### Installation

> Considers that you have `python 3.9+` with `pip` and `venv` packages

1. Create a virtual environment

    ```python -m venv env```

2. Activate the virtual environment

    ```. venv/bin/activate```

3. Install requirements

    ```pip install -r requirements.txt```

4. Run web server

    ```uvicorn main:app```

5. Enjoy the app at http://127.0.0.1:8000/  :)

