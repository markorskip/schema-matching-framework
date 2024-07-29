
# Example usage
import unittest
from schema_matching_framework.sudoku_schema_matcher import sort_by_closest_match, sudoku_matching_algorithm
import logging

class SudokuSchemaMatcherTest(unittest.TestCase):
    
    def test_sort_by_closest_match(self):
        source_column = "employee.first_name"
        destination_columns = ["employee.fname", "employee.lname", "employee.mname", "employee.id", "employee.dob"]
        
        expected_match = 'employee.fname'

        result = sort_by_closest_match(source_column, destination_columns)
        print(result)

        # Check if the result matches the expected output
        self.assertTrue(expected_match in next(iter(result)))
        
        # Additional checks to ensure sorting is correct
        sorted_items = list(result.items())
        self.assertTrue(all(sorted_items[i][1] >= sorted_items[i + 1][1] for i in range(len(sorted_items) - 1)))

    def test_algorithm(self):
        source_columns = ["employee.first_name", "employee.last_name", "employee.middle_name", "employee.id", "employee.date_of_birth"]
        destination_columns = ["employee.fname", "employee.lname", "employee.mname", "employee.id", "employee.dob"]
        
        expected_result = {'employee.id': 'employee.id', 
                           'employee.last_name': 'employee.lname', 
                           'employee.first_name': 'employee.fname', 
                           'employee.middle_name': 'employee.mname', 
                           'employee.date_of_birth': 'employee.dob'}

        result = sudoku_matching_algorithm(source_columns, destination_columns)

        print(result)
        self.assertEqual(expected_result, result)

if __name__ == '__main__':
    unittest.main()