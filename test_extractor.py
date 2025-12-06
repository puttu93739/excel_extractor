import pytest
import pandas as pd
from extractor import ExcelExtractor
from collections import Counter


@pytest.fixture
def mock_dataframe(tmp_path):
    data = {
        "Additional comments": [
            "Groups : [code]<I>Team A</I>[/code]",
            "Groups : [code]<I>Team B, Team C</I>[/code]",
            "No groups here",
            "Groups : [code]<I>Team A</I>[/code]",
        ]
    }

    df = pd.DataFrame(data)
    file_path = tmp_path / "coding_challenge_test.xlsx"
    df.to_excel(file_path, index=False)
    return file_path


# Test 1: Basic extraction from a single text string
def test_extract_from_text_single():
    extractor = ExcelExtractor("Groups")
    result = extractor.extract_from_text("Groups : [code]<I>Team A</I>[/code]")
    assert result == ["Team A"]


# Test 2: Multiple groups in one line
def test_extract_from_text_multiple():
    extractor = ExcelExtractor("Groups")
    text = "Groups : [code]<I>Team A, Team B, Team C</I>[/code]"
    result = extractor.extract_from_text(text)
    assert result == ["Team A", "Team B", "Team C"]


# Test 3: Case-insensitive extraction
def test_extract_from_text_case_insensitive():
    extractor = ExcelExtractor("groups")  # lower-case tag
    text = "Groups : [code]<I>Team X</I>[/code]"
    result = extractor.extract_from_text(text)
    assert result == ["Team X"]


# Test 4: Extraction from Excel file using fixture
def test_extract_from_file_counts(mock_dataframe):
    extractor = ExcelExtractor("Groups")
    result = extractor.extract_from_file(mock_dataframe, "Additional comments")
    assert result == Counter({"Team A": 2, "Team B": 1, "Team C": 1})


# Test 5: Missing column in file should raise error
def test_missing_column_error(tmp_path):
    df = pd.DataFrame({"WrongColumn": ["abc"]})
    file_path = tmp_path / "coding_challenge_test.xlsx"
    df.to_excel(file_path, index=False)

    extractor = ExcelExtractor("Groups")

    with pytest.raises(ValueError):
        extractor.extract_from_file(file_path, "Additional comments")
