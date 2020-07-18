
import os

item_path = []
for root, dirs, files in os.walk(".", topdown=False): 
    print(root, dirs, files)
    for name in files:
        path = os.path.join(root, name)
        if path.endswith("png"): # We want only the images
            item_path.append(path)

africa_path = item_path[:4]
eastAsia_path = item_path[4:8]
middleEast_path = item_path[8:12]
southAsia_path = item_path[12:16]
print(eastAsia_path)
