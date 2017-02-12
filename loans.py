import csv, sys
import json


class LoanAggregator:
    """This class processes CSV input files"""

    # Dict to hold CSV data
    data = None

    # Header information
    header = None

    MSISDN = 'MSISDN'
    NETWORK = 'Network'
    DATE = 'Date'
    PRODUCT = 'Product'
    AMOUNT = 'Amount'

    msisdn = -1
    network = -1
    date = -1
    product = -1
    amount = -1

    def __init__(self):
        self.data = {}

    def read_input(self, filename):
        """Reads an input CSV and processes the rows

        :param filename: The file to be read in.
        NB We're making some assumptions here around the file being a reliable, stable format.
        For example, specifying a single-quote character when reading the CSV. The chances are
        that input files are being generated automatically, so should be consistent, but we'd
        want to test this assumption by looking at real data coming out of production systems.
        """
        # Read CSV file
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, quotechar="'")
            try:
                for row in reader:
                    if self.header is None:
                        self.header = row
                        #print("Loaded header row: " + repr(self.header))
                        #print(len(self.header))
                        self._index_headers(row)
                    else:
                        self._process_row(row)
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
        #print(json.dumps(self.data))

    def _index_headers(self, header):
        """Determine the indices of the expected column headers in each row.

        This isn't strictly required if the input file format is known and does not change.
        In fact, if that is the case, these indices could be safely hard-coded, providing
        the production deployment of this code can be updated with relative ease.
        Either way, a more basic solution that this would likely suffice for an initial
        implementation and could be made more subtle in a future iteration if needed.
        """
        for i in range(0, len(header)):
            if self.header[i] == self.MSISDN:
                self.msisdn = i
            elif self.header[i] == self.NETWORK:
                self.network = i
            elif self.header[i] == self.DATE:
                self.date = i
            elif self.header[i] == self.PRODUCT:
                self.product = i
            elif self.header[i] == self.AMOUNT:
                self.amount = i
            #print(repr(i) + " - " + repr(self.header[i]))

        # NB we could raise a value error here if any of the heading indices
        # have not been updated from -1

    def _process_row(self, row):
        """ Aggregates the data from a single row.

        This method could check the length of an incoming CSV row, however if we assume that data files
        are being reliably and probably automatically generated, then the format is essentially guaranteed
        to be correct. Omitting this check makes the code simpler and more direct, but we'd want to try
        this out in a real environment to make sure that these expectations are valid.

        In the same way, we're using a simple substring to get the month from the date, on the basis that
        the date format is likely to be reliable. This saves parsing to a date and extracting the month
        when the month is available directly in the input string. If necessary, this could be improved in
        a future iteration, however consideration should be given to the expense of date parsing and the
        potential for unexpected results if we happent get caught up with e.g. timezones, depending on
        the settings of the underlying system(s) where the deployed code will run.

        We're also assuming the amount is a well-formed integer, but allowing for that to come in as 000.00.
        """

        # Extract the values from the row
        network = row[self.network]
        product = row[self.product]
        date = row[self.date]
        month =date[3:6]
        amount = row[self.amount]

        # Ensure the Dict has the necessary entries
        if network not in self.data:
            self.data[network] = {}
        if product not in self.data[network]:
            self.data[network][product] = {}
        if month not in self.data[network][product]:
            self.data[network][product][month] = {"count": 0, "total": 0}

        # Update count and total
        self.data[network][product][month]["count"] += 1
        self.data[network][product][month]["total"] += int(float(amount))

    def count(self, network, product, month):
        count = 0
        if network in self.data:
            if product in self.data[network]:
                if month in self.data[network][product]:
                    count = self.data[network][product][month]["count"]
        return count

    def total(self, network, product, month):
        total = 0
        if network in self.data:
            if product in self.data[network]:
                if month in self.data[network][product]:
                    total = self.data[network][product][month]["total"]
        return total


if __name__ == '__main__':

    print("Data processed:")
    print()

    print("Json:")
    loanAggregator = LoanAggregator()
    loanAggregator.read_input("data/Loans.csv")
    print(json.dumps(loanAggregator.data))
    print()

    print("Results:")
    for network in loanAggregator.data:
        for product in loanAggregator.data[network]:
            for month in loanAggregator.data[network][product]:
                record = loanAggregator.data[network][product][month]
                total = record["total"]
                count = record["count"]
                print(network + ", " + product + ", " + month + ": total=" + str(total) + " count=" + str(count))

