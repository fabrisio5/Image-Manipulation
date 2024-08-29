from PIL import Image
image = Image.open('TheShot.jpg')
image.show()
def edge_detection(img):
    width, height = img.size
    new_img = Image.new('RGB', (width, height))

    # Define Sobel operator
    Gx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    Gy = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    # Check the mode of the image
    if img.mode == 'RGB':
        # Convert image to grayscale manually
        gray_img = img.copy()  # Create a copy of the image for grayscale conversion
        for x in range(width):
            for y in range(height):
                r, g, b = img.getpixel((x, y))
                gray = int(0.299*r + 0.587*g + 0.114*b)
                gray_img.putpixel((x, y), (gray, gray, gray))  # Modify the copy, not the original image
    else:
        # If the image is not in 'RGB' mode, assume it's already in grayscale
        gray_img = img

    # Apply Sobel operator
    for x in range(1, width-1):
        for y in range(1, height-1):
            pixel_x = sum(sum(Gx[i][j] * (gray_img.getpixel((x+i-1, y+j-1))[0] if gray_img.mode == 'RGB' else gray_img.getpixel((x+i-1, y+j-1))) for j in range(3)) for i in range(3))
            pixel_y = sum(sum(Gy[i][j] * (gray_img.getpixel((x+i-1, y+j-1))[0] if gray_img.mode == 'RGB' else gray_img.getpixel((x+i-1, y+j-1))) for j in range(3)) for i in range(3))
            magnitude = min(int((pixel_x**2 + pixel_y**2)**0.5), 255)
            new_img.putpixel((x, y), (0, magnitude, 0) if magnitude > 0 else (0, 0, 0))

    return new_img
def resize(image, percent):
    width, height = image.size
    new_width = int(width * percent)
    new_height = int(height * percent)
    new_image = Image.new('RGB', (new_width, new_height))

    x_scale = width / new_width
    y_scale = height / new_height

    for x in range(new_width):
        for y in range(new_height):
            src_x = int(x * x_scale)
            src_y = int(y * y_scale)
            new_image.putpixel((x, y), image.getpixel((src_x, src_y)))

    return new_image
def On_top(background, overlay1, overlay2):
    # Resize overlay1 and apply edge detection
    overlay1_resized = resize(overlay1, 0.4)
    overlay1_edge = edge_detection(overlay1_resized)

    # Iterate over the pixels of overlay1_edge and put them onto background at (825, 540)
    for x in range(overlay1_edge.width):
        for y in range(overlay1_edge.height):
            background.putpixel((x + 825, y + 540), overlay1_edge.getpixel((x, y)))

    # Resize overlay2
    overlay2_resized = resize(overlay2, 0.5)

    # Iterate over the pixels of overlay2_resized and put them onto background at (300, 700)
    for x in range(overlay2_resized.width):
        for y in range(overlay2_resized.height):
            background.putpixel((x + 300, y + 700), overlay2_resized.getpixel((x, y)))

    return background
def top_half(image):
    width, height = image.size

    # Create a new image with half the height
    new_image = Image.new('RGB', (width, height // 2))

    # Copy the pixels from the top half of the original image to the new image
    for x in range(width):
        for y in range(height // 2):
            new_image.putpixel((x, y), image.getpixel((x, y)))

    return new_image
# Open the images
image = Image.open('TheShot.jpg')
cat_image = Image.open('cat.jpg')
dog_image = Image.open('dog.jpg')
# Resize the image by 70%
resized_image = resize(image, 0.7)
# Crop the top half of the dog image
top_half_dog = top_half(dog_image)
# Apply edge detection to the resized image and the top half of the dog image
edge_image = edge_detection(resized_image)
edge_dog_image = edge_detection(top_half_dog)
# Paste edge_cat_image and edge_dog_image onto edge_image
final_image = On_top(edge_image, cat_image, edge_dog_image)
# Display the final image
final_image.show()
