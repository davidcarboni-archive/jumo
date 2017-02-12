import unittest
import loans


class TestLoans(unittest.TestCase):

    def test_headers(self):
        """
        Checks that the header values are correctly located and are at the indices in the test data.

        We could make this more flexible by reading the test csv directly here in the test and comparing the read
        header order to the order determined by the class. This would be useful if/when we have multiple test files.
        """

        # Given
        # A data file
        filename = "data/Loans.csv"
        loanAggregator = loans.LoanAggregator()

        # When
        # We instantiate the class
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
        # Given


        # When

        # Then

        pass

    def test_stuff(self):
        # Given

        # When

        # Then

        pass



if __name__ == '__main__':
    unittest.main()
