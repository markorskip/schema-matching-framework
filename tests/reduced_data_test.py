import unittest
from typing import List, Dict

import difflib
from typing import List, Dict

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import Levenshtein

# Define Column class for source and destination schema representation
class Column:
    def __init__(self, table_name: str, table_desc: str, column_name: str, column_desc: str):
        self.table_name = table_name
        self.table_desc = table_desc
        self.column_name = column_name
        self.column_desc = column_desc

    def __str__(self):
        return f"{self.table_name}.{self.column_name}"

def calculate_similarity_tfidf(str1: str, str2: str) -> float:
    """
    Calculate similarity using TF-IDF and cosine similarity.
    """
    vectorizer = TfidfVectorizer().fit([str1, str2])
    tfidf_matrix = vectorizer.transform([str1, str2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]

def calculate_similarity_levenshtein(str1: str, str2: str) -> float:
    """
    Calculate similarity using normalized Levenshtein distance.
    """
    distance = Levenshtein.distance(str1, str2)
    max_length = max(len(str1), len(str2))
    return 1 - (distance / max_length)

def calculate_similarity_jaccard(str1: str, str2: str) -> float:
    """
    Calculate Jaccard similarity between two strings based on token overlap.
    """
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0

# Load a pre-trained transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def calculate_similarity_semantic(str1: str, str2: str) -> float:
    """
    Calculate semantic similarity using Sentence Transformers.
    """
    embeddings = model.encode([str1, str2])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
    return similarity[0][0]

def calculate_similarity_combined(name1, name2, desc1, desc2):
    name_similarity = calculate_similarity_levenshtein(name1, name2)
    desc_similarity = calculate_similarity_semantic(desc1, desc2)
    return name_similarity * 0.6 + desc_similarity * 0.4

def calculate_similarity(str1: str, str2: str) -> float:
    """
    Calculate similarity score between two strings using SequenceMatcher. PRIMITIVE!
    """
    return difflib.SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def match_columns(source_columns: List[Column], destination_columns: List[Column]) -> Dict[str, str]:
    """
    Match source columns to destination columns based on similarity of names and descriptions.
    """
    mapping = {}
    used_destinations = set()

    for src_col in source_columns:
        best_match = None
        best_score = 0

        for dest_col in destination_columns:
            # Skip already matched destination columns
            if str(dest_col) in used_destinations:
                continue

            # Calculate similarity scores

            total_score = calculate_similarity_combined(src_col.column_name, dest_col.column_name, src_col.column_desc, dest_col.column_desc)
            # name_similarity = calculate_similarity(src_col.column_name, dest_col.column_name)
            # desc_similarity = calculate_similarity(src_col.column_desc, dest_col.column_desc)

            # # Weighted similarity score (name: 0.6, description: 0.4)
            # total_score = name_similarity * 0.6 + desc_similarity * 0.4

            if total_score > best_score:
                best_score = total_score
                best_match = dest_col

        # Record the best match if above a threshold
        if best_match and best_score > 0.5:  # Adjust threshold as necessary
            mapping[str(src_col)] = str(best_match)
            used_destinations.add(str(best_match))
        else:
            mapping[str(src_col)] = "NA.NA"  # No match found

    return mapping



# Example match_columns function (assumed to exist and implemented elsewhere
class TestSchemaMatching(unittest.TestCase):
    def setUp(self):
        # Define source columns
        self.source_columns = [
            Column("ADMISSIONS", "The ADMISSIONS table gives information regarding a patient’s admission to the hospital.", "SUBJECT_ID", "The ADMISSIONS table can be linked to the PATIENTS table using SUBJECT_ID"),
            Column("ADMISSIONS", "The ADMISSIONS table gives information regarding a patient’s admission to the hospital.", "HADM_ID", "Each row of this table contains a unique HADM_ID"),
            Column("ADMISSIONS", "The ADMISSIONS table gives information regarding a patient’s admission to the hospital.", "ADMITTIME", "Provides the date and time the patient was admitted to the hospital"),
            Column("ADMISSIONS", "The ADMISSIONS table gives information regarding a patient’s admission to the hospital.", "DISCHTIME", "Provides the date and time the patient was discharged from the hospital"),
            Column("ADMISSIONS", "The ADMISSIONS table gives information regarding a patient’s admission to the hospital.", "DEATHTIME", "Provides the time of in-hospital death for the patient"),
        ]

        # Define destination columns
        self.destination_columns = [
            Column("VISIT_OCCURRENCE", "Contains events where persons engage with the healthcare system.", "person_id", "Use this to identify unique interactions between a person and the healthcare system."),
            Column("VISIT_OCCURRENCE", "Contains events where persons engage with the healthcare system.", "visit_occurrence_id", "Unique identifier for each interaction"),
            Column("VISIT_OCCURRENCE", "Contains events where persons engage with the healthcare system.", "visit_start_datetime", "Start date and time of the visit"),
            Column("VISIT_OCCURRENCE", "Contains events where persons engage with the healthcare system.", "visit_end_datetime", "End date and time of the visit"),
            Column("VISIT_OCCURRENCE", "Contains events where persons engage with the healthcare system.", "visit_type_concept_id", "Indicates the type of visit, such as inpatient or outpatient"),
        ]

        # Define expected solution mapping
        self.expected_mapping = {
            "ADMISSIONS.SUBJECT_ID": "VISIT_OCCURRENCE.person_id",
            "ADMISSIONS.HADM_ID": "VISIT_OCCURRENCE.visit_occurrence_id",
            "ADMISSIONS.ADMITTIME": "VISIT_OCCURRENCE.visit_start_datetime",
            "ADMISSIONS.DISCHTIME": "VISIT_OCCURRENCE.visit_end_datetime",
            "ADMISSIONS.DEATHTIME": "NA.NA",
        }

    def test_schema_matching(self):
        # Run the matching algorithm
        result = match_columns(self.source_columns, self.destination_columns)

        # Validate the result against the expected mapping
        for src_col, tgt_col in self.expected_mapping.items():
            self.assertIn(src_col, result)
            self.assertEqual(result[src_col], tgt_col)

if __name__ == "__main__":
    unittest.main()
