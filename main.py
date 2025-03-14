import os
import random
from dotenv import load_dotenv
from quote_generator import QuoteGenerator
from image_creator import ImageCreator
from instagram_uploader import InstagramUploader

def main():
    # Load environment variables
    load_dotenv()
    
    # Ensure output directory exists
    os.makedirs("instaPhotos", exist_ok=True)
    
    # Initialize components
    quote_gen = QuoteGenerator()
    img_creator = ImageCreator()
    insta_uploader = InstagramUploader()
    
    # Generate image with quote
    categories = ['motivation', 'wisdom', 'happiness', 'life']
    category = random.choice(categories)
    
    # Get quote and generate image
    quote_data = quote_gen.fetch_quote(category)
    if quote_data:
        image_url = img_creator.get_matching_image(category)
        if image_url:
            output_path = img_creator.create_quote_image(quote_data, image_url)
            if output_path:
                print("Quote image generated successfully!")
                # Upload to Instagram
                if insta_uploader.upload_image(output_path, quote_data):
                    print("Process completed successfully!")
                else:
                    print("Failed to upload to Instagram")
            else:
                print("Failed to create quote image")
        else:
            print("Failed to fetch matching image")
    else:
        print("Failed to fetch quote")

if __name__ == "__main__":
    main()