import moviepy.editor as mp
from bs4 import BeautifulSoup
import urllib.request
import ssl
import requests
import os
import urllib.parse
import cairosvg
from cairosvg import svg2png

# Disable SSL verification (for testing purposes, not for production)
context = ssl._create_unverified_context()
opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=context))
urllib.request.install_opener(opener)

# Function to validate image URLs
def is_valid_image_url(url):
    parsed_url = urllib.parse.urlparse(url)
    return bool(parsed_url.scheme) and parsed_url.path.endswith((".jpg", ".jpeg", ".png", ".gif", ".svg"))

# Load the background video
video = mp.VideoFileClip("background.mp4")

# List of URLs to scrape
urls = [
    "http://www.sanchobbdo.com.co/",
    "http://www.ajover.com/",
]

# List to store clips from each URL
final_clips = []

for url in urls:
    try:
        # Make the request using requests
        response = requests.get(url)
        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # Find the first image element
            image = soup.find("img")
            if image:
                # Validate image URL
                image_url = image["src"]
                if is_valid_image_url(image_url):
                    try:

                        image_filename, image_extension = os.path.splitext(image_url)
                        if image_extension.lower() == ".svg":  # Check for SVG
                            # Convert SVG to PNG using CairoSVG
                            svg_filename = f"temp_image.svg"  # Adjust filename if needed
                            urllib.request.urlretrieve(image_url, svg_filename)

                            # Create PNG from SVG using CairoSVG
                            png_filename = f"temp_image.png"  # Adjust filename if needed
                            svg2png(url=svg_filename, write_to=png_filename)
                            # Use the PNG image for the video clip
                            image_filename = png_filename

                        image_filename, image_extension = os.path.splitext(image_url)
                        if image_extension.lower() in (".jpg", ".jpeg", ".png"):
                            image_filename = f"temp_image{image_extension}"
                            urllib.request.urlretrieve(image_url, image_filename)

                            # Create the image clip
                            image_clip = mp.ImageClip(image_filename).set_duration(5).set_pos("center")

                            # Remove the temporary file
                            os.remove(image_filename)

                            # Append the image clip to the list
                            final_clips.append(image_clip)
                        else:
                            print(f"Unsupported image format: {image_extension} for URL: {url}")
                    except Exception as e:
                        print(f"Error downloading or processing image: {e}")
                else:
                    print(f"Invalid image URL: {image_url}")
            else:
                print(f"No image found for URL: {url}")
        else:
            print(f"Error fetching URL: {url} - Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error processing URL: {url} - {e}")
# Combine all URL clips into the final video
if final_clips:
    final_video = mp.concatenate_videoclips(final_clips)
    final_video.write_videofile("video_final.mp4")
else:
    print("No valid image-text combinations found for any URLs. No video created.")
