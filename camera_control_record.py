import cv2
import pyzed.sl as sl

camera_settings = sl.VIDEO_SETTINGS.BRIGHTNESS
str_camera_settings = "BRIGHTNESS"
step_camera_settings = 1


print("Running...")
init = sl.InitParameters()
init.camera_resolution = sl.RESOLUTION.HD1080
init.depth_mode = sl.DEPTH_MODE.NONE
cam = sl.Camera()
if not cam.is_opened():
    print("Opening ZED Camera...")
status = cam.open(init)
if status != sl.ERROR_CODE.SUCCESS:
    print(repr(status))
    exit()

def runZed():
    print_camera_information(cam)
    fps = cam.get_camera_information().camera_configuration.fps
    # a = input('Press enter to begin recording.')
    runtime = sl.RuntimeParameters()
    mat = sl.Mat()
    record(cam, runtime, mat, filepath="./test.svo", nframe=fps*5)
    cam.close()

def print_camera_information(cam):
    print("Resolution: {0}, {1}.".format(round(cam.get_camera_information().camera_configuration.resolution.width, 2), cam.get_camera_information().camera_configuration.resolution.height))
    print("Camera FPS: {0}.".format(cam.get_camera_information().camera_configuration.fps))
    print("Firmware: {0}.".format(cam.get_camera_information().camera_configuration.firmware_version))
    print("Serial number: {0}.\n".format(cam.get_camera_information().serial_number))

def record(cam, runtime, mat, filepath, nframe):
    vid = sl.ERROR_CODE.FAILURE
    out = False
    while vid != sl.ERROR_CODE.SUCCESS and not out:
        record_param = sl.RecordingParameters(filepath)
        vid = cam.enable_recording(record_param)
        print(repr(vid))
        if vid == sl.ERROR_CODE.SUCCESS:
            print("Recording started...")
            frames_recorded = 0
            while True:  # for spacebar
                err = cam.grab(runtime)
                if err == sl.ERROR_CODE.SUCCESS:
                    frames_recorded += 1
                    print("Frame count: " + str(frames_recorded), end="\r") 
                    cam.retrieve_image(mat,sl.VIEW.LEFT)
                    cv2.imshow("ZED", mat.get_data())
                    key = cv2.waitKey(5)
                    if frames_recorded == nframe:
                        break
    cam.disable_recording()
    print("Recording finished.")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    runZed()
