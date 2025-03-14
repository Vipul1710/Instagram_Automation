import os
import random
import requests
import json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

class ImageCreator:
    def __init__(self):
        self.search_terms = {
            'fitness': ['fitness', 'workout', 'exercise', 'gym'],
            'wisdom': ['nature', 'mountain', 'peaceful', 'meditation'],
            'happiness': ['happy', 'joy', 'sunshine', 'smile'],
            'motivation': ['success', 'achievement', 'goal', 'victory'],
            'life': ['journey', 'path', 'adventure', 'exploration']
        }

    def get_matching_image(self, category):
        """Fetch a relevant image from Unsplash based on category"""
        search_term = random.choice(self.search_terms.get(category, ['inspirational']))
        
        try:
            url = "https://api.unsplash.com/photos/random"
            params = {
                "query": search_term,
                "orientation": "landscape",
                "client_id": os.getenv('UNSPLASH_ACCESS_KEY', "Urm2K_WBtpYv2l500desi8UMDvdhjAz5t8wohl2qPvA")
            }
            
            response = requests.get(url, params=params, verify=False)
            data = json.loads(response.text)
            return data["urls"]["regular"]
        except Exception as e:
            print(f"Error fetching image: {e}")
            return None

    def create_quote_image(self, quote_data, image_url):
        """Create an image with the quote"""
        try:
            # Download and open the image
            response = requests.get(image_url, verify=False)
            image = Image.open(BytesIO(response.content))

            # Create overlay for text
            overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)

            # Calculate text box dimensions
            box_width = int(image.size[0] * 0.8)
            text_width = int(image.size[0] * 0.7)

            # Set font properties
            font_size = int(image.size[1] * 0.052)
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", font_size)
            small_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", int(font_size * 0.9))

            # Prepare quote text
            quote_text = f'"{quote_data["text"]}"'
            current_font = small_font if len(quote_text) > 100 else font

            # Split text into lines
            lines = self._split_lines(quote_text, current_font, box_width)
            text_height = sum(current_font.getbbox(line)[3] - current_font.getbbox(line)[1] for line in lines)

            # Calculate dimensions
            padding = 40
            bottom_margin = 40
            text_area_height = text_height + (padding * 2)
            text_area_top = image.size[1] - text_area_height - bottom_margin - 30
            text_position = ((image.size[0] - box_width) / 2, text_area_top + padding)

            # Draw background
            self._draw_background(overlay_draw, image.size[0], text_area_top, bottom_margin)

            # Draw text
            self._draw_text(overlay_draw, lines, current_font, text_position, box_width)

            # Composite and save
            image = Image.alpha_composite(image.convert('RGBA'), overlay)
            image = image.convert('RGB')
            output_path = "instaPhotos/quote_image.jpg"
            image.save(output_path)
            print(f"Image saved as {output_path}")
            return output_path

        except Exception as e:
            print(f"Error creating image: {e}")
            return None

    def _split_lines(self, text, font, width):
        """Split text into lines that fit within width"""
        words = text.split()
        lines = []
        current_line = words[0]
        for word in words[1:]:
            if font.getlength(current_line + ' ' + word) < width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def _draw_background(self, draw, width, top, bottom_margin):
        """Draw background with gradient and border"""
        bg_left = 0
        bg_right = width
        bg_bottom = width - bottom_margin

        # Draw border
        border_height = 3
        for i in range(border_height):
            opacity = int(255 * (1 - i/border_height))
            y = int(top) + i
            draw.rectangle(
                [(bg_left, y), (bg_right, y)],
                fill=(255, 255, 255, opacity)
            )

        # Draw gradient
        fade_height = 40
        for i in range(fade_height):
            progress = i / fade_height
            opacity = int(200 * progress)
            y = int(top) + border_height + i
            draw.rectangle(
                [(bg_left, y), (bg_right, y)],
                fill=(0, 0, 0, opacity)
            )

        # Draw main background
        draw.rectangle(
            [(bg_left, int(top) + border_height + fade_height), (bg_right, bg_bottom)],
            fill=(0, 0, 0, 180)
        )

    def _draw_text(self, draw, lines, font, position, box_width):
        """Draw text with outline effect"""
        current_position = position
        for line in lines:
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]
            x = current_position[0] + (box_width - line_width) / 2
            y = current_position[1]
            
            self._draw_text_with_outline(draw, line, (x, y), font)
            current_position = (current_position[0], current_position[1] + line_height * 1.5)

    def _draw_text_with_outline(self, draw, text, position, font):
        """Draw text with outline effect"""
        x, y = position
        outline_color = (0, 0, 0)
        text_color = (255, 255, 255)
        offset = 2

        # Draw outline
        for dx, dy in [(-offset,-offset), (offset,-offset), (-offset,offset), (offset,offset),
                      (-offset,0), (offset,0), (0,-offset), (0,offset)]:
            draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=text_color)