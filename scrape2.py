import webbrowser
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

def scrape_hospital_info(url, output_file):
    try:
        # Send a GET request to the hospital website
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Create a new Excel workbook and set up the sheet
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Hospital Info"

        # Add contact information
        contact_info = soup.find_all(string=lambda text: 'contact' in text.lower())
        sheet.append(["Contact Information"])
        for info in contact_info:
            sheet.append([info.strip()])

        # Add a blank row for spacing
        sheet.append([""])
        
        # Add service information
        service_info = soup.find_all(string=lambda text: 'service' in text.lower())
        sheet.append(["Services Offered"])
        for info in service_info:
            sheet.append([info.strip()])

        # Add a blank row for spacing
        sheet.append([""])
        
        # Add social media links
        social_links = {
            "Instagram": None,
            "Facebook": None,
            "Gmail": None,
            "YouTube": None
        }
        all_links = []

        for link in soup.find_all('a', href=True):
            href = link['href']
            all_links.append(href)
            if 'instagram.com' in href:
                social_links["Instagram"] = href
            elif 'facebook.com' in href:
                social_links["Facebook"] = href
            elif 'gmail.com' in href:
                social_links["Gmail"] = href
            elif 'youtube.com' in href:
                social_links["YouTube"] = href

        # Write social media links to Excel
        sheet.append(["Social Media Links"])
        for platform, link in social_links.items():
            sheet.append([platform, link if link else 'Not found'])

        # Add a blank row for spacing
        sheet.append([""])
        
        # Write all page links to Excel
        sheet.append(["All Links on the Page"])
        for link in all_links:
            sheet.append([link])

        # Add a blank row for spacing
        sheet.append([""])
        
        # Extract and write headings to Excel
        sheet.append(["Page Headings"])
        tags = ['h1', 'h2', 'h3', 'h4', 'h5']
        for tag in tags:
            for heading in soup.find_all(tag):
                sheet.append([tag.upper(), heading.get_text().strip()])

        # Save the workbook
        workbook.save(output_file)
        print(f"Data has been saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

search_query = "Hubli dharwad hospital website"
url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
webbrowser.open(url)

output_file = 'hospital_info.xlsx' 
hospital_url = input("Enter the hospital website to scrape: ")
scrape_hospital_info(hospital_url, output_file)
