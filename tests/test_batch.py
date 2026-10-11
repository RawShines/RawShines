# Sample Script to Generate a HDR image
import numpy as np
import exifread
import tifffile
import matplotlib.pyplot as plt
import pillow_heif
from PIL import Image
import subprocess
from pathlib import Path

import glob

tif_list = glob.glob("./assets/test_data/*.tif")
for tif_path in tif_list:
    # Parameters
    output_path = tif_path.replace(".tif", ".heic")
    # convert output_path to absolute path
    output_path = (Path.cwd() / output_path).resolve()
    # Read the TIF image into a numpy array
    tif_file = tifffile.TiffFile(tif_path)
    tif = tif_file.asarray().astype(np.uint32)
    tif = np.clip(tif * 1, 0, 65535).astype(
        np.uint16
    )  # enlarge the highlight to better demonstrate the HDR effect

    # Read the metadata from the TIF image
    tags = exifread.process_file(open(tif_path, "rb"))
    metadata_img = Image.open(tif_path)
    # print(metadata_img.getexif())
    # print("TIF image tags: ", tags)

    # Convert the TIF image to a HEIF image
    heif = pillow_heif.from_bytes(
        mode="RGB;16", data=tif.tobytes(), size=(tif.shape[1], tif.shape[0])
    )
    # heif.info["exif"] = metadata_img.getexif()
    heif.save(output_path)

    # Use the exiftool to add hdr render (in command line)
    # exiftool -overwrite_original_in_place -preserve '-CustomRendered=HDR (no original saved)' {output_path}
    # use python to call the command line
    # cmd_str = "exiftool -overwrite_original_in_place -preserve".split()
    # cmd_str.append(f"-CustomRendered=HDR (no original saved)")
    # cmd_str.append(f"{output_path}")
    # subprocess.run(cmd_str)
