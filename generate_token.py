from google_auth_oauthlib.flow import InstalledAppFlow
import os

def main():
    print("Opening browser to login to Google/YouTube...")
    
    # Check for secret file
    if not os.path.exists("client_secret.json"):
        print("ERROR: client_secret.json missing!")
        return

    # Run the login flow locally
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        ["https://www.googleapis.com/auth/youtube.upload"]
    )
    
    # This opens the browser
    # We use port 8080 which is commonly allowed. 
    # If this fails with "Address already in use", you can try port=0
    try:
        creds = flow.run_local_server(port=8080, open_browser=True)
    except Exception as e:
        print(f"Server failed on 8080, trying random port... Error: {e}")
        creds = flow.run_local_server(port=0, open_browser=True)
    
    print("\n\n=== AUTHENTICATION SUCCESSFUL! ===")
    print("="*50)
    print("COPY THE TEXT BELOW AND PASTE INTO STREAMLIT SECRETS:")
    print("="*50)
    print("\n[google_token]")
    print(f"token_json = '{creds.to_json()}'")
    print("\n" + "="*50)
    print("Go to Streamlit -> Manage App -> Secrets -> Paste the above.")

if __name__ == "__main__":
    main()
