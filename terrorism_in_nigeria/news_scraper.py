from seleniumbase import Driver


def scrape_boko_haram_news(start_year=2012, end_year=2024):
    driver = Driver(uc=True)  # Start an undetectable browser session
    try:
        for year in range(start_year, end_year + 1):
            search_query = f"Boko Haram site:punchng.com after:{year - 1}-12-31 before:{year}-12-31"
            driver.open("https://www.google.com/")
            driver.type("input[name='q']", search_query + "\n")
            driver.wait_for_element("h3")  # Wait for search results

            results = driver.find_elements("h3")  # Extract search result titles
            print(f"\nResults for {year}:")
            for result in results:
                print(result.text)

    finally:
        driver.quit()  # Close the browser session


# Run the function
scrape_boko_haram_news()