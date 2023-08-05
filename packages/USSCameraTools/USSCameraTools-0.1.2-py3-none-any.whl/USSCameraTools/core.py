from __future__ import annotations
import time
import cv2
import numpy as np
from harvesters.core import Harvester
from typing import Optional, Union, Dict
import sys
import os
import glob
from enum import Enum
import copy

class Colorspace(Enum):
    RGB = 1
    BGR = 2
    HSV = 3
    GRAYSCALE = 4

class USSCamera:
    def __init__(self, connection_arg: Union[int,Dict[str:str]], cti_file: Optional[str] = None):
        '''
        USSCamera class provides functionality to interact with GigE cameras using Harvesters library.

        Args:
        ----
            connection_arg: Connection argument to create the image acquirer. It can be either an integer or a dictionary.
            cti_file (optional): Path to the CTI (Camera Transport Interface) file. If not provided, it attempts to auto-find
                the MatrixVision CTI file in the system's GENICAM_GENTL64_PATH environment variable.

        Raises:
        ------
            OSError: If the operating system is not Windows NT, Linux, or BSD.
            OSError: If the MatrixVision CTI file is not found.
            FileNotFoundError: If the provided CTI file path is invalid or the file does not exist.
            ValueError: If no cameras are found on the network.
            ValueError: If there is an error creating the image acquirer.

        Attributes:
        ----------
            harvesters_obj: The Harvester object used for managing cameras.
            image_acquirer_obj: The ImageAcquirer object created for image acquisition.

        '''

        self.harvesters_obj = None
        self.image_acquirer_obj = None

        #Operating System Check - Not Sure if needed
        if(sys.platform not in ["win32", "linux"]):
            raise OSError("Incorrect Operating System; must be on a Windows NT, Linux, or BSD platform.")

        #Attempt to Auto-Find CTI File
        if cti_file is None:
            #Designed to work only with the MatrixVision CTI file - to be tested with others
            try:
                cti_file = glob.glob(f"{os.environ['GENICAM_GENTL64_PATH']}/*.cti")[0]

            except OSError as e:
                raise OSError(f"MatrixVision CTI file not found, download it from http://static.matrix-vision.com/mvIMPACT_Acquire/2.41.0/")
        else:
            if not os.path.exists(cti_file):
                raise FileNotFoundError(f'.cti file not found at path: {cti_file}')


        #Create Harvesters Object
        self.harvesters_obj = Harvester()
        self.harvesters_obj.add_file(cti_file)
        self.harvesters_obj.update()

        #Check if Camera List is Empty
        if(len(self.harvesters_obj.device_info_list) == 0):
            raise ValueError("No Cameras Found on Network")

        #Attempt to create the image acquirer 
        try:
            self.image_acquirer_obj = self.harvesters_obj.create(connection_arg)
            # self.image_acquirer_obj.remote_device.node_map.TriggerActivation.value = "RisingEdge"
        
        except ValueError as e:
            raise e

    #TO REVIEW: SHOULD COLORSPACE CONVERSIONS HAPPEN INSIDE OF THIS FUNCTION OR A DIFFERENT FUNCTION?
    def get_image(self, setting: Optional[Colorspace] = None) -> np.ndarray:
        self.image_acquirer_obj.start()
        rtn_frame = None
        with self.image_acquirer_obj.fetch() as buffer:
            component = buffer.payload.components[0]
            frame = component.data.reshape(component.height, component.width,int(component.num_components_per_pixel))
            rtn_frame = copy.deepcopy(frame)
        self.image_acquirer_obj.stop()

        if(setting is not None):
            raise NotImplementedError

        return rtn_frame
    
    def trigger_camera(self):
        '''
        Triggers the camera to capture an image.

        This method checks if the camera is currently acquiring images. If not, it starts the acquisition process.
        It then checks if the camera's trigger mode is off. If it is, it sets the trigger source to 'Software' and turns the trigger mode on.
        After triggering the camera, it fetches the image data from the camera's buffer, reshapes it to match the image dimensions and number of components per pixel, and returns a deep copy of the image data.

        Note:
        ----
            There is a known issue where the first trigger is always black. This is currently being debugged.

        Returns:
        -------
            numpy.ndarray: A deep copy of the captured image data.
        '''

        if not self.image_acquirer_obj.is_acquiring():
            self.image_acquirer_obj.start()

        if self.image_acquirer_obj.remote_device.node_map.TriggerMode.value == 'Off':
            self.image_acquirer_obj.remote_device.node_map.TriggerSource.value = 'Software'
            self.image_acquirer_obj.remote_device.node_map.TriggerMode.value = 'On'

        rtn_frame = None

        self.image_acquirer_obj.remote_device.node_map.TriggerSoftware.execute()
        with self.image_acquirer_obj.fetch() as buffer:
            component = buffer.payload.components[0]
            frame = component.data.reshape(component.height, component.width,int(component.num_components_per_pixel))
            rtn_frame = copy.deepcopy(frame)

        return rtn_frame

    def get_continous_stream(self):
        self.image_acquirer_obj.start()
        self.image_acquirer_obj.remote_device.node_map.TriggerMode.value = 'Off'
        try:
            while True:
                with self.image_acquirer_obj.fetch() as buffer:
                    component = buffer.payload.components[0]
                    frame = component.data.reshape(component.height, component.width,int(component.num_components_per_pixel))
                    yielded_frame = copy.deepcopy(frame)
                    yield yielded_frame
        except GeneratorExit:
            self.image_acquirer_obj.stop()

    def get_camera_attribute(self, attribute: Optional[str] = None) -> Union[list,tuple]:
        '''
        Starts the camera's image acquisition process and retrieves a continuous stream of images.
    
        This method turns off the camera's trigger mode to start the continuous image streaming. 
        It then enters into an infinite loop where it continuously fetches image data from the camera's buffer.
        The image data is reshaped according to the image's dimensions and the number of components per pixel.
        A deep copy of each fetched image frame is then yielded. 
        In case of a 'GeneratorExit' exception, it stops the image acquisition and ends the function execution.

        Yields:
        ------
            numpy.ndarray: A deep copy of each fetched image frame from the continuous stream.

        Raises:
        ------
            GeneratorExit: An exception that is raised when the generator's close() method is called. 
            It signals the method to stop the image acquisition process.
        '''

        if(attribute is None):
            attribute_list = []
            for index,item in enumerate(dir(self.image_acquirer_obj.remote_device.node_map)):
                try:
                    attribute_dir = dir(eval(f'self.image_acquirer_obj.remote_device.node_map.{item}'))
                    if 'value' in attribute_dir:
                        attribute_list.append((item, eval(f'self.image_acquirer_obj.remote_device.node_map.{item}.value')))
                        
                except Exception as e:
                    pass
        
            return attribute_list

        else:
            try:
                if type(attribute) is str:
                    return (attribute, eval(f'self.image_acquirer_obj.remote_device.node_map.{attribute}.value'))
                else:
                    raise TypeError(f"Expected argument 'attribute' to be of type <class 'str'> but got type {type(attribute)}")

            except AttributeError:
                raise AttributeError(f'No such camera attribute with name {attribute}')
        
    def set_camera_attribute(self,setting: str,value):
        try:
            exec(f'self.image_acquirer_obj.remote_device.node_map.{setting}.value = {value}')

        except Exception as e:
            raise e
    
    def __del__(self):
        if self.image_acquirer_obj and self.image_acquirer_obj.is_valid():
            try:
                if self.image_acquirer_obj.is_acquiring():
                    self.image_acquirer_obj.stop()
            finally:
                self.image_acquirer_obj.destroy()
        if self.harvesters_obj:
            self.harvesters_obj.reset()