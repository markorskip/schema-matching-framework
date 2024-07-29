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

    # Compare each column to the destination list, and return the highest matching source and destination
    highest_match_source_column = source_columns[0]
    highest_match_destination_column = destination_columns[0] # init with something in case no matches

    overall_highest_match_score_for_all_columns = 0

    for source_column in source_columns:
        matching_dict = sort_by_closest_match(source_column, destination_columns)
    
        #Get the hightest match column
        match_dest_column_name = next(iter(matching_dict))
        match_score_for_this_column = matching_dict[match_dest_column_name]
    
        if (match_score_for_this_column > overall_highest_match_score_for_all_columns):
            overall_highest_match_score_for_all_columns = match_score_for_this_column
            highest_match_source_column = source_column
            highest_match_destination_column = match_dest_column_name

    print("Highest match: " + highest_match_source_column + ": " + highest_match_destination_column)
    print("Total score:")
    print(overall_highest_match_score_for_all_columns)
    return highest_match_source_column, highest_match_destination_column

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
        print("Removing source column:" + highest_match_source_column)

        source_columns.remove(highest_match_source_column)
        print("Removing destination column:" + highest_match_destination_column)
        destination_columns.remove(highest_match_destination_column)

        print("Remaining source and  destination columns")
        print (source_columns)
        print (destination_columns)

    return mapping
        

