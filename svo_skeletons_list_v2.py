import os
import pyzed.sl as sl
from tqdm import tqdm, trange
import shutil
import subprocess

def copyDirectory_createMat(file_dir,output_dir,body_format='BODY_18'):
    obj = os.scandir(file_dir)
    count = 1
    # for entry in tqdm(list(obj),desc=file_dir):
    for entry in list(obj):
        if entry.is_dir():
            os.makedirs(os.path.join(output_dir,entry.name),exist_ok=True)
            copyDirectory_createMat(entry.path,os.path.join(output_dir,entry.name))
        if entry.is_file() and entry.name.endswith('.svo'):
            # temp = entry.name.split(".")
            # output_path = os.path.join(output_dir,temp[-2]+".mat")
            # 重命名为'run1.mat'，'run2.mat',...
            temp = os.path.basename(file_dir)
            output_mat_path = os.path.join(output_dir,temp+"_"+str(count)+".mat")
            command = [
                "python3","svo_skeletons.py","-i", entry.path,"-o", output_mat_path,"-b", body_format
            ]
            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running the script: {e}")
            count += 1
    obj.close()

'''
直接运行有时候程序会卡住，原因不明，所以将命令写入文件，然后运行该文件
Export mode:    0=Export LEFT+RIGHT AVI.
                1=Export LEFT+DEPTH_VIEW AVI.
                2=Export LEFT+RIGHT image sequence.
                3=Export LEFT+DEPTH_VIEW image sequence.
                4=Export LEFT+DEPTH_16Bit image sequence.
'''
commands = []
def copyDirectory_createMP4(file_dir,output_dir,mode=1):
    obj = os.scandir(file_dir)
    count = 1
    # for entry in tqdm(list(obj),desc=file_dir):
    for entry in list(obj):
        if entry.is_dir():
            os.makedirs(os.path.join(output_dir,entry.name),exist_ok=True)
            copyDirectory_createMP4(entry.path,os.path.join(output_dir,entry.name))
        if entry.is_file() and entry.name.endswith('.svo'):
            temp = os.path.basename(file_dir)
            output_mp4_path = os.path.join(output_dir,temp+"_"+str(count)+".mp4")
            command = f"python3 svo_export.py {entry.path} {output_mp4_path} {mode}"
            commands.append(command)
            count += 1
    obj.close()

if __name__ == "__main__":
    file_dir = "/home/rzy/Documents/ZED/Data_1231/svos/"
    output_dir = "./data_new_18/" # 注意不要将'./data'写为'./data/'
    body_format = 'BODY_18'
    # if os.path.exists(output_dir):
    #     shutil.rmtree(output_dir)
    os.makedirs(output_dir,exist_ok=True)
    copyDirectory_createMat(file_dir,output_dir,body_format)
    copyDirectory_createMP4(file_dir,output_dir,mode=1)
    with open('commands.sh', 'w') as f:
        for command in commands:
            f.write(command+'\n')
    print('finished.')