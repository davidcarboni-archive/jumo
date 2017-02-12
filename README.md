# Aggregate loan calculation


## Prerequisites

It should be possible to "clone and run" this repo, providing the following two dependencies are satisfied:

  * Git
  * Python 3


## Running

First, clone the repo:

    # git clone https://github.com/davidcarboni/jumo.git

Using Python 3 (e.g. virtualenv or pyenv):
    
    # python loans.py
    
Or if Python 3 is available:

    # python3 loans.py


## Overview

The key assumption I've made in this code is that "calculation by tuple" refers to aggregating input data so that it can be queried using a combination of Network, Product and Month (composite key). I'm not 100% familiar with the term, but from reading through the exercise, this appears to be the intent.

The `loans.py` file therefore contains a class, `LoanAggregator`, which is capable of reading input files to update totals and counts and which can be queried using the `count(network, product, month)` and `total(network, product, month)` methods.

Additionaly there are three unit tests in `test.py` to check that CSV headers are correctly located and that the `count` and `total` methods arrive at the expected values.

I've included a bunch of comments in the code as I've worked through my reasoning, which should help to explain the things I have done as well as the things I've decided not to do.


## Assumptions

I've talked through most of the assumptions in comments in the code, but thought I'd add a few additional discussion points:

The main assumption is that, providing the data files to be read are being automatically generated, there should be a high degree of confidence in their format and correctness, for example constant and reliable headers and CSV rows of the correct length. If so, that means a bunch of checks can reasonably not be implemented in the code, enabling it to remain simpler and clearer to read. On the other hand, you'd want to check these assumptions against live data and take into account any scenarios that could lead to a malformed file being presented for processing.

One such "reliability shortcut" is in the processing of dates to extract month values. Rather than incur the expense of date parsing, the date strings can be accessed directly to substring the month value. This may well be sufficient for an initial iteration and the need for anything more complex can be assessed for a further iteration.

Error handling could be more robust, for example when opening and reading files. Whilst the system generating data files may be automated and reliable, the mechanism for reading them into this system may be less reliable (e.g. an S3 bucket where a network error might occur).

## Language choice

I decided to write this in Python for a couple of reasons:

  * Python is usually good for relatively performant data processing
  * It's also good for general simplicity and ease of iteration
  * Python should also make it particularly straightforward to run the code on both Mac and Linux
  * Java would likely be a relatively heavy choice for a task of this size and complexity
  * Golang would also be a good choice, although building/running from source would be less straightforward

In terms of a coding exercise, ease of development, iteration and running the code when received got extra weight in this choice!

## Performance and sizing

I thought I'd jot down some of my thoughts here around performance and sizing.

Perhaps initially counterintuitive is that I have chosen to go for a pretty basic design, using an in-memory dict to store incoming data.

The reason for this is that, at this stage, we don't have a view of the volume of data being processed, the speed with which it needs to be processed (it sounds like a month-end batch process) and the opportunity for breaking down the data set into manageable chunks.

As a result, I've opted to keep it simple at first in order to prove we can get the right results, with a view to "optimising late" - or at least when there's a clearer picture of intended scale - to avoid complexity if possible, so improving the chances of ongoing development and iteration, as well as having less moving parts to give it the best chance of working (and simplifying troubleshooting) when this gets to production.

Taking a guess at likely performance/sizing needs, if this is about selling products to individuals, it's likely to come out at "human scale" - that is, we're not talking about a fleet of tens of thousands of IoT devices delivering multiple readings on a per-second basis. If this is a scaling business, we may initially be looking at hundreds, then thousands, then tens of thousands (depending on the size of the market). If things go well, we could hit million scale, but we're probably not looking at billions or above.

It also sounds like this is a month-end batch process, so may not be time-critical. If so, an overnight run of a single Python process may have plenty of capacity to process the data. Providing the system can be designed to be stateless, options such as running a number of instances in parallel can quickly provide substantial capacity (and avoid the GIL which might be an issue with threading inside a single Python process).

If demand does exceed throughput, it may be time to consider Golang (or Java, or .Net, depending on what's important in the Juno context, and I would add that it probably also depends on the skills and preferences of the team). The task could be decomposed into a series of steps, with a view to running these concurrently, for example passing messages between queues and having workers (or microservices) process the data.

For the time being, a single-threaded, in-memory process is both fast and simple. However, there should be a question about data persistence. Whilst a console print-out or CSV output may be sufficient, it's likely that we'd want to store the results. Given a relatively small number of networks, products and months, a Json document would likely be a good option (as per the dict in this implementation). On the other hand, a straightforward single-table relational database would also be a neat fit for the data being stored. Again, it's going to depend on context and needs, but it would seem there's a good range of options. If the process were made concurrent, there would be a need to synchronize updates to the data store, but this shouldn't be an issue.

One interesting question is whether this needs an object-oriented design. It's certainly convenient in terms of the way this has been implemented, but there would be other ways to implement this. Because of the line-by-line nature of the data, a fairly straightforward data-in-data-out design could do the job - the only state being maintained here is for query purposes. If the results were stored in, say, a database, the code itself could be very simple indeed.                      

## Conclusion

Hopefully this has given you an idea of how I look at problems and the questions I ask to try and arrive at "right size, right tech" designs. For me, I think what's not built can be at least as important as what is built, so designing to "maximise work not done" is a really good way to keep things simple, clean, flexible and operational. Hopefully this resonates with you too.

---

David

