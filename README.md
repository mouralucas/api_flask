# Flask API

Code teste for DevGrid

## Installation

Python virtual environment was used to develop the solution. 

For Windows 10:

```bash
python -m venv venv
venv\Scripts\activate
```

For Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Use the package manager pip to install the requirements available in requirements.txt. With the virtual environment activated:

```bash
pip install -r requirements.txt (Windows)
pip3 install -r requirements.txt (Linux)
```

The requirements needed to execute are listed below:

- Flask==2.0.2
- Flask-RESTful==0.3.9
- Flask-Caching==1.10.1
- requests==2.26.0
- Flask-Pydantic==0.9.0

To run the project:

```bash
python -m flask run (Windows)
python3 -m flask run (Linux)
```

## Usage

To get information from the API Postman can be used with the given URL available in the description document.

- /temperature/<city_name>
- /temperature?max=<max_number>

## Testing
To run the tests just execute the fallowing command in the terminal:

```bash
pip -m unittest tests/tests.py (Windows)
pip3 -m unittest tests/tests.py (Linux)
```

These tests consist in validate the return content in cases of success. It also validates the endpoint that get the n cached values based on parameter "max".

Edge case test are performed to check the response in cases that the city passed as parameter does not exist in Openweather API and also validate the error when passed a string to cached temperatures endpoint.
