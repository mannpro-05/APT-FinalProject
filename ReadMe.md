# Advance Programming Techniques

# Final Project

### Mann Prajapati | U52609954

- The pose-output.csv file is located in the source directory. This file contains the tensor for the pose estimation
  algorithm. This tensor will be used to create a visualization of the given exercises in the CSV file.
- Since the flask framework is being used for building this webapp all the static files like the css and javascript
  files are in the static directory of the project. The Html files are in the template directory of the project.
- Also, the videos that are generated in this project are also stored in the static folder as flask recommend's to keep
  all the static files in the static folder.
- The images are stored in a folder which are named on the base of the exercise. All these image folders are located in
  the img directory of source directory.
- All the routes of the webpage are handled in the app.py file and the generation of the images and the video is done in
  the main.py
- There is a requirement.txt file in the source directory of the project which contains all the libraries that being
  used in this project. To execute this file all you have to do is to run this command in the terminal.

```bash
pip install -r requirements.txt
```

- To run the project you have to navigate to the source directory of the project and just have to execute the run.py
  file with the following command.

```bash
 python app.py
```

OR

```bash
 python3 app.py
```

# How to create a visualization in the frontend.

- The webapp is running on the local host and on the 5000 port so make sure no other service is running on the 5000 port
  or else it will give an error. The link to the webapp would be http://127.0.0.1:5000/
- Once you open the link in the browser you will see a dropdown list with all the exercises mentioned in it.
- You select any on of the exercise and click on the submit button. It will take some time for the video to show up on
  the screen.
- Once the video is generated it will automatically start playing the video in the browser.

# Execution of the program.

## Frontend-backend communication.

- To establish the communication between the frontend and the backend Ajax jQuery is used. It sends a post request with
  JSON data to the backend where the data is processed. When the user clicks on the submit button a json data with the
  name of the exercise will be sent to the backend.'

## Parsing data in the backend.

- Now that we have the name of the video we find the index of the video in the pose-output.csv file.
- In the scv file the first 37 columns contains meaningful data, so I am getting 1st till 36th columns (Index starts at
    0) data of the selected video by using the pandas' library.
- Now I iterate through all the columns, parse the content of every column and append it in a list called pose_vals.
  After parsing all the required data I am converting the pose_vals list into a numpy array.
- After having the index of the video I am checking if the path to the image for the chosen video already exists or not.
    - If it exists and if all the images are present, I do not create them again. This saves a lot of time.
    - If it exists all the images are not present then we generate them properly so that we get the output that we
      desire.
    - And finally we generate the video whether it exists or not. This is done just to make sure that the video has been
      created properly.
    - If it does not exist then we generate the path for the images, add images to it and then generate the video out of
      those images.

## Image generation

- before generating the images we have re-arrange the data in such a way that the x, y and z coordinates of a point are
  clubbed together so that we can plot them in a 3d plane. To do this I am using reshape method of numpy library. So,
  basically I am converting a 2-D array to a 3-D array. Now the data is ready to generate images out of it.
- To generate the images in need to do two things:
    - Plotting the points in a 3D plane:
        - To plot a point in a 3D plane im using the Axes3D from the mpl_toolkits.mplot3d library with passing
          plt.figure() as an argument in it.
        - Now we iterate through every frame for the exercise and plot the points by using the scatter method of the
          Axes3D library.
        - In this method we provide the coordinates of all the axis (x,y and z).
        - We also provide the color of the point as red.
    - Plotting a vector/line between specific plotted points.
        - I am pre-defining a 2d list which contains the list of all the points which needs to be connected so form a
          meaningful visualization.
        - Once we have the plotted points we iterate through that pre-defined list and use the plot method of the Axes3D
          library. In its method I provide the connecting points for all 3 axis and the color of the vector/line which
          connects the points.
- Now I am Re-arranging the 3D plane so that the plotting looks good i.e. rotating the entire plane in required
  direction so that we can observe the visualization from a proper angle. to do that we are using the view_init method
  of the Axes3D library which takes an elevation angle in the z plane and angle in the (x, y) plane as arguments.
- To generate an image of the plotted graph we use the savefig method of the matplotlib.pyplot library which takes name
  of the image and dpi of the image as 2 arguments.

## Generation of video.

- Once we have all the images I am calling the generate_video method which need the path to the image directory, path to
  save the video and name of the video.
- Now I am getting a list of all the image names in given path to the image and sorting the alphanumeric string of the
  images.
- Now I am creating a frame of a single image to get the height, width and layers of all the images. This is done to get
  the dimension of the all the images which is used to generate the video. To generate the frame I am using the imread
  method of the cv2 library which takes the path to the image and name of the image as arguments.
- Now I am creating an instance of the VideoWriter of the cv2 library which takes filename, fourcc, fps and the
  frameSize as arguments.
    - filename is the name of the file.
    - fourcc is the video format
    - fps is the frames per second of the video.
    - frame size is the dimension of the video.
- to generate the video we iterate through all the images in the given path, and use the write method of the VideoWriter
  method which takes the frame as an argument and for creating the frame we again use the imread method of the CV2
  library which I used earlier to create a single frame.

# Note

- Please make sure that you have python3 installed in your system, no service is running on 5000 port and have all the
  libraries provided in the requirements.txt file installed in your system before executing the project.
