'''
This script is used to convert svo file to keypoint mat file for one person.
'''
import pyzed.sl as sl
from scipy.io import savemat
import argparse
import os
import numpy as np    

def main(args):
    input_svo_path = args.input_svo_path
    output_mat_path = args.output_mat_path
    output_dir = os.path.dirname(output_mat_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)   
    body_format = args.body_format
    cam = sl.Camera()
    cam_init(cam,input_svo_path,body_format)
    ERROR,_,_,_ = cam2mat(cam,output_mat_path)
    if ERROR == 0:
        print(f"Successfully convert {input_svo_path} to {output_mat_path}")
    else:
        print(f"ERROR:No data output in {output_mat_path}")
    cam.disable_object_detection()
    cam.disable_positional_tracking()
    cam.close()

def cam_init(cam,svo_path,body_format='BODY_18'):
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
    init_params.coordinate_units = sl.UNIT.METER          # Set coordinate units
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP
    # print("Using SVO file: {0}".format(svo_path))
    init_params.svo_real_time_mode = True # Real Time Modes would drop some frames.
    init_params.set_from_svo_file(svo_path)
    err = cam.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(f"ERROR: {svo_path} open failed!")
        exit(1)
    positional_tracking_parameters = sl.PositionalTrackingParameters()
    positional_tracking_parameters.set_as_static = True
    cam.enable_positional_tracking(positional_tracking_parameters)
    body_param = sl.BodyTrackingParameters()
    body_param.enable_tracking = True                # Track people across images flow
    body_param.enable_body_fitting = True            # Smooth skeleton move
    body_param.detection_model = sl.BODY_TRACKING_MODEL.HUMAN_BODY_ACCURATE 
    if body_format == 'BODY_18':
        body_param.body_format = sl.BODY_FORMAT.BODY_18
    elif body_format == 'BODY_34':
        body_param.body_format = sl.BODY_FORMAT.BODY_34
    elif body_format == 'BODY_38':
        body_param.body_format = sl.BODY_FORMAT.BODY_38
    else:
        print(f"ERROR: {body_format} is not supported!")
        exit(1)
    cam.enable_body_tracking(body_param)

def cam2mat(cam,output_path):
    body_runtime_param = sl.BodyTrackingRuntimeParameters()
    body_runtime_param.detection_confidence_threshold = 40
    bodies = sl.Bodies()
    body_format = bodies.body_format
    camera_info = cam.get_camera_information()
    fps = camera_info.camera_configuration.fps
    timestampList = []
    keypoints = []
    localorientations = []
    localpositions = []
    positions = []
    velocities = []
    while cam.grab() == sl.ERROR_CODE.SUCCESS:
        cam.retrieve_bodies(bodies, body_runtime_param)
        if bodies.is_new:
            timestamp = bodies.timestamp
            obj_array = bodies.body_list
            if obj_array == []:
                timestampList.append(timestamp.get_milliseconds())
                if body_format == sl.BODY_FORMAT.BODY_18.value:
                    keypoints.append(np.zeros((18,3)))
                elif body_format == sl.BODY_FORMAT.BODY_34.value:
                    keypoints.append(np.zeros((34,3)))
                elif body_format == sl.BODY_FORMAT.BODY_38.value:
                    keypoints.append(np.zeros((38,3)))
                positions.append(np.zeros((3,)))
                velocities.append(np.zeros((3,)))
                continue
            first_object = obj_array[0]
            keypoint = first_object.keypoint
            # localorientation = first_object.local_orientation_per_joint
            # localposition = first_object.local_position_per_joint
            position = first_object.position
            velocity = first_object.velocity	
            # Update List
            keypoints.append(keypoint)
            # localorientations.append(localorientation)
            # localpositions.append(localposition)
            timestampList.append(timestamp.get_milliseconds())
            positions.append(position)
            velocities.append(velocity)
    ERROR = 0
    try:
        if len(timestampList) == 0 or len(keypoints) == 0:
            ERROR = 1
            raise ValueError(f"Timestamp list or keypoints list for {output_path} is empty.")
    except ValueError as e:
        print(e)
    savemat(output_path,{'timestampList':timestampList,'keypoints':keypoints,'fps':fps,'positions':positions,'velocities':velocities})
    # print(f"Nframes:{len(keypoints)} {svo_path} {output_path}")
    return ERROR,timestampList,keypoints,fps

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert svo to mat.')
    parser.add_argument('-i','--input_svo_path', type=str, default='./data1.svo', help='Input svo path, default:./test.svo')
    parser.add_argument('-o','--output_mat_path', type=str, default='./data/temp.mat', help='Output: mat path, default:./data/temp.mat')
    parser.add_argument('-b','--body_format', type=str, default='BODY_18', help='Capatured body format, available selections: BODY_18, BODY_34, BODY_38; default:BODY_18')
    args = parser.parse_args()
    main(args)