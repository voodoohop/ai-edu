import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import os

def generate_image(prompt, width=512, height=512, model="stable-diffusion"):
    """
    Generate an image using the Pollinations.AI API
    
    Parameters:
        prompt (str): Text prompt describing the image to generate
        width (int): Image width
        height (int): Image height
        model (str): Model to use, options include "stable-diffusion" and "sdxl"
        
    Returns:
        PIL.Image: Generated image object
    """
    # Pollinations.AI API endpoint
    url = "https://pollinations.ai/api/generate/image"
    
    # Request parameters
    params = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "model": model
    }
    
    print(f"Generating image with prompt: '{prompt}'")
    
    # Send request
    response = requests.post(url, json=params)
    
    # Check response status
    if response.status_code == 200:
        # Get image URL from response
        image_url = response.json().get("imageUrl")
        print(f"Image generated successfully, URL: {image_url}")
        
        # Download image
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        
        return image, image_url
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None, None

def save_image(image, filename="generated_image.png"):
    """
    Save the generated image
    
    Parameters:
        image (PIL.Image): Image to save
        filename (str): Filename
    """
    if image:
        image.save(filename)
        print(f"Image saved as: {filename}")
    else:
        print("No image to save")

def display_image(image, prompt=""):
    """
    Display the generated image
    
    Parameters:
        image (PIL.Image): Image to display
        prompt (str): Prompt used to generate the image
    """
    if image:
        plt.figure(figsize=(10, 10))
        plt.imshow(image)
        plt.axis('off')
        if prompt:
            plt.title(prompt)
        plt.show()
    else:
        print("No image to display")

def main():
    """
    Main function demonstrating how to use Pollinations.AI to generate images
    """
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Example 1: Basic image generation
    prompt1 = "A robot in traditional Chinese landscape painting style"
    image1, _ = generate_image(prompt1)
    if image1:
        display_image(image1, prompt1)
        save_image(image1, "output/chinese_landscape_robot.png")
    
    # Example 2: Using the SDXL model
    prompt2 = "Future city skyline, cyberpunk style, night, neon lights"
    image2, _ = generate_image(prompt2, width=768, height=512, model="sdxl")
    if image2:
        display_image(image2, prompt2)
        save_image(image2, "output/cyberpunk_city.png")
    
    # Example 3: Experimenting with different styles
    styles = ["oil painting style", "watercolor style", "sketch style", "pixel art style"]
    base_prompt = "A cat sitting on a windowsill"
    
    for i, style in enumerate(styles):
        prompt = f"{base_prompt}, {style}"
        image, _ = generate_image(prompt)
        if image:
            display_image(image, prompt)
            save_image(image, f"output/cat_style_{i+1}.png")

if __name__ == "__main__":
    main()
