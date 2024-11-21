import unittest

# Sample test data
sample_data = [
    {"TableName": "ADMISSIONS", "TableDesc": "The ADMISSIONS table gives information regarding a patient’s admission to the hospital.",
     "ColumnName": "SUBJECT_ID", "ColumnDesc": "The ADMISSIONS table can be linked to the PATIENTS table using SUBJECT_ID"},
    {"TableName": "ADMISSIONS", "TableDesc": "The ADMISSIONS table gives information regarding a patient’s admission to the hospital.",
     "ColumnName": "HADM_ID", "ColumnDesc": "Each row of this table contains a unique HADM_ID, which represents a single patient’s admission to the hospital."},
    {"TableName": "CALLOUT", "TableDesc": "Information regarding when a patient was cleared for ICU discharge and when the patient was actually discharged.",
     "ColumnName": "SUBJECT_ID", "ColumnDesc": "patient corresponding to the given call out event"},
    {"TableName": "CALLOUT", "TableDesc": "Information regarding when a patient was cleared for ICU discharge and when the patient was actually discharged.",
     "ColumnName": "HADM_ID", "ColumnDesc": "hospital admission corresponding to the given call out event"},
]

expected_mapping = {
    "ADMISSIONS.SUBJECT_ID": "CALLOUT.SUBJECT_ID",
    "ADMISSIONS.HADM_ID": "CALLOUT.HADM_ID",
}

class TestColumnMatching(unittest.TestCase):
    def setUp(self):
        # Create Column objects for source and destination tables
        self.source_columns = [
            Column(data["TableName"], data["TableDesc"], data["ColumnName"], data["ColumnDesc"])
            for data in sample_data[:2]  # First two rows are source
        ]
        self.destination_columns = [
            Column(data["TableName"], data["TableDesc"], data["ColumnName"], data["ColumnDesc"])
            for data in sample_data[2:]  # Last two rows are destination
        ]

    def test_column_matching(self):
        # Run the matching algorithm
        result = match_columns(self.source_columns, self.destination_columns)

        # Verify the mapping
        for source, dest in expected_mapping.items():
            self.assertIn(source, result)
            self.assertEqual(result[source], dest)

if __name__ == "__main__":
    unittest.main()
