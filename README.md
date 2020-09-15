# This project is for Rosbot2.0 and Rosbot2.0 Pro

## Hosts

* wifi network: Chaos
* robot master: 192.168.28.11 , login: sw/abc123!@# , wifi: Cloud
* robot nodes:
  * ros2p_0: 192.168.28.77 ssh: husarion/husarion, wifi: Chaos

## Requirements

### install ROS environment to run roscore in another host (ignore if just use the rosbot node)

**roscore host and rosbot should be running in same Ros version**

* roscore host
  * refer [Ubuntu install of ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) to install ROS Kinetic
  * refer [Ubuntu install of ROS Melodic] to install ROS Melodic
* rosbot node
  * refer [ROSbot 2.0 Pro](https://husarion.com/downloads/) to reinstall ROS Kinetic or Melodic



my system configuration is:

* roscore host: Ubuntu 16.04 + ROS Kinetic + python 2.7
* rosbot node: Ubuntu 16.04 + ROS Kinetic + python 2.7



### config roscore host (ignore if just use the rosbot node)

refer [Running ROS on multiple machines](https://husarion.com/tutorials/ros-tutorials/5-running-ros-on-multiple-machines/) to config the `~/.bashrc`

### config rosbot node

```
sudo apt update

mkdir -p ~/projects
cd ~/projects
git clone https://github.com/wdxpz/rosbot2.git

mkdir -p ~/ros_workspace/src
cd ~/ros_workspace/src
catkin_init_workspace
cd ..
catkin_make

cd src
git clone https://github.com/husarion/rosbot_description.git
git clone https://github.com/husarion/tutorial_pkg.git

cd ~/ros_workspace/src
catkin_create_pkg multi_rosbot_nav
cd multi_rosbot_nav
cp -r ~/projects/rosbot2/multi_rosbot_nav/* .
cd ..

#Install dependencies (optional)
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
```



## scan the environment map

refer [SLAM navigation](https://husarion.com/tutorials/ros-tutorials/6-slam-navigation/) for details

```
roscore
```

```
roslaunch multi_rosbot_nav slam.launch
########
# use i, j, k, l, , to control robot movements
########
```

```
roscd multi_rosbot_nav/maps
mkdir new_map
cd new_map
rosrun map_server map_saver -f map
```



## navigate the robot in the map

* run the roscore in roscore host or rosbot node

```
roscore
```

* change the map file configuration at rosbot node

```
roscd multi_rosbot_nav/launch
nano nav.launch

######
# modify the follwing configuration:
# <arg name="map_file" default="$(find multi_rosbot_nav)/maps/new_map/map.yaml"/>
######
```

* if use rviz to navigate the robot

```
roslaunch multi_rosbot_nav nav.launch
#you can use "2D Pose Estimation" button in rviz to get the coordinate of a target location 
```

* if use `~/projects/rosbot2/goto_s.py` to navigate the robot

```
# use "2D Pose Estimation" button in rviz to get the target location's coordinate

# change the target position in goto_s.py
# position = {'x': 0.0, 'y' : 0.7}

python goto_s.py
```



## reference for Rosbot 2.0

```


1. [map navigation](https://husarion.com/tutorials/ros-tutorials/9-map-navigation/)
2. [config files for movebase](https://github.com/husarion/tutorial_pkg/tree/master/config)
```



## Fine-tune navigation

refer detail [Path planning](https://husarion.com/tutorials/ros-tutorials/7-path-planning/)

### Parameters for trajectory planner
file: `trajectory_planner.yaml` in  `~/ros_workspace/src/tutorial_pkg/config/`

```
xy_goal_tolerance: 0.15
yaw_goal_tolerance: 0.25

These parameters define how far from destination it can be considered as reached. Linear tolerance is in meters, angular tolerance is in radians.
```
### Parameters for local cost map
file 'local_costmap_params.yaml' in  `~/ros_workspace/src/tutorial_pkg/config/`

```
static_map: false

This parameter defines if map can change in time, true if map will not change.
*need to check if should set as true*
```
### Common parameters for cost map
file: `costmap_common_params.yaml` in  `~/ros_workspace/src/tutorial_pkg/config/`

```
obstacle_range: 6.0
raytrace_range: 8.5

In `obstacle_range` this range obstacles will be considered during path planning, `raytrace_range` This defines range in which area could be considered as free
*need to check if can set obstacle_range: 3.0 raytrace_range: 3.5 like turtlebot3_waffle_pi*


```
### tune the performance to avoid error like `Costmap2DROS transform timeout`, `Could not get robot pose, cancelling reconfiguration`
1. refer [control loop missed its desired rate, but with low CPU load](https://answers.ros.org/question/207010/control-loop-missed-its-desired-rate-but-with-low-cpu-load/) and [Problem loading prebuilt map](https://community.husarion.com/t/problems-loading-pre-built-map/700/19) to see how to adjust local_cost params and acml node parasm, acutally it is found these param work:



```
#local_costmap_paras.yaml
  transform_tolerance: 0.5
  resolution: 0.05

#acml node params
  <param name="transform_tolerance" value="0.5"/>
  <param name="update_min_d" value="0.2"/>
  <param name="update_min_a" value="0.2"/>
  <param name="min_particles" value="500"/> #these two paras are for waffle_pi, they may be increase a little bit
  <param name="max_particles" value="3000"/> 
  
 and also `control loop rate` in `move_base` node:
  <param name="controller_frequency" value="5.0" /> #origin value is 10
```

