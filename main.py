from extractor import ExcelExtractor


def main():
    file_path = f"coding_challenge_test.xlsx"
    column_name = "Additional comments"
    tag = "Groups"

    extractor = ExcelExtractor(tag)
    result = extractor.extract_from_file(file_path, column_name)

    print("\nGroup Name\t\tOccurrences")
    for group, count in result.items():
        print(f"{group}\t\t{count}")


if __name__ == "__main__":
    main()
