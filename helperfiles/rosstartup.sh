#!/bin/bash

# copy troshub service to 
# sudo cp roshub.service /etc/systemd/system/roshub.service

# change to executable
# chmod 744 /home/pi/repos/ros_hub/roshub.service

 # sudo systemctl start roshub.service
 # sudo systemctl stop roshub.service
 # sudo systemctl status roshub.service

# Alwyas run if u make chanfges to service
# sudo systemctl daemon-reload

# to enable on reboot use
# sudo systemctl enable roshub.service


source /opt/ros/kinetic/setup.bash
source /home/pi/repos/ros_hub/devel/setup.bash
# roscore
nohup roscore>/home/pi/repos/ros_hub/roscore.out 2>/home/pi/repos/ros_hub/roscore.err  & echo "$(date) : "$! > /home/pi/repos/ros_hub/roscore_run.pid && echo "$(date)">>/home/pi/repos/ros_hub/roscore_run.pid & 
sleep 60
roslaunch hubmain hubmain.launch