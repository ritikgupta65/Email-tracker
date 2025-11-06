# APPS_SCRIPT_URL = https://script.google.com/macros/s/AKfycbz1dfxYpHiDxOdPIMmBzftJSopChxu79RpcWI7PSKuaxlZOiUyoykSESRKYGgZeoeDZ/exec
from PIL import Image

img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))  # fully transparent
img.save("pixel.png", "PNG")
print("Saved pixel.png")