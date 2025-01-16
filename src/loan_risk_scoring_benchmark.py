import math
import pandas as pd
import threading
import time


def main() -> None:
    INPUT_FILE = "/data/loan_data.parquet"
    NUM_THREADS = 4   

    # Single-threaded execution
    start_time = time.time()
    result_single = risk_scoring_single_threaded(INPUT_FILE)
    end_time = time.time()
    print(f"Single-threaded execution time: {end_time - start_time:.2f} seconds, high-risk loans: {result_single}")

    # Multi-threaded execution
    start_time = time.time()
    result_multi = risk_scoring_multi_threaded(INPUT_FILE, NUM_THREADS)
    end_time = time.time()
    print(f"Multi-threaded execution time: {end_time - start_time:.2f} seconds, high-risk loans: {result_multi}")
   
   
def risk_scoring_single_threaded(path:str) -> None: 
    chunks = load_parquet_in_chunks(path, chunk_size=50000)
    high_risk_loans = 0
    for chunk in chunks:
        high_risk_loans += process_chunk(chunk)
    return high_risk_loans


def risk_scoring_multi_threaded(path:str, num_threads:int) -> int:
    chunks = list(load_parquet_in_chunks(path, chunk_size=50000))  # Convert generator to list for repeatable indexing
    high_risk_counts = [0] * len(chunks)  # Ensure results list matches the number of chunks

    def worker(chunk_index):
        # Process the chunk and store the result in the corresponding index
        high_risk_counts[chunk_index] = process_chunk(chunks[chunk_index])

    # Create and start threads
    threads = []
    for i in range(len(chunks)):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Return the total sum of high-risk loans
    return sum(high_risk_counts )

def process_chunk(chunk:pd.DataFrame) -> int:
    """Calculate risk scores for a chunk of data."""
    high_risk_loans = 0
    for _, row in chunk.iterrows():
        risk_score = calculate_risk_score(
            applicant_income=row.get("AMT_INCOME_TOTAL", 0),
            loan_amount=row.get("AMT_CREDIT", 1),
            dependents=row.get("CNT_CHILDREN", 0),
            credit_history=row.get("TARGET", 0)
        )

        if risk_score > 0.8:
            high_risk_loans += 1

    return high_risk_loans


def calculate_risk_score(applicant_income:int, loan_amount:int, dependents:int, credit_history:int) -> float:
    """Simulate a risk scoring computation with CPU-intensive operations."""
    try:
        income_to_loan_ratio = applicant_income / loan_amount
    except ZeroDivisionError:
        income_to_loan_ratio = 0
        
    risk = 0
    
    # Simulate a CPU-intensive operation for benchmarking purposes only
    for _ in range(100):  # Increase iterations to simulate CPU load
        risk += math.sqrt(income_to_loan_ratio) * math.sin(dependents) ** 2
        risk = (risk % 1) * 100
        
    risk -= credit_history * 10
    return max(0, min(1, risk / 100))  # Normalize between 0 and 1


def load_parquet_in_chunks(path, chunk_size):
    """Load a Parquet file and yield chunks of data."""
    df = pd.read_parquet(path)
    for i in range(0, len(df), chunk_size):
        yield df.iloc[i:i + chunk_size]
        

if __name__ == '__main__':
    main()
