# This project is for Rosbot2.0 and Rosbot2.0 Pro

## Hosts

* wifi network: Chaos
* robot master: 192.168.28.11 , login: sw/abc123!@# , wifi: Cloud
* robot nodes:
  * ros2p_0: 192.168.28.77 ssh: husarion/husarion, wifi: Chaos

## Install

### update environment and install neccesary packages

```
mkdir -p ~/ros_workspace/src
cd ~/ros_workspace/src
catkin_init_workspace
cd ..
catkin_make

cd src
git clone https://github.com/husarion/rosbot_description.git
git clone https://github.com/husarion/tutorial_pkg.git

sudo apt update

#Install dependencies
#sudo apt install python-rosdep2
#sudo rosdep init
#rosdep update
#rosdep install --from-paths src --ignore-src -r -y

#compile
cd ~/ros_workspace
catkin_make

#install enviroment
nano ~/.bashrc
# add: export ~/ros_workspace/devel/setup.sh
source ~/.bashrc


### install slam and navigation launch

```
#copy rosbot config yamls to multirobot_nv package
cd project_dir
cp -r map /home/husarion/ros_workspace/src/tutorial_pkg/maps
cp -r launch /home/husarion/ros_workspace/src/tutorial_pkg/launch
```

### Implementation reference for Rosbot 2.0
1. [map navigation](https://husarion.com/tutorials/ros-tutorials/9-map-navigation/)
2. [config files for movebase](https://github.com/husarion/tutorial_pkg/tree/master/config)
