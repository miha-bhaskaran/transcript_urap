import csv
from rapidfuzz import fuzz


def find_missing_courses(
    file_a_path,
    file_b_path,
    output_missing_path,
    output_matched_path,
    course_threshold=90,
    grade_threshold=95,
):
    # File A (raw data)
    with open(file_a_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        file_a_rows = list(reader)

    # File B (truth)
    with open(file_b_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        truth_rows = [row for row in reader if row and len(row) >= 1]

    missing = []
    matched = []
    total = len(truth_rows)

    for truth_row in truth_rows:
        course_b = truth_row[0].strip().upper().replace("  ", " ")
        grade_b = (
            truth_row[1].strip().upper().replace(" ", "") if len(truth_row) > 1 else ""
        )

        match_found = False

        for row in file_a_rows:

            tokens = [
                cell.strip().upper().replace(" ", "") for cell in row if cell.strip()
            ]
            candidates = []

            #  2–4 token combinations for course matching
            for i in range(len(tokens)):
                for j in range(i + 1, min(i + 4, len(tokens))):  # 2–4 tokens
                    course_candidate = " ".join(tokens[i : j + 1])
                    candidates.append(course_candidate)

            for candidate in candidates:
                course_sim = fuzz.ratio(
                    course_b.replace(" ", ""), candidate.replace(" ", "")
                )
                if course_sim >= course_threshold:
                    for cell in row:
                        grade_candidate = cell.strip().upper().replace(" ", "")
                        grade_sim = fuzz.ratio(grade_b, grade_candidate)
                        if grade_sim >= grade_threshold:
                            match_found = True
                            matched.append(truth_row)
                            break
                if match_found:
                    break
            if match_found:
                break

        if not match_found:
            missing.append(truth_row)

    with open(output_missing_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Course", "Grade"])
        writer.writerows(missing)
    with open(output_matched_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Course", "Grade"])
        writer.writerows(matched)

    matched = total - len(missing)
    match_percent = (matched / total) * 100 if total > 0 else 0

    print(f"Total courses in truth set: {total}")
    print(f"Matched: {matched}")
    print(f"Missing: {len(missing)}")
    print(f"Match %: {match_percent:.2f}%")
    print(f"Missing courses written to: {output_missing_path}")
