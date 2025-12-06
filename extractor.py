import pandas as pd
import re
from collections import Counter


class ExcelExtractor:
    """
    This class can work with ANY tag (e.g., Groups, Teams, Divisions).
    """

    def __init__(self, tag: str):
        """
        Initialize with a dynamic tag name.
        Example: "Groups"
        """
        self.tag = tag
        self.pattern = rf"{tag}\s*:\s*\[code\]<I>(.*?)</I>"

    def extract_from_text(self, text: str):
        """
        Extract groups from a single cell text.
        Returns a list of group names.
        """
        groups = []
        matches = re.findall(self.pattern, text, flags=re.IGNORECASE)

        for match in matches:
            # Split in case of multiple groups in one line
            for g in match.split(","):
                g = g.strip()
                if g:
                    groups.append(g)

        return groups

    def extract_from_file(self, file_path: str, column_name: str):
        """
        Process the entire Excel file and count occurrences of groups.
        Returns a Counter object.
        """
        df = pd.read_excel(file_path)

        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in the file")

        all_groups = []

        for text in df[column_name].dropna().astype(str):
            all_groups.extend(self.extract_from_text(text))

        return Counter(all_groups)
