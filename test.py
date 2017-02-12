import unittest
import loans
import json


class TestLoans(unittest.TestCase):

    def test_headers(self):
        """
        Checks that the header values are correctly located and are at the indices in the test data.

        We could make this more flexible by reading the test csv directly here in the test and comparing the read
        header order to the order determined by the class. This would be useful if/when we have multiple test files.
        """

        # Given
        # A data file
        filename = "data/Test.csv"
        loanAggregator = loans.LoanAggregator()

        # When
        # We read the test data
        loanAggregator.read_input(filename)

        # Then
        # The indices in the header should be correctly identified: "MSISDN", "Network", "Date", "Product", "Amount"
        self.assertNotEqual(loanAggregator.msisdn, -1, "MSISDN column not found in input")
        self.assertEqual(loanAggregator.msisdn, 0, "Incorrect MSISDN column index returned")
        self.assertNotEqual(loanAggregator.network, -1, "Network column not found in input")
        self.assertEqual(loanAggregator.network, 1, "Incorrect Network column index returned")
        self.assertNotEqual(loanAggregator.date, -1, "Date column not found in input")
        self.assertEqual(loanAggregator.date, 2, "Incorrect Date column index returned")
        self.assertNotEqual(loanAggregator.product, -1, "Product column not found in input")
        self.assertEqual(loanAggregator.product, 3, "Incorrect Product column index returned")
        self.assertNotEqual(loanAggregator.amount, -1, "Amount column not found in input")
        self.assertEqual(loanAggregator.amount, 4, "Incorrect Amount column index returned")

    def test_count(self):
        """Checks that count values are correctly calculated.

        This purposely checks a couple of non-existent values to ensure we don't get an error.

        The data/Test.csv file has been tweaked to duplicate the last line of data/Loans.csv so that we can demonstrate
        a count greater than one.

        This test uses the expected values in Test_counts.json. It could be made more adaptable because currently
        you'd have to know to keep the json in sync with the csv file. Splitting the job between two files is at
        best a drag and at worst creates an opportunity for error, so it would be nice to move to a neater solution.
        """

        # Given
        # A data file
        filename = "data/Test.csv"
        loanAggregator = loans.LoanAggregator()
        with open('data/Test_counts.json') as data_file:
            expected = json.load(data_file)

        # When
        # We read the test data
        loanAggregator.read_input(filename)

        # Then
        # The counts should be as expected
        for network in expected:
            for product in expected[network]:
                for month in expected[network][product]:
                    count = loanAggregator.count(network, product, month)
                    self.assertEqual(count, expected[network][product][month],
                                     "Unexpected count: " + network + "/" + product + "/" + month + ": " + str(count))

    def test_total(self):
        """Checks that total values are correctly calculated.

        This purposely checks a couple of non-existent values to ensure we don't get an error.

        The data/Test.csv file has been tweaked to duplicate the last line of data/Loans.csv so that we can demonstrate
        a total that is more than just the value of a single row.

        Similar to test_count, his test uses the expected values in Test_totals.json. It could be made more adaptable
        because currently you'd have to know to keep the json in sync with the csv file. Splitting the job between
        two files is at best a drag and at worst creates an opportunity for error, so it would be nice to move to a
        neater solution.
        """

        # Given
        # A data file
        filename = "data/Test.csv"
        loanAggregator = loans.LoanAggregator()
        with open('data/Test_totals.json') as data_file:
            expected = json.load(data_file)

        # When
        # We read the test data
        loanAggregator.read_input(filename)

        # Then
        # The amounts should be as expected
        for network in expected:
            for product in expected[network]:
                for month in expected[network][product]:
                    total = loanAggregator.total(network, product, month)
                    self.assertEqual(total, expected[network][product][month],
                                     "Unexpected count: " + network + "/" + product + "/" + month + ": " + str(total))


if __name__ == '__main__':
    unittest.main()
