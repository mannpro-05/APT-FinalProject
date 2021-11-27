import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import cv2
import re

'''
Creating a regular expression for numbers and storing it in a temp variable.
'''
_nsre = re.compile('([0-9]+)')

'''
This function will provides the key for sorting the images according their name.
'''


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]


'''
Parameters: The numpy 2d array of the position values of all the parsed columns of the CSV file, name of the video.

Processing: Will re-shape the 2d numpy array into a 3d numpy array to plot a point in a 3D plane.
With the help of the Axes3D the re-shaped array will be plotted into a 3D plane with the help of matplotlib.pyplot.
The images of every frame will be stored within a folder with the name of the video in a img directory.

Output:
It will generate the images for every frame of the chosen exercise and store them in video folder.
'''


def generate_images(pose_vals, video_name):
    # Re-shaping the numpy array to 3D array.
    video = pose_vals.reshape((pose_vals.shape[0] // 3, 3, pose_vals.shape[1]))

    print(video.shape)

    # Specifying the connection between the points for the.
    vector_points = [[0, 1], [0, 2], [0, 6], [1, 3],
                     [1, 7], [2, 4], [3, 5], [6, 8],
                     [7, 9], [8, 10], [9, 11], [6, 7]]
    fig = plt.figure()
    ax = Axes3D(fig)

    # Iterating through all the frames.
    for f in range(video.shape[2]):
        ax.clear()

        # Plotting the points in a 3D plane for a single frame.
        ax.scatter(video[:, 0, f], video[:, 1, f], video[:, 2, f], c="red", s=2)

        # Creating a line between the points.
        for v in vector_points:
            ax.plot([video[v[0], 0, f], video[v[1], 0, f]],
                    [video[v[0], 1, f], video[v[1], 1, f]],
                    zs=[video[v[0], 2, f], video[v[1], 2, f]], c="green")
        # Re-arranging the 3D plane so that the plotting looks good.
        ax.set_xlim3d(0, 1)
        ax.set_ylim3d(0, 1)
        ax.set_zlim3d(0, 1)
        ax.view_init(105, 90)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_zticklabels([])

        # Saving the image in the video directory with the frame number as the name of the image file.
        plt.savefig("img/{0}/{1}.jpg".format(video_name, f), dpi=300)
    print("done with images!")


'''
Parameters: Path of the image folder for the video, Index of the requested video, name of the requested video.

Processing: With the help of OpenCv cv2 images will be combined and generate a video out of it.

Output:
Generated a plotted video of the selected exercise form the pose-output.csv file.
'''


def generate_video(path, video_path, video_name):
    # Getting the a list of name of the images and sorting them.
    images = [img for img in os.listdir(path) if img.endswith(".jpg")]
    images.sort(key=natural_sort_key)

    # Generating video .mp4 out of those images.
    print("Making frames")
    frame = cv2.imread(os.path.join(path, images[0]))
    print("done with frames")
    height, width, layers = frame.shape
    print("Making video path")
    video = cv2.VideoWriter(filename=video_path + "\\" + video_name + ".mp4",
                            fourcc=0x31637661,
                            fps=15,
                            frameSize=(width, height))
    print("Making video")
    for image in images:
        video.write(cv2.imread(os.path.join(path, image)))

    cv2.destroyAllWindows()
    video.release()

    # Returing the name of video.
    return video_name + ".mp4"


'''
Parameters: Index of the requested video, name of the requested video.

Processing: This function will parse required columns of the pose-output.csv file.
Create a 2d numpy array of the columns.
Will check if the all the images of the selected video are there in the img directory or not.
If they are there it will check if the video is generated and return the path. If not then it will generate the video 
and return the path.
If images are not properly generated it will generate them, create the video and will return the path of the video

Output:
It returns the name of the generated video 
'''


def parsing_csv(video_idx, video_name):
    data = pd.read_csv("pose-output.csv")

    # Getting the required columns form the csv file.
    pose = data.values[video_idx, 1:37]
    c = pose.shape
    c = c[0]

    keypoint_vals = []

    # Parsing through the columns of the requested video.
    for keypoint_idx in range(c):
        list_vals = pose[keypoint_idx][1:-1].split(', ')
        keypoint_vals.append(list_vals)

    pose_vals = np.array(keypoint_vals, dtype=float)

    # Replacing blankSpace with - in the video_name.
    video_name = video_name.replace(" ", "-")
    # Creating a path to the image folder for the selected video.
    image_path = os.getcwd() + '\\img\\' + video_name
    # Creating a path to store the video.
    video_path = os.getcwd() + '\\static'

    # This will check if the path already exist.
    if os.path.exists(image_path):

        total_files_in_dir = len([name for name in os.listdir(image_path)])
        total_frames = len(pose_vals[0])

        # Checking if all the images are there.
        if not total_files_in_dir == total_frames:
            generate_images(pose_vals, video_name)

        return generate_video(image_path, video_path, video_name)


    # If path does not exist generate image dir for the video, generate images and then generate video.
    else:
        # Creating a dir for the video.
        os.mkdir(os.getcwd() + '\\img\\' + video_name)
        generate_images(pose_vals, video_name)
        return generate_video(image_path, video_path, video_name)
