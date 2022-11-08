# CodeChallenge - Pedro Carmine

The code has been developed using Python 3.10.8

Please note that an older python version may not support [Streamlit](https://docs.streamlit.io/library/changelog#:~:text=Copy-,Version%201.14.0,-Release%20date%3A%20October) version 1.14.0

### Creating virtual environment
```bash
python -m pip venv .venv
```

### Activating the virtual environment

- For Linux/MacOS:
 
```bash
source .venv/bin/activate
```
- For Windows:

```
.\venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Running the code
```bash
streamlit run main.py
```

### Overall notes
- What could have been improved?
1. Operations/calculations using numpy to improve code performance/readability.
2. Better usage of Pandas library.
3. Reduce the amount of times that the yfinance API is fetched.
4. Improve code for a production environment, since there is no previous experience in this field.
5. Code organization/structure.

- Commentary

Doing this challenge showed me how much can be done using Python libraries that I have not used before with just a few lines of code. It was extremely fun and challenging at the same to work with libraries that I had to learn from zero (and learned just the tip of the iceberg) and see how things worked together in the end to produce a dashboard.
