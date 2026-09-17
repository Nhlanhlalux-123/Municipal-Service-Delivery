def clean_data(rows):
    cleaned_rows = []
    seen_ids = set()

    quality_report = {
        "total_records": len(rows),
        "duplicate_records": 0,
        "missing_fields": 0,
        "clean_records": 0,
        "rejected_records": []
    }

    for row in rows:

        if row["id"] in seen_ids:
            quality_report["duplicate_records"] += 1

            quality_report["rejected_records"].append({
                "id": row["id"],
                "reason": "Duplicate ID"
            })

            continue

        seen_ids.add(row["id"])

        municipality = row["municipality"].strip().title()
        service = row["service"].strip().title()
        area = row["area"].strip().title()
        status = row["status"].strip().title()

        missing_fields = []

        if not municipality:
            missing_fields.append("municipality")

        if not service:
            missing_fields.append("service")

        if not area:
            missing_fields.append("area")

        if missing_fields:
            quality_report["missing_fields"] += 1

            quality_report["rejected_records"].append({
                "id": row["id"],
                "reason": f"Missing: {', '.join(missing_fields)}"
            })

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

    quality_report["clean_records"] = len(cleaned_rows)

    return cleaned_rows, quality_report