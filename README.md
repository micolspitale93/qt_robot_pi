README
======

Setup
-----

For instructions on how to setup the autostart, consult the README at [RobotPT's Cordial Public repo](https://github.com/robotpt/cordial-public)


1. Update ROS with new keys and update:

       sudo apt-key del 421C365BD9FF1F717815A3895523BAEEB01FA116
       sudo -E apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
       sudo apt clean && sudo apt update

2. Install `pyaudio` and ROS's `audio-common` libraries

       sudo apt-get install python-pyaudio ros-kinetic-audio-common

3. Clone this repository into your workspace's `src` directory

4. Use `catkin_make` to build the project.  Note if you run out of virtual
   memory, see about resizing your swap memory from the instructions 
   [here](https://github.com/robotpt/cordial-public).
