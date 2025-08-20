# Getting Started Guide for Your ROS Workspace  

Welcome to the ROS workspace for your swarm drone project! This guide will help you get started with setting up and using the workspace, including the `mavsdk_interface` package and its `mavsdk_node`.  

## Prerequisites  
Before you begin, ensure you have the following installed:  
- ROS 2 jazzy
- MAVSDK  
- Python 3.x 

## Workspace Setup  
1. Clone the repository:  
    ```bash  
    git clone <repository_url> <local_dir> 
    cd ~/swarm_drone_ws  
    ```  

2. Build the workspace:  
    ```bash  
    colcon build  
    ```  

3. Source the workspace:  
    ```bash  
    source install/setup.bash  
    ```  

## Using `mavsdk_interface`  

### Running the Node  
To launch the `mavsdk_node`, use the following command:  
```bash  
ros2 run mavsdk_interface mavsdk_node  
```  

### Available Topics  
The `mavsdk_node` interacts with the following topics:  
- **Published Topics**:  
  - `/mavsdk/connection_status`: Provides telemetry data from the drone.  
  - `/mavsdk/uptime`: Reports the status of the current mission.  

<!-- - **Subscribed Topics**:  
  - `/mavsdk/command`: Accepts commands to control the drone.  
  - `/mavsdk/mission_upload`: Uploads a mission to the drone.  
  - `/mavsdk/parameter_set`: Sets parameters on the drone.   -->

Use `ros2 topic list` to view all available topics and `ros2 topic echo <topic_name>` to inspect their data.  

### Setting System Parameters  
The following parameters can be configured for the `mavsdk_node`:  
- `system_address`: The connection port of the drone (default: serial:///dev/ttyACM0:57600).  


<!-- To set these parameters, use the `ros2 param` command. For example:  
```bash  
ros2 param set /mavsdk_node system_id 1  
ros2 param set /mavsdk_node component_id 1  
ros2 param set /mavsdk_node connection_url udp://:14540  
```   -->

### Remapping Node Name and Namespace  
You can remap the node name or namespace by passing arguments during launch. For example:  
```bash  
ros2 run mavsdk_interface mavsdk_node --ros-args -r __node:=custom_node_name -r __ns:=/custom_namespace  
```  

Happy flying!  