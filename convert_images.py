# import os

import os
import subprocess
import time

import polars as pl
from loguru import logger


def convert_to_dvs(
    file_name: str,
    video_path: str,
    output_path: str,
) -> None:
    start_time = time.time()
    # output csv is 346 x 260 (however, able to adjust output height and width manually
    # get rid of --dvs346 and use the '--output_height' and '--output_width' options
    command = f"python3 v2e.py --input_frame_rate 24 --dvs346 --no_preview option --skip_video_output --dvs_params clean -i /home/hwpark/work/bcl/test_image_dir -o {output_path} --dvs_text {file_name}"
    subprocess.run(command, shell=True)
    logger.info(f"Conversion took {time.time() - start_time} seconds")


def post_process_dvs(
    file_name: str,
    path: str,
) -> None:
    start_time = time.time()

    # read in the file
    full_path = f"{path}/{file_name}.txt"
    events = []
    with open(full_path, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            # split the line with whitespace
            parts = line.split()

            # convert second to microsecond
            parts[0] = int(float(parts[0]) * 1_000_000)

            events.append((parts[1], parts[2], parts[3], parts[0]))

    # save the file
    df = pl.DataFrame(events, orient="row")
    df.write_csv(f"{path}/{file_name}.csv", include_header=False)

    logger.info(f"Post processing took {time.time() - start_time} seconds")


def convert_images() -> None:
    # Initialize the paths
    INPUT_DIR = "/home/hwpark/work/bcl/test_image_dir"
    OUTPUT_DIR = "image_output"

    # Create the output directory if it does not exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    convert_to_dvs("test", INPUT_DIR, OUTPUT_DIR)
    # # Get the list of processed files
    # processed_files = []
    # with os.scandir(OUTPUT_DIR) as entries:
    #     for entry in entries:
    #         if entry.is_dir():
    #             processed_files.append(entry.name)

    # # Iterate over the input directory
    # with os.scandir(INPUT_DIR) as entries:
    #     for entry in entries:
    #         if entry.is_file():
    #             logger.info(f"Processing {entry.name}")
    #             file_name = entry.name.split(".")[0]
    #             output_path = f"{OUTPUT_DIR}/{file_name}"

    #             # skip if already processed
    #             if file_name in processed_files:
    #                 logger.info(f"Skipping {entry.name}")
    #                 continue

    #             # Convert the video to DVS
    #             logger.info(f"Processing {entry.name}")
    #             convert_to_dvs(file_name, entry.path, output_path)

    #             # Post process the DVS file
    #             post_process_dvs(file_name, OUTPUT_DIR)


if __name__ == "__main__":
    convert_images()
    post_process_dvs("test", "image_output")
