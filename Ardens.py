
# Your name: Arden Stirling
# Your student id: 8531 6564
# Your email: starden@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): Adila
# If you worked with generative AI also add a statement for how you used it.
# e.g.: Google Gemini, Chat GPT
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

# The html file I'd like to use: listing_6107359.html
# File path: /Users/ardenstirling/Desktop/Data Prog/project2-w26-got_it_2/html_files/listing_6107359.html

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, 
add the following argument to any of your open() functions:
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
        base_dir = os.path.abspath(os.path.dirname(__file__))
        search_results_path = os.path.join(base_dir, "html_files", "search_results.html")

        with open(search_results_path, "r", encoding="utf-8-sig") as file:
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

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================

    l_dict = {}

    # use the os path way instead
    base_dir = os.path.abspath(os.path.dirname(__file__))
    list_details_path = os.path.join(base_dir, "html_files", f"listing_{listing_id}.html")

    with open(list_details_path, "r", encoding="utf-8-sig") as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")

        text = soup.get_text()

        policy_label = soup.find(string=lambda t: "Policy number" in t)
        policy_num = policy_label.find_next('span').get_text()
        policy_number = ""

        if "pending" in policy_num.lower():
            policy_number = "Pending"
        elif "exempt" in policy_num.lower():
            policy_number = "Exempt"
        else:
            policy_number = policy_num


        host_type = "regular"
        host_text = soup.find('span', class_='_1mhorg9').get_text()
        if "superhost" in host_text.lower():
            host_type = "Superhost"


        host_name = ""

        if "Hosted by" in text:
            start = text.find("Hosted by") + len("Hosted by")
            host_name = text[start:start+30].strip()

            host_name = host_name.split("Joined")[0].strip()

        # <span class="_12si43g" aria-hidden="true">4.89</span>

        container = soup.find('div', class_='_tqmy57')
        if container:
            text = container.get_text(strip=True).lower()
            
            if "private room" in text:
                room_type = "Private Room"
            elif "shared room" in text:
                room_type = "Shared Room"
            else:
                room_type = "Entire Room"

        location_rating = 0.0
        loc = soup.find('span', class_='_12si43g')
        if loc:
            t_loc = loc.get_text()
            match = re.search(r"(\d+\.?\d+?)", t_loc)
            # clean_l = match.get_text().strip().replace(' ', '')
            location_rating = float(match.group(1))

        #match = re.search(r"Location\s*([0-9]\.[0-9])", loc)
        #if match:
        #    location_rating = float(match.group(0))

        l_dict[listing_id] = {
            "policy_number": policy_number,
            "host_type": host_type,
            "host_name": host_name,
            "room_type": room_type,
            "location_rating": location_rating
        }

    return l_dict

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


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
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


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
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    
    avg_rating = {}
    final_averages = {}

    for d_tuple in data:
        listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating = d_tuple

        if location_rating == 0.0:
            continue
        
        if room_type not in avg_rating:
            avg_rating[room_type] = {'total_score': location_rating, 'count': 1}
        else:
            avg_rating[room_type]['total_score'] += location_rating
            avg_rating[room_type]['count'] += 1

    for room, stats in avg_rating.items():
        average = stats['total_score'] / stats['count']
        final_averages[room] = round(average, 1)

    return final_averages


    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        self.assertEqual(len(self.listings), 18, msg="Fail")
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"), msg="Fail")

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.

        results = []

        for item in html_list:
            results.append(get_listing_details(item))

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        
        self.assertEqual(results[0]["467507"]["policy_number"], "STR-0005349", msg="Fail")
        self.assertEqual(results[2]["1944564"]["host_type"], "Superhost", msg="Fail")
        self.assertEqual(results[2]["1944564"]["room_type"], "Entire Room", msg="Fail")
        self.assertEqual(results[2]["1944564"]["location_rating"], 4.9, msg="Fail")

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        pass

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        pass

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        pass


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)

# EXTRA GET_LISTING_DETAILS FUNCTION BITS:
    # l_dict = {}
    # file_path = f"listing_{listing_id}.html"

    # try:
    #     with open(file_path, "r", encoding="utf-8-sig") as file:
    #         html_content = file.read()
        
    #     soup = BeautifulSoup(html_content, 'html.parser')

    #     # example html line:
    #     # "Policy number: " "== $0 <span class="ll4r2nl dir dir-ltr">STR-0001085</span>
    #     policy_num = soup.find('span', class_='ll4r2nl').get_text()
    #     policy_number = ""
    #     if "pending" in policy_num:
    #         policy_number = "Pending"
    #     elif "exempt" in policy_num:
    #         policy_number = "Exempt"
    #     else:
    #         policy_number = policy_num

    #     # example html line:
    #     # <span aria-hidden="false" class"_1mhorg9">Superhost</span> == $0
    #     host_check = soup.find('span', class_='_1mhorg9').get_text()
    #     host_type = ""

    #     if host_check:
    #         host_check.strip()
    #         if host_check == "Superhost":
    #             host_type = "Superhost"
    #         else:
    #             host_type = "Regular"
                
    #     # example html line:
    #     # <h2 tabindex="-1" class="hnwb2pd dir dir-ltr" elementtiming="LCP-target">Hosted by Michelle</h2> == $0
    #     host_name = soup.find('h2', class_='hnwb2pb').get_text()

    #     # example html line:
    #     # <div class="_kh3xmo">Private room in home</div> == $0
    #     room_check = soup.find('span', class_='_kh3xmo').get_text()
    #     room_type = ""

    #     if room_check:
    #         room_check.strip()
    #         if "Private" in room_check:
    #             room_type = "Private Room"
    #         elif "Shared" in room_check:
    #             room_type = "Shared Room"
    #         else:
    #             room_type = "Entire Room"

    #     button = soup.find('button', attrs={'aria-label': re.compile(r'Rated')})
    #     if button:
    #         full_label = button['aria-label']
    #         location_rating = re.search(r'(\d+\d+)', full_label).group(1)

    # except FileNotFoundError:
    #     print(f"Error: The file {file_path} was not found.")

    # return l_dict