import requests
import webbrowser

def main():
    # Step 1: Send a GET request and access cookies
    url = "https://parents.msrit.edu/parentsodd/"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("GET request successful")
        cookies = response.cookies  # Accessing cookies from the response
        print("Cookies:", cookies)
        
        # Step 2: Send a POST request to url with payload and cookies
        dashboard_url = "https://parents.msrit.edu/parentsodd/index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard"
        payload = {
            'username': 'USN',
            'dd': '00',  # Day
            'mm': '00',  # Month
            'yyyy': '0000'  # Year
        }
        
        cookies_dict = {cookie.name: cookie.value for cookie in cookies}
        headers = {'Cookie': '; '.join([f"{name}={value}" for name, value in cookies_dict.items()])}
        
        post_response = requests.post(url, data=payload, headers=headers)
                
        if post_response.status_code == 200:
            print("POST request successful")
            # print("Dashboard Response:", post_response.content)
            
            # Step 3: Open the URL in the browser
            webbrowser.open_new_tab(url)
        else:
            print("POST request failed")
    else:
        print("GET request failed")

if __name__ == "__main__":
    main()
