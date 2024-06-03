# AI Recycle App

## How to setup environment for the application
Note: It is recommended to use Python 3.11 or above for this application.
### 1. Create a virtual environment:
```bash
$ python3.11 -m venv venv
```
### 2. Activate the virtual environment:
```bash
$ source venv/bin/activate
```
### 3. Install requirements (including development and testing requirements):
```bash
$ pip install -r requirements.txt
```

## How to run the application
### 1. Activate the virtual environment:
```bash
$ source venv/bin/activate
```
### 2. Set the environment variables:
Copy the .env.example file to .env and set the values for the environment variables such as OPENAI_API_KEY, LANGSMITH_API_KEY, and IMGBB_API_KEY.
### 3. Run the Streamlit server:
```bash
$ streamlit run app.py
```
This would run the application server in the default 8501 port. You can access the application by visiting http://localhost:8501 in your browser.

