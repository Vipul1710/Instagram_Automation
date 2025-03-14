# Instagram Quote Poster

Automatically generates and posts inspirational quotes with beautiful background images to Instagram.

## Features

- Fetches quotes from Zen Quotes API with local fallback
- Creates beautiful quote images with:
  - Random background images from Unsplash
  - Clean text layout with outline effect
  - Gradient overlay for better readability
- Automatic Instagram posting
- Runs twice daily via GitHub Actions

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Instagram_Automation.git
cd Instagram_Automation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your credentials:
```env
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
UNSPLASH_ACCESS_KEY=your_unsplash_api_key
```

4. For GitHub Actions automation, add these secrets to your repository:
- `INSTAGRAM_USERNAME`
- `INSTAGRAM_PASSWORD`
- `UNSPLASH_ACCESS_KEY`

## Usage

Run manually:
```bash
python main.py
```

The script will:
1. Generate a quote image
2. Post it to Instagram
3. Add relevant hashtags

## Project Structure

- `main.py` - Main execution script
- `quote_generator.py` - Handles quote fetching and management
- `image_creator.py` - Creates quote images
- `instagram_uploader.py` - Handles Instagram uploads
- `.github/workflows/post_quote.yml` - GitHub Actions workflow

## Automation

The script runs automatically at:
- 9:00 AM IST
- 9:00 PM IST

You can also trigger it manually from the GitHub Actions tab.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request