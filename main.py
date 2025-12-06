from extractor import ExcelExtractor


def save_results_to_text(counter, output_file="results.txt"):
    with open(output_file, "w") as f:
        f.write("Group Name\t| Occurrences\n")
        f.write("---------------------------------\n")

        for group, count in counter.items():
            f.write(f"{group}\t{count}\n")

    print(f"Results saved to {output_file}")

def main():
    file_path = f"coding_challenge_test.xlsx"
    column_name = "Additional comments"
    tag = "Groups"

    extractor = ExcelExtractor(tag)
    result = extractor.extract_from_file(file_path, column_name)

    save_results_to_text(result, "group_output.txt")

    print("\nGroup Name\t\tOccurrences")
    for group, count in result.items():
        print(f"{group}\t\t{count}")


if __name__ == "__main__":
    main()
