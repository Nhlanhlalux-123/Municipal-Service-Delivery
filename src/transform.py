def clean_data(rows):
    cleaned_rows = []
    seen_ids = set()

    for row in rows:
        if row["id"] in seen_ids:
            continue

        seen_ids.add(row["id"])

        municipality = row["municipality"].strip().title()
        service = row["service"].strip().title()
        area = row["area"].strip().title()
        status = row["status"].strip().title()

        if not municipality:
            continue

        if not service:
            continue

        if not area:
            continue

        cleaned_row = {
            "id": row["id"],
            "date": row["date"],
            "municipality": municipality,
            "service": service,
            "area": area,
            "status": status
        }

        cleaned_rows.append(cleaned_row)

    return cleaned_rows