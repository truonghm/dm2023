# Project for Data Mining 2023 Class

## Requirements

- Topic: Image instance segmentation using Mean-shift clustering
- Input: RGB image
- Output: Instance segmented image with highlighted segments

## Set up

1. Create a virtual environment
2. Install the required packages: 

```bash
pip install -r requirements.txt
```

## Run the project

First, change directory into the project folder:

```bash
cd project
```

The clustering algorithm can be run with the following command:

```bash
python segment.py --input <input_file> --output <output_file> --kernel <kernel> --bandwidth <bandwidth> --verbose True
```

To see the detailed description of the arguments, run:

```bash
python segment.py --help
```

For example, to run the algorithm with:

- [test image](/project/data/china_resized.jpg), run:
- Flat kernel with bandwidth = 0.5:
- Output image: [output.jpg](/project/data/output.jpg)

```bash
python segment.py --input data/china_resized.jpg --output data/output_flat.jpg --kernel flat --bandwidth 0.5
```

## Project structure

```
dm2023
├─ .gitignore
├─ README.md
├─ project
│  ├─ core
│  │  ├─ __init__.py
│  │  ├─ clustering
│  │  │  ├─ MeanShiftClustering.py
│  │  │  └─ __init__.py
│  │  ├─ dataobject
│  │  │  ├─ DataVector.py
│  │  │  ├─ Point.py
│  │  │  └─ __init__.py
│  │  ├─ kernel
│  │  │  ├─ Kernel.py
│  │  │  └─ __init__.py
│  │  └─ utils
│  │     └─ __init__.py
│  ├─ notebooks
│  │  ├─ .gitignore
│  │  └─ test.ipynb
│  ├─ report
│  ├─ segment.py
│  └─ tests
├─ pyproject.toml
└─ requirements.txt
```

