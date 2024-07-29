import difflib
from typing import List

    # Define a function to get the similarity ratio

def sort_by_closest_match(source_column: str, destination_columns: List[str]):

    def similarity_ratio(s):
        return difflib.SequenceMatcher(None, source_column, s).ratio()

    # Create a dictionary with similarity ratios
    similarity_dict = {s: similarity_ratio(s) for s in destination_columns}
    
    # Sort the dictionary by similarity ratio in descending order
    sorted_similarity_dict = dict(sorted(similarity_dict.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_similarity_dict

def compare_each_column_to_destination(source_columns: List[str], destination_columns: List[str]):

    highest_match_source_column = ""
    highest_match_destination_column = ""

    overall_highest_match = 0

    for source_column in source_columns:
        matching_dict = sort_by_closest_match(source_column, destination_columns)
    
        highest_match_dest_col = next(iter(matching_dict))
        highest_match_score = matching_dict[highest_match_dest_col]
    
        if (highest_match_score > overall_highest_match):
            overall_highest_match = highest_match_score
            highest_match_source_column = source_column
            highest_match_destination_column = highest_match_dest_col

    return highest_match_source_column, highest_match_destination_column;

def sudoku_matching_algorithm(source_columns: List[str], destination_columns: List[str]):
    # compare each column in the source to ALL the columns in the destination and creating matching scores
    # Then for each column, find the one with the highest probability match
    # The create a mapping for the source and destination, remove them from the original sets, and run the algorithm again
    # do this over and over again until a mapping has been found for every source column

    mapping = {}

    # while source columns size > 0
    while source_columns:
        highest_match_source_column, highest_match_destination_column = compare_each_column_to_destination(source_columns, destination_columns)
        mapping[highest_match_source_column] = highest_match_destination_column
        source_columns.remove(highest_match_source_column)
        destination_columns.remove(highest_match_destination_column)

    return mapping
        

