def open_site(site_name):
    site_name = site_name.lower().strip()

    # Common known websites
    common_sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "twitter": "https://www.twitter.com",
        "amazon": "https://www.amazon.in",
        "flipkart": "https://www.flipkart.com"
    }

    # If it matches a known site
    if site_name in common_sites:
        return common_sites[site_name]

    # If user says "open instagram site" → clean extra words
    site_name = site_name.replace("site", "").replace("website", "").strip()

    # Default: construct the URL automatically
    return f"https://www.{site_name}.com"
