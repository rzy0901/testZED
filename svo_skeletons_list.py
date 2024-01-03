import os
import pyzed.sl as sl
from scipy.io import savemat
from tqdm import tqdm, trange


def copyDirectory_createMat(file_dir,output_dir):
    obj = os.scandir(file_dir)
    count = 1
    for entry in tqdm(list(obj),desc=file_dir):
        if entry.is_dir():
            os.makedirs(os.path.join(output_dir,entry.name),exist_ok=True)
            copyDirectory_createMat(entry.path,os.path.join(output_dir,entry.name))
        if entry.is_file() and entry.name.endswith('.svo'):
            # temp = entry.name.split(".")
            # output_path = os.path.join(output_dir,temp[-2]+".mat")
            # 重命名为'run1.mat'，'run2.mat',...
            temp = os.path.basename(file_dir)
            output_path = os.path.join(output_dir,temp+"_"+str(count)+".mat")
            count += 1
            svo2mat(entry.path,output_path)
    obj.close()

def svo2mat(svo_path,output_path):
    zed = sl.Camera()
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
    init_params.coordinate_units = sl.UNIT.METER          # Set coordinate units
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP
    # print("Using SVO file: {0}".format(svo_path))
    init_params.svo_real_time_mode = True # Real Time Modes would drop some frames.
    init_params.set_from_svo_file(svo_path)
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)
    positional_tracking_parameters = sl.PositionalTrackingParameters()
    positional_tracking_parameters.set_as_static = True
    zed.enable_positional_tracking(positional_tracking_parameters)
    body_param = sl.BodyTrackingParameters()
    body_param.enable_tracking = True                # Track people across images flow
    body_param.enable_body_fitting = True            # Smooth skeleton move
    body_param.detection_model = sl.BODY_TRACKING_MODEL.HUMAN_BODY_ACCURATE 
    body_param.body_format = sl.BODY_FORMAT.BODY_34  # Choose the BODY_FORMAT you wish to use
    zed.enable_body_tracking(body_param)
    body_runtime_param = sl.BodyTrackingRuntimeParameters()
    body_runtime_param.detection_confidence_threshold = 40
    bodies = sl.Bodies()
    # Get ZED camera information
    camera_info = zed.get_camera_information()
    fps = camera_info.camera_configuration.fps
    timestampList = []
    keypoints = []
    localorientations = []
    localpositions = []
    while zed.grab() == sl.ERROR_CODE.SUCCESS:
        # Retrieve objects
        zed.retrieve_bodies(bodies, body_runtime_param)
        if bodies.is_new:
            timestamp = bodies.timestamp
            obj_array = bodies.body_list
            if obj_array == []:
                continue
            first_object = obj_array[0]
            keypoint = first_object.keypoint
            localorientation = first_object.local_orientation_per_joint
            localposition = first_object.local_position_per_joint	
            # Update List
            keypoints.append(keypoint)
            localorientations.append(localorientation)
            localpositions.append(localposition)
            timestampList.append(timestamp.get_milliseconds())
    # Disable modules and close camera
    zed.disable_object_detection()
    zed.disable_positional_tracking()
    zed.close()
    # print(sl.BODY_BONES_POSE_34)
    savemat(output_path,{'timestampList':timestampList,'keypoints':keypoints,'fps':fps})
    # print(len(timestampList))
    # print(len(keypoints))
    # print(len(keypoints[1]))
    # print(svo_path+ "  " +output_path)

if __name__ == "__main__":
    file_dir = "/home/rzy/Documents/ZED/Data_1231/svos"
    output_dir = "./data_new" # 注意不要将'./data'写为'./data/'
    os.makedirs(output_dir,exist_ok=True)
    copyDirectory_createMat(file_dir,output_dir)
    print('finished.')

        