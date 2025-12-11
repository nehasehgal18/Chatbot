def open_site(site_name):
    site_name = site_name.lower().strip()

    common_sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "twitter": "https://www.twitter.com",
        "amazon": "https://www.amazon.in",
        "flipkart": "https://www.flipkart.com"
    }

    if site_name in common_sites:
        return common_sites[site_name]

    site_name = site_name.replace("site", "").replace("website", "").strip()

    return f"https://www.{site_name}.com"
