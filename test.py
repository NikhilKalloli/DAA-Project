import requests
import webbrowser

def main():
    login_url = "https://parents.msrit.edu/parentsodd/index.php"  # URL to submit the login form
    dashboard_url = "https://parents.msrit.edu/parentsodd/index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard"  # URL of the dashboard after login
    
    # Create a session
    session = requests.Session()

    # Login payload
    login_payload = {
        'username': 'myUSN',  # Your username
        'dd': '00',  # Day of birth
        'mm': '00',  # Month of birth
        'yyyy': '0000',  # Year of birth
    }

    # Send POST request to login
    response = session.post(login_url, data=login_payload)

    if response.status_code == 200:
        print("Login successful")
        # Open the dashboard URL in the browser
        webbrowser.open_new_tab(dashboard_url)
    else:
        print("Login failed")

if __name__ == "__main__":
    main()
