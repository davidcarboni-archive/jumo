# Aggregate loan calculation

## Prerequisites

Git
Python 3

## Running

    # git clone ...

Using Python 3 (e.g. virtualenv or pyenv)is available
    
    
    
    # python3

## Assumptions

CSV files are in the Excel "dialect"

Error handling could be improved

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

