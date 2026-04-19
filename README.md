<img width="2816" height="1536" alt="amazon_scraper" src="https://github.com/user-attachments/assets/abce5a95-a62d-4cec-8186-eca697a4b530" />

Step-by-Step Installation and Usage Guide

Overview:
This guide outlines the deployment of the Amazon Price-Drop Scraper. It is optimized for standard local development environments as well as headless Linux server environments (such as Ubuntu 22.04), which are highly recommended for running automated tracking pipelines and managing persistent cron jobs.

Phase 1: Environment Setup
Step 1: Verify System Prerequisites
Ensure that Python 3 is installed on your system.

Linux (Ubuntu/Debian): Run python3 --version in your terminal.

Windows/macOS: Run python --version.
If Python is not installed, download it from python.org or install it via your server's package manager (sudo apt install python3 python3-pip).

Step 2: Create a Virtual Environment (Recommended)
To avoid dependency conflicts with other automation scripts or trackers on your machine, isolate this project using venv.

Open your terminal or command prompt.

Navigate to your desired project directory: cd /path/to/your/project

Create the environment:

python3 -m venv scraper_env

Activate the environment:

Linux/macOS: source scraper_env/bin/activate

Windows: scraper_env\Scripts\activate

Step 3: Install Required Libraries
With your virtual environment activated, install the external dependencies required by the script: requests for handling HTTP calls and beautifulsoup4 for parsing the DOM structure.
Run the following command:

Bash
pip install requests beautifulsoup4
Phase 2: Configuration and Execution
Step 1: Save the Script
Create a new Python file named amazon_scraper.py and paste the provided code into it. You can do this using an IDE (like VS Code or PyCharm) or a command-line editor (like nano amazon_scraper.py on your server).

Step 2: Customize the Search Parameters
Open amazon_scraper.py and scroll to the bottom of the file where the if __name__ == "__main__": block is located.

Change the search_term variable to the specific product category you are targeting (e.g., "monitors", "wireless earbuds").

Adjust the pages parameter in the scrape_amazon_discounts function to control how deep the script searches. Note: Keep this number low (1-3) initially to test functionality without triggering rate limits.

Modify the filename parameter in the save_to_csv function if you want to name your output file differently (e.g., 'prime_refund_targets.csv').

Step 3: Run the Script
Execute the script from your terminal:

Bash
python3 amazon_scraper.py
You will see console outputs indicating the pages being scraped and the randomized sleep intervals between requests.

Phase 3: Reviewing the Data and Troubleshooting
Reviewing the Output:
Once the script finishes execution, check your project directory for the newly generated .csv file. You can open this file in Excel, Google Sheets, or parse it dynamically for further automation. The file will contain four columns:

Title: The product name.

Current_Price: The discounted price.

Original_Price: The previous price.

Link: The direct URL to the product page.

Troubleshooting Common Errors:

Error 503 / "No discounted data to save" immediately: Amazon has detected the script as a bot. The requests library does not render JavaScript and is easily identifiable.

Solution: If you intend to scale this logic into a production-level tracker, you will need to upgrade the pipeline to use rotating residential proxies (via the proxies parameter in the requests library) or migrate the request engine to a headless browser automation tool like Playwright or Selenium.

Empty fields in CSV: Amazon frequently conducts A/B testing on their DOM structure. The CSS classes used in the script (a-price, a-text-price) might change.

Solution: Inspect the Amazon search page source code in your browser and update the class_ targets within the BeautifulSoup parsing logic in the script.

🛡️ License 

This project is licensed under the MIT License. For more information, see the [LICENSE](LICENSE) file.
