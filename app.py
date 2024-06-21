''' Web Scraping Python Script with Flask Integration
===========================================================
Scrapes NBA champions data from Wikipedia and serves it in a web app.
===========================================================
'''
from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Function to scrape NBA champions data from Wikipedia
def scrape_nba_champions():
    url = 'https://en.wikipedia.org/wiki/List_of_NBA_champions'

    try:
        # Fetch the web page
        page = requests.get(url)
        page.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(page.content, 'html.parser')

        # Find the correct table containing NBA champions data
        table = soup.find('table', class_='wikitable sortable')

        # Initialize an empty list to store data
        data = []

        # Extract table rows (skip the header row)
        rows = table.find_all('tr')[1:]

        # Iterate through each row and extract data
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 7:  # Ensure all columns are present
                team_name = columns[0].text.strip()
                total_championships = columns[1].text.strip()
                total_app_losses = columns[2].text.strip()
                total_appearances = columns[3].text.strip()
                finals_win_percentage = columns[4].text.strip()
                years_won = columns[5].text.strip()
                years_lost = columns[6].text.strip()

                # Append data as a dictionary to the list
                data.append({'Team Name': team_name,
                             'Championships': total_championships,
                             'Lost': total_app_losses,
                             'Appearances': total_appearances,
                             'Win %': finals_win_percentage,
                             'Years Won': years_won,
                             'Years Lost': years_lost})

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(data)

        return df.to_dict(orient='records')  # Return data as list of dictionaries

    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return []

    except AttributeError as e:
        print(f"Error parsing HTML: {e}")
        return []

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

# Route for home page
@app.route('/')
def index():
    # Scrape NBA champions data
    data = scrape_nba_champions()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
