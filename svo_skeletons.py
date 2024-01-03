import pyzed.sl as sl
from scipy.io import savemat

if __name__ == "__main__":
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
    filepath = './HD1080_SN35745898_18-04-50.svo'
    
    print("Using SVO file: {0}".format(filepath))
    init_params.svo_real_time_mode = True # Real Time Modes would drop some frames.
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

    body_param = sl.BodyTrackingParameters()
    body_param.enable_tracking = True                # Track people across images flow
    body_param.enable_body_fitting = False            # Smooth skeleton move
    body_param.detection_model = sl.BODY_TRACKING_MODEL.HUMAN_BODY_ACCURATE 
    body_param.body_format = sl.BODY_FORMAT.BODY_18  # Choose the BODY_FORMAT you wish to use

    # Enable Object Detection module
    zed.enable_body_tracking(body_param)

    body_runtime_param = sl.BodyTrackingRuntimeParameters()
    body_runtime_param.detection_confidence_threshold = 40

    # Get ZED camera information
    camera_info = zed.get_camera_information()
    fps = camera_info.camera_configuration.fps

    # Create ZED objects filled in the main loop
    bodies = sl.Bodies()
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

    # savemat('./data/data_all.mat',{'timestampList':timestampList,'keypoints':keypoints,'localorientations':localorientations,'localpositions':localpositions})
    savemat('./data/data_all.mat',{'timestampList':timestampList,'keypoints':keypoints,'fps':fps})
    print(len(timestampList))
    print(len(keypoints))
    print(len(keypoints[1]))
    print('finished.')

    
