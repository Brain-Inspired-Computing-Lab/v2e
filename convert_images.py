import os
import subprocess
import time

import cv2
import numpy as np
import polars as pl
from loguru import logger

# I/O PATHS
INPUT_DIR = "/home/hwpark/work/ASL/asl_alphabet_train/asl_alphabet_train"
OUTPUT_ROOT_DIR = "/home/hwpark/work/ASL/asl_alphabet_train/v2e_output"

# VIDEO GENERATION
FRAME_RATE = 60
DURATION = 1
FRAME_COUNT = int(FRAME_RATE * DURATION)
DEGREE_MOVEMENT = 10


def generate_video(
    file_name: str,
    path: str,
) -> tuple[str, str, str]:
    start_time = time.time()
    image = cv2.imread(path)

    if image is None:
        raise Exception(f"Error: Unable to read image from {path}")

    OUTPUT_DIR = f"{OUTPUT_ROOT_DIR}/{file_name}"
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    height, width, _ = image.shape

    generated_video_path = f"{OUTPUT_DIR}/{file_name}.mp4"
    video_writer = cv2.VideoWriter(
        generated_video_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        FRAME_RATE,
        (width, height),
    )

    for i in range(FRAME_COUNT):
        angle = (i / FRAME_COUNT) * DEGREE_MOVEMENT  # Move left
        M = np.float32([[1, 0, -angle], [0, 1, 0]])
        frame = cv2.warpAffine(image, M, (width, height))
        video_writer.write(frame)

    for i in range(FRAME_COUNT):
        angle = (
            1 - i / FRAME_COUNT
        ) * DEGREE_MOVEMENT  # Move back to the original position
        M = np.float32([[1, 0, -angle], [0, 1, 0]])
        frame = cv2.warpAffine(image, M, (width, height))
        video_writer.write(frame)

    # # Generate frames for right movement
    # for i in range(FRAME_COUNT):
    #     angle = (i / FRAME_COUNT) * DEGREE_MOVEMENT  # Move right
    #     M = np.float32([[1, 0, angle], [0, 1, 0]])
    #     frame = cv2.warpAffine(image, M, (width, height))
    #     video_writer.write(frame)

    # for i in range(FRAME_COUNT):
    #     angle = (
    #         1 - i / FRAME_COUNT
    #     ) * DEGREE_MOVEMENT  # Move back to the original position
    #     M = np.float32([[1, 0, angle], [0, 1, 0]])
    #     frame = cv2.warpAffine(image, M, (width, height))
    #     video_writer.write(frame)

    # # Generate frames for up movement
    # for i in range(FRAME_COUNT):
    #     angle = (i / FRAME_COUNT) * DEGREE_MOVEMENT  # Move up
    #     M = np.float32([[1, 0, 0], [0, 1, -angle]])
    #     frame = cv2.warpAffine(image, M, (width, height))
    #     video_writer.write(frame)

    # for i in range(FRAME_COUNT):
    #     angle = (
    #         1 - i / FRAME_COUNT
    #     ) * DEGREE_MOVEMENT  # Move back
    #     M = np.float32([[1, 0, 0], [0, 1, -angle]])
    #     frame = cv2.warpAffine(image, M, (width, height))
    #     video_writer.write(frame)

    video_writer.release()

    if not os.path.exists(generated_video_path):
        raise Exception(f"Error: Unable to generate video at {generated_video_path}")

    logger.info(f"Video generation took {time.time() - start_time} seconds")
    return generated_video_path, height, width


def convert_to_dvs(
    file_name: str,
    video_path: str,
    height: str,
    width: str,
) -> None:
    start_time = time.time()

    OUTPUT_DIR = f"{OUTPUT_ROOT_DIR}/{file_name}/dvs"
    DVS_PARAM = "clean"

    command = f"python3 v2e.py -i {video_path} -o {OUTPUT_DIR} --output_height {height} --output_width {width} --no_preview --skip_video_output --dvs_params {DVS_PARAM} --dvs_text {file_name} --disable_slomo"
    subprocess.run(command, shell=True)
    logger.info(f"Conversion took {time.time() - start_time} seconds")


def post_process_dvs(
    file_name: str,
) -> None:
    start_time = time.time()

    # read in the file
    full_path = f"{OUTPUT_ROOT_DIR}/{file_name}/dvs/{file_name}.txt"
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
    df.write_csv(f"{OUTPUT_ROOT_DIR}/{file_name}/{file_name}.csv", include_header=False)

    logger.info(f"Post processing took {time.time() - start_time} seconds")


if __name__ == "__main__":
    A_DIR = f"{INPUT_DIR}/A"
    C_DIR = f"{INPUT_DIR}/C"
    L_DIR = f"{INPUT_DIR}/L"

    with os.scandir(A_DIR) as entries:
        for i in range(1000):
            entry = next(entries)
            if entry.is_file():
                logger.info(f"{i+1}/1000: Processing {entry.name}")

                full_path = entry.path
                file_name = entry.name.split(".")[0]

                generated_video_path, height, width = generate_video(
                    file_name, full_path
                )
                convert_to_dvs(file_name, generated_video_path, height, width)
                post_process_dvs(file_name)

    with os.scandir(C_DIR) as entries:
        for i in range(1000):
            entry = next(entries)
            if entry.is_file():
                logger.info(f"{i+1}/1000: Processing {entry.name}")

                full_path = entry.path
                file_name = entry.name.split(".")[0]

                generated_video_path, height, width = generate_video(
                    file_name, full_path
                )
                convert_to_dvs(file_name, generated_video_path, height, width)
                post_process_dvs(file_name)

    with os.scandir(L_DIR) as entries:
        for i in range(1000):
            entry = next(entries)
            if entry.is_file():
                logger.info(f"{i+1}/1000: Processing {entry.name}")

                full_path = entry.path
                file_name = entry.name.split(".")[0]

                generated_video_path, height, width = generate_video(
                    file_name, full_path
                )
                convert_to_dvs(file_name, generated_video_path, height, width)
                post_process_dvs(file_name)

    # with os.scandir(INPUT_DIR) as entries:
    #     for entry in entries:
    #         if entry.is_file():
    #             logger.info(f"Processing {entry.name}")

    #             full_path = entry.path
    #             file_name = entry.name.split(".")[0]

    #             generated_video_path, height, width = generate_video(
    #                 file_name, full_path
    #             )
    #             convert_to_dvs(file_name, generated_video_path, height, width)
    #             post_process_dvs(file_name)
