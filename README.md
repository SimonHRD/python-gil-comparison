# Python GIL Comparison


🚀 Exploring Python Without the GIL! 🚀

This repository benchmarks the performance of Python 3.13.1 with and without the Global Interpreter Lock (GIL) using real-world workloads.

📖 Read the full analysis and benchmark results in my blog post:<br>
👉 [Exploring Python 3.13: Hands-on with the GIL Disablement](https://simonontech.hashnode.dev/exploring-python-313-hands-on-with-the-gil-disablement)
 
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
This section verifies whether the **Global Interpreter Lock (GIL)** is enabled or disabled in the Python environment. Running `gil_status.py` will confirm if the GIL is active, ensuring the correct interpreter settings before executing performance benchmarks.
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
This benchmark tests a **CPU-intensive mathematical computation** by counting prime numbers within a given range. The test is executed in both **single-threaded** and **multi-threaded** modes to measure the impact of the GIL on parallel performance.

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

### Loan Risk Scoring Benchmark
This benchmark simulates a **real-world financial workload** by analyzing loan applications and calculating a **risk score** for each applicant. The dataset is processed in both **single-threaded** and **multi-threaded** modes to compare performance with and without the GIL.

#### GIL Enabled
Run `loan_risk_scoring_benchmark.py` to measure the performance of risk scoring in Python 3.13.1 with the GIL:
```shell
docker container run --rm -it -v ${pwd}/src:/app -v ${pwd}/data:/data -w /app python:3.13.1-bookworm-gil python loan_risk_scoring_benchmark.py
```
#### GIL Disabled
Run `loan_risk_scoring_benchmark.py` to measure the performance of risk scoring in Python 3.13.1 with the GIL disabled:
```shell
docker container run --rm -it -v ${pwd}/src:/app -v ${pwd}/data:/data -w /app -e PYTHON_GIL=0 python:3.13.1-bookworm-nogil python loan_risk_scoring_benchmark.py
```