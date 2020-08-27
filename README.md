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

## Finetune navigation
refer detai [Path planning](https://husarion.com/tutorials/ros-tutorials/7-path-planning/)

### Parameters for trajectory planner
file: `trajectory_planner.yaml` in  `~/ros_workspace/src/tutorial_pkg/config/`

```
xy_goal_tolerance: 0.15
yaw_goal_tolerance: 0.25

```
These parameters define how far from destination it can be considered as reached. Linear tolerance is in meters, angular tolerance is in radians.

### Parameters for local cost map
file 'local_costmap_params.yaml' in  `~/ros_workspace/src/tutorial_pkg/config/`

```
static_map: false
```
This parameter defines if map can change in time, true if map will not change.
*need to check if should set as true*


### Common parameters for cost map
file: `costmap_common_params.yaml` in  `~/ros_workspace/src/tutorial_pkg/config/`

```
obstacle_range: 6.0
raytrace_range: 8.5
```
In `obstacle_range` this range obstacles will be considered during path planning, `raytrace_range` This defines range in which area could be considered as free
*need to check if can set obstacle_range: 3.0 raytrace_range: 3.5 like turtlebot3_waffle_pi*

