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

        # Column headers
        sheet.append(["Contact Information", "Services Offered", "Social Media Links", "All Links on Page", "Page Headings"])

        # Collecting information
        contact_info = [info.strip() for info in soup.find_all(string=lambda text: 'contact' in text.lower())]
        service_info = [info.strip() for info in soup.find_all(string=lambda text: 'service' in text.lower())]

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

        social_links_list = [f"{platform}: {link if link else 'Not found'}" for platform, link in social_links.items()]
        
        # Extracting headings
        tags = ['h1', 'h2', 'h3', 'h4', 'h5']
        headings = [f"{tag.upper()}: {heading.get_text().strip()}" for tag in tags for heading in soup.find_all(tag)]

        # Determine the maximum number of rows needed
        max_rows = max(len(contact_info), len(service_info), len(social_links_list), len(all_links), len(headings))

        # Populate the Excel sheet row by row
        for i in range(max_rows):
            row = [
                contact_info[i] if i < len(contact_info) else "",
                service_info[i] if i < len(service_info) else "",
                social_links_list[i] if i < len(social_links_list) else "",
                all_links[i] if i < len(all_links) else "",
                headings[i] if i < len(headings) else ""
            ]
            sheet.append(row)

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
