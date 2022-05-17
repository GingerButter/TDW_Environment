'''
Demo for magnet robot in TDW
'''

from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.add_ons.third_person_camera import ThirdPersonCamera
# from tdw.add_ons.image_capture import ImageCapture
from magnebot import Magnebot, ActionStatus, Arm
from tdw.librarian import ModelLibrarian
from tdw.add_ons.object_manager import ObjectManager


import numpy as np
import numpy
import cv2

import time

# # show all the objects in TDW
# librarian = ModelLibrarian()
# for record in librarian.records:
#     print(record.name)


def startTDW():
    c = Controller(launch_build=False)
    magnebot1 = Magnebot(position={"x": 0, "y": 0.5, "z": -1.13}, rotation={"x": 0, "y": 0, "z": 0},robot_id=c.get_unique_id())
    magnebot2 = Magnebot(position={"x": 0, "y": 0.5, "z": 1.13}, rotation={"x": 0, "y": 180, "z": 0},robot_id=c.get_unique_id())
    # Create a camera and enable image capture.
    camera1 = ThirdPersonCamera(position={"x": 0, "y": 1.3, "z": -1},
                            rotation={"x": 20, "y": 0, "z": 0},
                            field_of_view = 100,
                            avatar_id="a")
    
    om = ObjectManager(transforms=True, bounds=True, rigidbodies=True)
                            
    c.add_ons.extend([magnebot1, magnebot2, camera1,om])


    print("Setting Up Scene...")
    '''Set up scene'''
    commands = [{"$type": "set_screen_size",
                    "width": 512,
                    "height": 512}]
    commands.extend([{"$type": "set_render_quality", "render_quality": 4}])
    commands.extend([TDWUtils.create_empty_room(8, 8)])
    # commands.extend(c.get_add_physics_object(model_name='quatre_dining_table',
    #                                     #  library="models_core.json",
    #                                         position={"x": 0, "y": 0, "z": 0},
    #                                         kinematic = True,
    #                                         object_id=c.get_unique_id()))
    

    table_id =c.get_unique_id()
    commands.extend(c.get_add_physics_object(model_name='b05_table_new',
                                                position={"x": 0, "y": 0, "z": 0},
                                                rotation = {"x":0,"y":90,"z":0},
                                                object_id=table_id))

    c.communicate(commands)


    commands = []

    top = om.bounds[table_id].top
                                                

    bowl_id = c.get_unique_id()
    commands.extend(c.get_add_physics_object(model_name='b04_bowl_smooth',
                                        library="models_core.json",
                                            position={"x": top[0]-0.3, "y": top[1], "z":top[2]-0.6},
                                            rotation={"x":0,"y":120,"z":0},
                                            bounciness=0,
                                            kinematic = True,
                                            static_friction = 1,
                                            dynamic_friction = 1,
                                            object_id=bowl_id,
                                            ))

    apple_id = c.get_unique_id()
    commands.extend(c.get_add_physics_object(model_name='apple',
                                        library="models_core.json",
                                            position={"x": top[0], "y": top[1], "z": top[2]-0.63},
                                            bounciness=0,
                                            # mass=0.001,
                                            kinematic = True,
                                            static_friction = 1,
                                            dynamic_friction = 1,
                                            object_id=apple_id))


    orange_id = c.get_unique_id()
    commands.extend(c.get_add_physics_object(model_name='b04_orange_00',
                                        library="models_core.json",
                                           position={"x": top[0], "y": top[1], "z": top[2]+0.1},
                                            mass = 3,
                                            bounciness=0,
                                            object_id=orange_id))


    banana_id = c.get_unique_id()
    commands.extend(c.get_add_physics_object(model_name='chocolate_bar001',
                                        library="models_core.json",
                                            position={"x": top[0]+0.3, "y": top[1], "z": top[2]-0.6},
                                            bounciness=0,
                                            # mass=9999,
                                            static_friction = 1,
                                            dynamic_friction = 1,
                                            object_id=banana_id))

    # banana2_id = c.get_unique_id()
    # commands.extend(c.get_add_physics_object(model_name='b04_banana',
    #                                     library="models_core.json",
    #                                         position={"x": 0.24, "y": 0.8682562, "z": 0.4},
    #                                         mass = 3,
    #                                         bounciness=1,
    #                                         object_id=banana2_id))


    # apple2_id = c.get_unique_id()
    # commands.extend(c.get_add_physics_object(model_name='apple',
    #                                     library="models_core.json",
    #                                         position={"x": -0.17, "y": 0.8682562, "z": 0.25},
    #                                         mass = 3,
    #                                         bounciness=1,
    #                                         object_id=apple2_id))

    resp = c.communicate(commands)
    
    




    print("Starting TDW...")

    '''Control the robot by pick/drop'''
    magnebot1.grasp(apple_id,Arm.right)
    while magnebot1.action.status == ActionStatus.ongoing:
        c.communicate([])
    c.communicate([])
    magnebot1.reach_for(target={"x": top[0]-0.3, "y": top[1]+0.5, "z": top[2]-0.6}, arm=Arm.right)
    while magnebot1.action.status == ActionStatus.ongoing:
        c.communicate([])
    c.communicate([])
    magnebot1.reach_for(target={"x": top[0]-0.3, "y": top[1], "z":top[2]-0.6}, arm=Arm.right)
    while magnebot1.action.status == ActionStatus.ongoing:
        c.communicate([])
    c.communicate([])
    magnebot1.drop(apple_id,Arm.right)
    while magnebot1.action.status == ActionStatus.ongoing:
        c.communicate([])
    c.communicate([])
    # magnebot1.reach_for(target={"x": 0, "y": 1.2, "z": -1}, arm=Arm.right)
    # while magnebot1.action.status == ActionStatus.ongoing:
    #     c.communicate([])
    # c.communicate([])
    magnebot1.reset_arm(arm=Arm.right)
    while magnebot1.action.status == ActionStatus.ongoing:
        c.communicate([])
    c.communicate([])

    print("grasp completed")

    magnebot1.grasp(banana_id,Arm.right)
    while magnebot1.action.status == ActionStatus.ongoing:
        c.communicate([])
    c.communicate([])
    magnebot1.reach_for(target={"x": top[0]-0.3, "y": top[1]+0.33, "z":top[2]-0.6}, arm=Arm.right)
    while magnebot1.action.status == ActionStatus.ongoing:
        c.communicate([])
    c.communicate([])
    magnebot1.reach_for(target={"x": top[0]-0.3, "y": top[1]+0.15, "z":top[2]-0.6}, arm=Arm.right)
    while magnebot1.action.status == ActionStatus.ongoing:
        c.communicate([])
    c.communicate([])
    magnebot1.drop(banana_id,Arm.right)
    while magnebot1.action.status == ActionStatus.ongoing:
        c.communicate([])
    c.communicate([])
    # magnebot1.reach_for(target={"x": 0, "y": 1.2, "z": -1}, arm=Arm.right)
    # while magnebot1.action.status == ActionStatus.ongoing:
    #     c.communicate([])
    # c.communicate([])
    magnebot1.reset_arm(arm=Arm.right)
    while magnebot1.action.status == ActionStatus.ongoing:
        c.communicate([])
    c.communicate([])




def main():
    startTDW()

if __name__ == "__main__":
    main()