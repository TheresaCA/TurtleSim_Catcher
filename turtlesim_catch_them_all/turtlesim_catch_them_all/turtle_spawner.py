#!/usr/bin/env python3
import rclpy
import random
import math
from rclpy.node import Node
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
from functools import partial
from my_robot_interfaces.msg import Turtle
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.srv import CatchTurtle


class TurtleSpawnerNode(Node): 
    def __init__(self):
        super().__init__("turtle_spawner") 
        self.declare_parameter("spawn_frequency", 1.0)
        
        self.alive_turtles_ = []
        # self.spawn_freq = self.get_parameter(
        #     "spawn_frequency").value
        self.spawn_client_ = self.create_client(Spawn, "/spawn")
        self.kill_client_ = self.create_client(Kill, "/kill")
        self.create_timer(0.8, self.spawn_new_turtle)
        self.counter_1_ = 2
    
        #make a publisher to send coordinats along with name
        self.turtles_publisher_ = self.create_publisher(
            TurtleArray, "alive_turtles", 10)
        #killing the turtle
        self.catch_turtle_service = self.create_service(CatchTurtle, "catch_turtle", self.callback_catch_turtle)
    
    
    def callback_catch_turtle(self, request: CatchTurtle.Request, response: CatchTurtle.Response):
        self.call_kill_service(request.name)
        response.success = True 
        return response
    
        
    def publish_alive_turtles(self):
        msg = TurtleArray()
        msg.turtles = self.alive_turtles_
        self.turtles_publisher_.publish(msg)
    
    
    def spawn_new_turtle(self):
        name = "turtle"+str(self.counter_1_)
        self.counter_1_ += 1
        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)
        theta = random.uniform(0.0, 2*math.pi)
        self.call_spawn_service(name, x, y, theta)
    
    def call_spawn_service(self, turtle_name, x, y, theta):
        while not self.spawn_client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for service....")
            
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = turtle_name
        future = self.spawn_client_.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_spawn_service, request=request))
        
    def callback_call_spawn_service(self, future, request):
        response: Spawn.Response = future.result()
        if response.name != "":
            self.get_logger().info(
                "New alive turtle: " +response.name)
            new_turtle = Turtle()
            new_turtle.name = response.name
            new_turtle.x = request.x
            new_turtle.y = request.y
            new_turtle.theta = request.theta
            self.alive_turtles_.append(new_turtle)
            self.publish_alive_turtles()
            
    def call_kill_service(self, turtle_name):
        while not self.kill_client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for kill service....")
        request = Kill.Request()
        request.name = turtle_name
        future = self.kill_client_.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_kill_service, request=request))
        
    
    def callback_call_kill_service(self, future, request: Kill.Request):
        for (i, turtle) in enumerate(self.alive_turtles_):
            if turtle.name == request.name:
                del self.alive_turtles_[i]
                self.publish_alive_turtles()
                break
        

def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    #node.call_spawn_service("test", 3.0, 3.0, 0.0)  <for testing>
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
