def clean_data(rows):
    cleaned_rows = []

    for row in rows:
        row["municipality"] = row["municipality"].strip().title()
        row["service"] = row["service"].strip().title()
        row["area"] = row["area"].strip.title()
        row["status"] = row["status"].strip.title()

        cleaned_rows.append(row)

    return cleaned_rows