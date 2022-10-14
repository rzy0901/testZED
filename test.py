from fileinput import filename
from sqlite3 import Timestamp
import pyzed.sl as sl
from scipy.io import savemat

if __name__ == "__main__":
    print("Running Body Tracking sample ... Press 'q' to quit")

    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
    init_params.coordinate_units = sl.UNIT.METER          # Set coordinate units
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP

    # If applicable, use the SVO given as parameter
    # Otherwise use ZED live stream
    filepath = '/home/rzy/Documents/ZED/HD1080_SN35745898_19-28-43.svo'
    print("Using SVO file: {0}".format(filepath))
    init_params.svo_real_time_mode = True
    init_params.set_from_svo_file(filepath)

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    # Enable Positional tracking (mandatory for object detection)
    positional_tracking_parameters = sl.PositionalTrackingParameters()
    # If the camera is static, uncomment the following line to have better performances and boxes sticked to the ground.
    positional_tracking_parameters.set_as_static = True
    zed.enable_positional_tracking(positional_tracking_parameters)

    obj_param = sl.ObjectDetectionParameters()
    obj_param.enable_body_fitting = True            # Smooth skeleton move
    # Track people across images flow
    obj_param.enable_tracking = True
    obj_param.detection_model = sl.DETECTION_MODEL.HUMAN_BODY_FAST
    # Choose the BODY_FORMAT you wish to use
    obj_param.body_format = sl.BODY_FORMAT.POSE_18

    # Enable Object Detection module
    zed.enable_object_detection(obj_param)

    obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
    obj_runtime_param.detection_confidence_threshold = 40

    # Get ZED camera information
    camera_info = zed.get_camera_information()

    # Create ZED objects filled in the main loop
    bodies = sl.Objects()
    timestampList = []
    keypoints = []

    while zed.grab() == sl.ERROR_CODE.SUCCESS:
        # Retrieve objects
        zed.retrieve_objects(bodies, obj_runtime_param)
        if bodies.is_new:
            # timestamp = zed.get_timestamp(sl.TIME_REFERENCE.CURRENT)
            timestamp = bodies.timestamp
            obj_array = bodies.object_list
            first_object = obj_array[0]
            keypoint = first_object.keypoint
            # Update List
            keypoints.append(keypoint)
            timestampList.append(timestamp.get_milliseconds())

    # Disable modules and close camera
    zed.disable_object_detection()
    zed.disable_positional_tracking()
    zed.close()

    file = open('./' + 'data.txt', 'w', encoding='utf-8')

    savemat('data.mat',{'timestampList':timestampList,'keypoints':keypoints})

    print(len(timestampList))
    print(len(keypoints))
