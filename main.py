import requests
from bs4 import BeautifulSoup

def main():
    url = "https://parents.msrit.edu/parentsodd/index.php"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    with requests.Session() as session:
        session.get(url, headers=headers)

        payload = {
            "username": "USN",
            "dd": "00",
            "mm": "00",
            "yyyy": "0000",
            "passwd": "yyyy-mm-dd",
            "remember": "",
            "option": "com_user",
            "task": "login",
            "return": "",
            "ea07d18ec2752bcca07e20a852d96337": "1"
        }

        response = session.post(url, data=payload, headers=headers)

        if response.status_code == 200:
            print("Login successful")

            soup = BeautifulSoup(response.content, 'html.parser')

            rows = soup.find('tbody').find_all('tr')
            extracted_data = []

            for row in rows:
                course_code = row.find('td').text.strip()

                course_name = row.find_all('td')[1].text.strip()

                attendance_button = row.find('button', class_='cn-attendanceclr')
                attendance_value = None
                if attendance_button:
                    attendance_value = attendance_button.text.strip().split()[0] 

                extracted_data.append({
                    'course_code': course_code,
                    'course_name': course_name,
                    'attendance': attendance_value,
                })

            for data in extracted_data:
                print(data)

        else:
            print("Login failed")

if __name__ == "__main__":
    main()
