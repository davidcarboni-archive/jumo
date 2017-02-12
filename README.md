# Aggregate loan calculation

## Prerequisites

Git
Python 3

## Running

    # git clone ...

Using Python 3 (e.g. virtualenv or pyenv):
    
    # python loans.py
    
Or if Python 3 is available:

    # python3 loans.py

## Assumptions

CSV files are in the Excel "dialect"

Error handling could be improved

Assume headers are constant / reliable

Date format is reliable - rather than parse the date, the month can be extracted as a substring, which may be sufficient

## Language choice

Java too heavy - too much boilerplate.

Python good for what sholud be a relatively straightforward data processing task.

For high performance / throughput particularly if concurrency is a consideration, consider Golang.

## Performance and sizing

What are the performance needs?
 
 What are the data volumes?
 
Dict is a good solution for in-memory processing while input is relatively small

Multiple CSVs? Process in parallel & aggregate

how are files delivered? push/pull?

One large CSV? Read and send to processors?

Performance? Consider Golang.

Database?                         

Does this need to be OO? More of a batch-processing job?






Concurrent updates need to be synchronised.

