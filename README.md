# Python GIL Comparison
This repository compares the performance of Python 3.13.1 with the GIL enabled and disabled.

## Create the Docker Images
### Build the Docker Image with GIL Enabled
```shell
docker build --no-cache --file python-3.13.1-bookworm-gil.Dockerfile --tag python:3.13.1-bookworm-gil .
```
### Build the Docker Image with GIL Disabled
```shell
docker build --no-cache --file python-3.13.1-bookworm-nogil.Dockerfile --tag python:3.13.1-bookworm-nogil .
```

## Check the GIL Status
### GIL-Enabled Image
Run `gil_status.py` to verify that the GIL is active:
```shell
docker container run --rm -it -v ${pwd}/src:/app -w /app python:3.13.1-bookworm-gil python gil_status.py
```
### GIL-Disabled Image
Run `gil_status.py` to verify that the GIL is disabled:
```shell
docker container run --rm -it -v ${pwd}/src:/app -w /app python:3.13.1-bookworm-nogil python gil_status.py
```

## Performance Comparison With and Without GIL
### Prime Number Calculation
#### GIL Enabled
Run `prime_counter.py` to measure the performance of prime number calculations in Python 3.13.1 with the GIL:
```shell
docker container run --rm -it -v ${pwd}/src:/app -w /app python:3.13.1-bookworm-gil python prime_counter.py
```
#### GIL Disabled
Run `prime_counter.py` to measure the performance of prime number calculations in Python 3.13.1 with the GIL disabled: 
```shell
docker container run --rm -it -v ${pwd}/src:/app -w /app python:3.13.1-bookworm-nogil python prime_counter.py
```