# Pixls

This module is meant to provide functions to easily interface
with [pxls.space](https://github.com/pxlsspace/Pxls) websites. This takes care of the low-level interactions with
the website to let you focus on your code.

## Installation


## Examples
```
from pxls import PxlsConnector

conn = PxlsConnector("https://pxls.space")

# Get canvas size
width, height = conn.get_shape()

# Get color palette
palette = conn.get_palette()
# Get color list
rgb_colors = palette.get_colors('rgb')
hex_colors = palette.get_colors('hex')

# Get stats
canvas_stats = conn.get_stats()
```

Retrieve canvas image:
```
from pxls import PxlsConnector
import matplotlib.pyplot as plt

canvas_img = conn.get_canvas()
plt.imshow(canvas_img)
```

Retrieve template image:
```
from pxls import Template
import matplotlib.pyplot as plt

url = "https://pxls.space/#template=https%3A%2F%2FpxlsFiddle.com%2Ftemp%2F7JDiwX&tw=192&oo=1&ox=1131&oy=915&x=1217&y=971&scale=4.2"
template_img = Template.from_url(url)
plt.imshow(template_img)
```

Get uncompleted parts of a template:
```
template_height, template_width = template_img.shape[2:]

# Crop canvas to the part matching the template:
cropped_canvas = canvas_img[
    template_img.y:template_img.y+template_height,
    template_img.x:template_img.x+template_width
    ]

# Compare template and canvas
filled_mask = (cropped_canvas==template_img).all(axis=-1)

# Make all pixels that were correctly filled transparent
# in the template
template_progress = template_img.copy()
template_progress[filled_mask] = (0, 0, 0, 0)
plt.imshow(template_progress)

# Get completion percentage
tot_pixels = np.count_nonzero(template_img.any(axis=-1))
remaining_pixels = np.count_nonzero(template_progress.any(axis=-1))
print("Completion %:", 1 - remaining_pixels/tot_pixels)
```