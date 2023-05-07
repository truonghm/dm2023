# Running the labworks

## Prerequisites

- Python 3.10
- Create a virtual environment and install the dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the labworks

```bash
cd labwork
```

Displaying help for arguments:

```bash
python 01.preprocessing.py --help
```

### Labwork 1

```bash
python 01.preprocessing.py -st=0.02 -ft=30 -n=1000
```

### Labwork 2

```bash
python 02.review.length.py
```
