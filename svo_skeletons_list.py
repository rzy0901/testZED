import os
import pyzed.sl as sl
from tqdm import tqdm, trange
import shutil
from .svo_skeletons import cam_init, cam2mat

def copyDirectory_createMat(cam,file_dir,output_dir,body_format='BODY_18'):
    obj = os.scandir(file_dir)
    count = 1
    # for entry in tqdm(list(obj),desc=file_dir):
    for entry in list(obj):
        if entry.is_dir():
            os.makedirs(os.path.join(output_dir,entry.name),exist_ok=True)
            copyDirectory_createMat(cam,entry.path,os.path.join(output_dir,entry.name))
        if entry.is_file() and entry.name.endswith('.svo'):
            # temp = entry.name.split(".")
            # output_path = os.path.join(output_dir,temp[-2]+".mat")
            # 重命名为'run1.mat'，'run2.mat',...
            temp = os.path.basename(file_dir)
            output_mat_path = os.path.join(output_dir,temp+"_"+str(count)+".mat")
            count += 1
            cam_init(cam,entry.path,body_format)
            ERROR,_,_,_ = cam2mat(cam,output_mat_path)
            if ERROR == 0:
                print(f"Successfully convert {entry.path} to {output_mat_path}")
            else:
                print(f"ERROR:No data output in {output_mat_path}")
            cam.disable_object_detection()
            cam.disable_positional_tracking()
            cam.close()
    obj.close()

if __name__ == "__main__":
    file_dir = "/home/rzy/Documents/ZED/Data_1231/svos/"
    output_dir = "./data_new_18/" # 注意不要将'./data'写为'./data/'
    body_format = 'BODY_18'
    cam = sl.Camera()
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir,exist_ok=True)
    copyDirectory_createMat(cam,file_dir,output_dir,body_format)
    print('finished.')

        