import pandas as pd
import matplotlib.pyplot as plt

name_csv = "timing_results.csv"
# Load results from the CSV file
results = pd.read_csv(name_csv)

# Create a plot of the data
plt.figure(figsize=(10, 6))
plt.plot(results['Run'], results['Read Time'], label='Read Time', marker='o')
plt.plot(results['Run'], results['Count Time'], label='Count Time', marker='o')
plt.plot(results['Run'], results['Join and Order Time'], label='Join and Order Time', marker='o')
plt.plot(results['Run'], results['Total Time'], label='Total Time', marker='o')
plt.xlabel('Run Number')
plt.ylabel('Time (seconds)')
plt.title('Performance Metrics Across Runs')
plt.legend()
plt.grid(True)

# Save the plot to a JPG file
plt.savefig(f"{name_csv}.jpg", format='jpg')
plt.show()


import pandas as pd
import matplotlib.pyplot as plt

# Create a plot of RAM usage
plt.figure(figsize=(10, 6))
plt.plot(results['Run'], results['Total RAM'], label='Total RAM', color='blue', marker='s')
plt.xlabel('Run Number')
plt.ylabel('Total RAM (GB)')
plt.title('RAM Usage Across Runs')
plt.legend()
plt.grid(True)

# Save the plot to a file
plt.savefig(f"{name_csv}_ram.jpg", format='jpg')
plt.show()

from PIL import Image

# Open the images
img1 = Image.open(f"{name_csv}.jpg")
img2 = Image.open(f"{name_csv}_ram.jpg")

# Resize images to the same height
img2 = img2.resize((img1.width, img1.height))

# Combine images horizontally
total_width = img1.width + img2.width
combined_image = Image.new('RGB', (total_width, img1.height))
combined_image.paste(img1, (0, 0))
combined_image.paste(img2, (img1.width, 0))

# Save the combined image
combined_image.save(f"{name_csv}_combined_metrics.jpg")
combined_image.show()

