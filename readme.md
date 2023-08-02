# uStorage

## About
This is my **experimental** project to develop something like a object-storage.

## Concepts
- Make simple Web interface
- To use SQLite as a object storage
  - According to the SQLite's document, it is ~35 % faster than file systems. So I want to test if using SQLite as a object storage achive performance high enough.

## Usage

### Requirements
- Python ^3.11

### Install and Run
1. Clone this repository
``` shell
git clone <this repositry>
```

2. Move to ustorage directory
``` shell
cd ./ustorage/
```

3. Install dependency with poetry and run the module
``` shell
poetry install
poetry run python -m ustorage
```