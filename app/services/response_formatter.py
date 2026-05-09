def format_recommendations(recommendations):

    formatted = []

    seen = set()

    for item in recommendations:

        url = item.get("url", "")

        if url in seen:
            continue

        seen.add(url)

        formatted.append({

            "name": item.get("name", ""),
            "url": url,
            "test_type": item.get("test_type", "Unknown")

        })

    return formatted[:10]