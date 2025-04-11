import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import os

def generate_image(prompt, width=512, height=512, model="stable-diffusion"):
    """
    使用Pollinations.AI API生成图像
    
    参数:
        prompt (str): 描述要生成的图像的文本提示
        width (int): 图像宽度
        height (int): 图像高度
        model (str): 要使用的模型，可选值包括"stable-diffusion"和"sdxl"
        
    返回:
        PIL.Image: 生成的图像对象
    """
    # Pollinations.AI API端点
    url = "https://pollinations.ai/api/generate/image"
    
    # 请求参数
    params = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "model": model
    }
    
    print(f"正在生成图像，提示词: '{prompt}'")
    
    # 发送请求
    response = requests.post(url, json=params)
    
    # 检查响应状态
    if response.status_code == 200:
        # 从响应中获取图像URL
        image_url = response.json().get("imageUrl")
        print(f"图像生成成功，URL: {image_url}")
        
        # 下载图像
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        
        return image, image_url
    else:
        print(f"错误: {response.status_code} - {response.text}")
        return None, None

def save_image(image, filename="generated_image.png"):
    """
    保存生成的图像
    
    参数:
        image (PIL.Image): 要保存的图像
        filename (str): 文件名
    """
    if image:
        image.save(filename)
        print(f"图像已保存为: {filename}")
    else:
        print("没有图像可保存")

def display_image(image, prompt=""):
    """
    显示生成的图像
    
    参数:
        image (PIL.Image): 要显示的图像
        prompt (str): 用于生成图像的提示词
    """
    if image:
        plt.figure(figsize=(10, 10))
        plt.imshow(image)
        plt.axis('off')
        if prompt:
            plt.title(prompt)
        plt.show()
    else:
        print("没有图像可显示")

def main():
    """
    主函数，演示如何使用Pollinations.AI生成图像
    """
    # 创建输出目录
    os.makedirs("output", exist_ok=True)
    
    # 示例1：基本图像生成
    prompt1 = "一只在中国传统山水画风格中的机器人"
    image1, _ = generate_image(prompt1)
    if image1:
        display_image(image1, prompt1)
        save_image(image1, "output/chinese_landscape_robot.png")
    
    # 示例2：使用SDXL模型
    prompt2 = "未来城市天际线，赛博朋克风格，夜晚，霓虹灯"
    image2, _ = generate_image(prompt2, width=768, height=512, model="sdxl")
    if image2:
        display_image(image2, prompt2)
        save_image(image2, "output/cyberpunk_city.png")
    
    # 示例3：不同风格的实验
    styles = ["油画风格", "水彩画风格", "素描风格", "像素艺术风格"]
    base_prompt = "一只猫坐在窗台上"
    
    for i, style in enumerate(styles):
        prompt = f"{base_prompt}，{style}"
        image, _ = generate_image(prompt)
        if image:
            display_image(image, prompt)
            save_image(image, f"output/cat_style_{i+1}.png")

if __name__ == "__main__":
    main()
