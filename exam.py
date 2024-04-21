import requests
from bs4 import BeautifulSoup
import csv
import os

url = "https://exam.msrit.edu/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

# Define the CSV file path
csv_file = 'exam_results.csv'

# Check if the CSV file already exists
if os.path.exists(csv_file):
    # If the file exists, truncate it to clear its contents
    with open(csv_file, 'w', newline='') as csvfile:
        csvfile.truncate()
        print(f"Cleared existing data in {csv_file}")

# Open a CSV file to save the data
with open(csv_file, 'w', newline='') as csvfile:
    fieldnames = ['USN', 'Name', 'SGPA', 'Semester']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(1, 169):  
        usn = f"1MS22CS{i:03}" 
        payload = {
            "usn": usn,
            "osolCatchaTxt": "",
            "osolCatchaTxtInst": "0",
            "option": "com_examresult",
            "task": "getResult"
        }

        with requests.Session() as session:
            session.get(url, headers=headers)
            response = session.post(url, data=payload, headers=headers)
            if response.status_code == 200:
                print(f"Fetching results for USN: {usn}")
                soup = BeautifulSoup(response.content, 'html.parser')
                name = soup.find('h3').text.strip()
                sgpa = soup.find_all('p')[3].text.strip()
                semester = soup.find('p').text.split(',')[-1].strip()
                # Write the extracted data to the CSV file
                writer.writerow({'USN': usn, 'Name': name, 'SGPA': sgpa, 'Semester': semester})
            else:
                print(f"Failed to fetch results for USN: {usn}")

print("Data extraction complete. Results saved to exam_results.csv")
