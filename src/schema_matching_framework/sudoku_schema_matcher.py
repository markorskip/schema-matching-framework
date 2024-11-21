import difflib
from typing import List, Dict

# Define a new structure for columns
class Column:
    def __init__(self, table_name: str, table_description: str, column_name: str, column_description: str):
        self.table_name = table_name
        self.table_description = table_description
        self.column_name = column_name
        self.column_description = column_description

    def __str__(self):
        return f"{self.table_name}.{self.column_name} ({self.table_description}, {self.column_description})"

def calculate_similarity(source: str, destination: str) -> float:
    """Calculate similarity between two strings."""
    return difflib.SequenceMatcher(None, source, destination).ratio()

def compare_columns(source_column: Column, destination_column: Column) -> float:
    """Compare a source column with a destination column based on multiple attributes."""
    name_similarity = calculate_similarity(source_column.column_name, destination_column.column_name)
    description_similarity = calculate_similarity(source_column.column_description, destination_column.column_description)
    table_name_similarity = calculate_similarity(source_column.table_name, destination_column.table_name)
    table_description_similarity = calculate_similarity(source_column.table_description, destination_column.table_description)

    # Weighted average of similarities
    return (name_similarity * 0.5 +
            description_similarity * 0.3 +
            table_name_similarity * 0.1 +
            table_description_similarity * 0.1)

def find_best_match(source_column: Column, destination_columns: List[Column]) -> Dict[str, float]:
    """Find the best match for a source column in the destination columns."""
    similarity_scores = {
        str(dest): compare_columns(source_column, dest)
        for dest in destination_columns
    }
    # Sort by similarity scores in descending order
    return dict(sorted(similarity_scores.items(), key=lambda item: item[1], reverse=True))

def match_columns(source_columns: List[Column], destination_columns: List[Column]) -> Dict[str, str]:
    """Match source columns to destination columns."""
    mapping = {}

    while source_columns:
        highest_match_score = 0
        best_source = None
        best_destination = None

        for source in source_columns:
            match_results = find_best_match(source, destination_columns)
            best_dest, score = next(iter(match_results.items()))
            if score > highest_match_score:
                highest_match_score = score
                best_source = source
                best_destination = best_dest

        if best_source and best_destination:
            mapping[str(best_source)] = best_destination
            source_columns.remove(best_source)
            destination_columns = [
                col for col in destination_columns if str(col) != best_destination
            ]

    return mapping

# Example Usage
source_columns = [
    Column("users", "User table", "user_id", "Unique identifier for user"),
    Column("users", "User table", "email", "User's email address"),
]

destination_columns = [
    Column("customers", "Customer table", "customer_id", "Unique identifier for customer"),
    Column("customers", "Customer table", "email_address", "Customer's email address"),
]

result = match_columns(source_columns, destination_columns)
for source, dest in result.items():
    print(f"{source} -> {dest}")
