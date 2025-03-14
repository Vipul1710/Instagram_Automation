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
            # Try to load existing session
            session_file = "instagram_session.json"
            if os.path.exists(session_file):
                try:
                    cl.load_settings(session_file)
                    print("Loaded existing session")
                    cl.login(username=self.username, password=self.password)
                except Exception as e:
                    print(f"Failed to load session: {e}")
                    cl.login(username=self.username, password=self.password)
            else:
                cl.login(username=self.username, password=self.password)
            
            # Save session for future use
            cl.dump_settings(session_file)
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