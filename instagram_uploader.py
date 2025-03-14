import os
from instagrapi import Client

class InstagramUploader:
    def __init__(self):
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')

    def upload_image(self, image_path, quote_data):
        """Upload image to Instagram"""
        if not self.username or not self.password:
            print("\nError: Instagram credentials not found!")
            print("Please set these environment variables in the .env file:")
            print("INSTAGRAM_USERNAME='your_username'")
            print("INSTAGRAM_PASSWORD='your_password'")
            return False

        print("\nAttempting to login to Instagram...")
        cl = Client()
        
        try:
            session_file = "instagram_session.json"
            
            # First time setup
            if not os.path.exists(session_file):
                print("\nPerforming first-time Instagram setup...")
                print("You will need to complete 2FA verification.")
                print("This only needs to be done once to create a valid session.\n")
                
                # Initial login will trigger 2FA
                cl.login(username=self.username, password=self.password)
                
                # Save the authenticated session
                cl.dump_settings(session_file)
                print("\nSession file created successfully!")
                print(f"The session file has been saved to: {session_file}")
                print("\nFor GitHub Actions automation:")
                print("1. Copy the entire content of instagram_session.json")
                print("2. Add it as a repository secret named INSTAGRAM_SESSION")
                
            else:
                try:
                    # Use existing session
                    cl.load_settings(session_file)
                    print("Loaded existing session")
                    cl.relogin()
                except Exception as e:
                    print(f"\nError: Failed to use existing session: {e}")
                    print("Please delete instagram_session.json and run the script again")
                    return False
            
            print("Login successful!")

            # Prepare caption
            caption = f'"{quote_data["text"]}"\n\n#inspiration #{quote_data["category"]} #quotes'

            # Upload the image
            media = cl.photo_upload(path=image_path, caption=caption)
            print("Image uploaded successfully!")
            return True

        except Exception as e:
            print(f"\nError uploading to Instagram: {e}")
            print("\nTroubleshooting tips:")
            print("1. Check your Instagram credentials")
            print("2. Make sure you're not rate limited")
            print("3. Try logging in via browser first")
            return False
