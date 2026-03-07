# TurtleSim Catcher Project 🐢

This project is a **ROS 2 based turtlesim automation project** where the main turtle (`turtle1`) automatically catches other spawned turtles.

A **Spawner Node** continuously spawns turtles in the simulation, while a **Controller Node** moves `turtle1` toward the **closest turtle**. When `turtle1` reaches a turtle, the spawner removes (kills) it from the simulation.

---

## Project Overview
The system works using two main components:

### 1. Turtle Spawner
```bash
turtlesim_catch_them_all/turtlesim_catch_them_all/turtle_spawner.py
```
Responsible for spawning turtles at random positions in the turtlesim environment.
Functions:
- Spawns turtles randomly
- Tracks spawned turtles
- Removes (kills) turtles when `turtle1` reaches them

### 2. Turtle Controller
```bash
turtlesim_catch_them_all/turtlesim_catch_them_all/turtle_controller.py
```
Controls the movement of `turtle1`.
Functions:
- Detects positions of spawned turtles
- Finds the closest turtle
- Moves `turtle1` toward that turtle using velocity commands

---

## Launching the Project
Run the following command to start the simulation:
```bash
ros2 launch my_robot_bringup turtlesim_catch_them_all.launch.xml
