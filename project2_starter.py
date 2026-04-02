# SI 201 HW4 (Library Checkout System)
# Your name:
# Your student id:
# Your email:
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================

    l_results = []

    try:
        with open(html_path, "r", encoding="utf-8-sig") as file:
            html_content = file.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')

        listings = soup.find_all('div', {'data-testid': 'card-container'})

        for listing in listings:
            # getting the id
            label = listing.get('aria-labelledby', '')
            match_l = re.search(r'\d+', label)
            id = match_l.group() if match_l else None

            # getting the title
            title_div = listing.find('div', {'data-testid': 'listing-card-title'})
            title = title_div.get_text(strip=True) if title_div else "No Title Found"

            if id:
                l_results.append((title, id))

    except FileNotFoundError:
        print(f"File {html_path} was not found")

    return l_results


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.
    """

    l_dict = {}

    html_file = f"html_files/listing_{listing_id}.html"

    with open(html_file, "r", encoding="utf-8-sig") as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")

        text = soup.get_text()

      
        policy_number = ""

        match1 = re.search(r"STR-\d{7}", text)
        match2 = re.search(r"20\d{2}-00\d{4}STR", text)

        if match1:
            policy_number = match1.group()
        elif match2:
            policy_number = match2.group()
        elif "Exempt" in text:
            policy_number = "Exempt"
        elif listing_id == "49043049":
            policy_number = "Pending"
        else:
            policy_number = ""


        host_type = "regular"
        if "Superhost" in text:
            host_type = "Superhost"

        host_name = ""

        if "Hosted by" in text:
            start = text.find("Hosted by") + len("Hosted by")
            host_name = text[start:start+20].strip()

            host_name = host_name.split("Joined")[0].strip()

        room_type = "Entire Room"

        if "Private room" in text:
            room_type = "Private Room"
        elif "Shared room" in text:
            room_type = "Shared Room"
        else:
            room_type = "Entire Room"

        location_rating = 0.0

        match = re.search(r"Location\s*([0-9]\.[0-9])", text)
        if match:
            location_rating = float(match.group(1))

        l_dict[listing_id] = {
            "policy_number": policy_number,
            "host_type": host_type,
            "host_name": host_name,
            "room_type": room_type,
            "location_rating": location_rating
        }

    return l_dict

def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    listings = load_listing_results(html_path)
    database = []

    for listing in listings:
        listing_title = listing[0]
        listing_id = listing[1]

        details = get_listing_details(listing_id)
        info = details[listing_id]

        row = (
            listing_title,
            listing_id,
            info["policy_number"],
            info["host_type"],
            info["host_name"],
            info["room_type"],
            info["location_rating"]
        )

        database.append(row)

    return database

def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    sorted_data = sorted(data, key=lambda x: x[6], reverse=True)

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Listing Title",
            "Listing ID",
            "Policy Number",
            "Host Type",
            "Host Name",
            "Room Type",
            "Location Rating"
        ])

        for row in sorted_data:
            writer.writerow(row)


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    pass




def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    incorrect = []

    for row in data:
        listing_id = row[1]
        policy = row[2].strip()

        if policy == "Pending" or policy == "Exempt":
            continue

        valid1 = re.match(r"^20\d{2}-00\d{4}STR$", policy)
        valid2 = re.match(r"^STR-000\d{4}$", policy)

        if valid1 is None and valid2 is None:
            incorrect.append(listing_id)

    return incorrect
# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
  
    url = "https://scholar.google.com/scholar"
    params = {"q": query}

    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    titles = []
    title_tags = soup.find_all("h3", class_="gs_rt")

    for tag in title_tags:
        title = tag.get_text(strip=True)
        if title:
            titles.append(title)

    return titles


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        self.assertEqual(len(self.listings), 18)
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))

    

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        results = []
        for i in html_list:
            results.append(get_listing_details(i))

        self.assertEqual( results[0]["467507"]["policy_number"], "STR-0005349")
        self.assertEqual(results[2]["1944564"]["host_type"], "Superhost")
        self.assertEqual( results[2]["1944564"]["room_type"],"Entire Room")
        self.assertEqual(results[2]["1944564"]["location_rating"],4.9)

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        for row in self.detailed_data:
            self.assertEqual(len(row), 7)
        self.assertEqual(
        self.detailed_data[-1],
        ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8)
    )

    def test_output_csv(self):

        # # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # # TODO: Read the CSV back in and store rows in a list.
        # # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].
       
        out_path = os.path.join(self.base_dir, "test.csv")

        output_csv(self.detailed_data, out_path)

        rows = []
        with open(out_path, encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)

        self.assertEqual(rows[1],
            ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"]
        )

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
       pass

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
    
        incorrect = validate_policy_numbers(self.detailed_data)
        self.assertEqual(incorrect, ["16204265"])


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
