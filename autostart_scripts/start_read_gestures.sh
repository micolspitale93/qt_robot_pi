# !/bin/bash

source /home/qtrobot/robot/autostart/qt_robot.inc

SCRIPT_NAME="start_audio.sh"
LOG_FILE=$(prepare_logfile "$SCRIPT_NAME")

echo "Starting"

{
prepare_ros_environment
wait_for_ros_node "/rosout" 60
wait_for_tcpip_port 1883 60



roslaunch qt_robot_read_gesture read_gestures.launch
} &>> ${LOG_FILE}


echo "Finished"
