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
            "username": "myUSN",
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
            print(soup.prettify())

        else:
            print("Login failed")

if __name__ == "__main__":
    main()
