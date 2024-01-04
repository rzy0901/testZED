# testZED

## Introduction
+ Using a ZED 2i to convert `.svo` file to 3d skeletons.

+ [ZED SDK](https://www.stereolabs.com/developers/release/) should be installed.
  + ZED SDK 4.0.8 is used in this repository.
  + [Blog post](https://rzy0901.github.io/post/zed/) for my notes.

+ Screenshots:

<table>
	<tbody>
		<tr>
			<td><img src="https://user-images.githubusercontent.com/66763689/197104509-e7c63ab2-8b38-4d8f-ba0e-24e48e9878c6.png" alt="image" width="1300px;" /></td>
			<td><img src="https://rzy0901.github.io/zed.assets/test2.gif" alt="image;" /></td>
		</tr>
	</tbody>
</table>

<!-- <table>
	<tbody>
		<tr>
			<td>walk1</td>
			<td>walk2</td>
			<td>run1</td>
			<td>run2</td>
			<td>squat</td>
		</tr>
		<tr>
			<td><img src="https://github.com/rzy0901/testZED/blob/main/README.assets/walk1.gif" alt="image";" /></td>
			<td><img src="https://github.com/rzy0901/testZED/blob/main/README.assets/walk2.gif" alt="image";" /></td>
			<td><img src="https://github.com/rzy0901/testZED/blob/main/README.assets/run1.gif" alt="image";" /></td>
			<td><img src="https://github.com/rzy0901/testZED/blob/main/README.assets/run2.gif" alt="image";" /></td>
			<td><img src="https://github.com/rzy0901/testZED/blob/main/README.assets/squat.gif" alt="image";" /></td>
		</tr>
	</tbody>
</table> -->

## Usage

### Record `.svo`

``` 
python3 camera_control_record.py
```

### Post Processing

Play 3-d skeletons from `.svo`:

```
python3 body_tracking_real_time_svo.py ./test.svo
```

Export 3-d skeletons to `.mat` from local recorded `.svo`:

```
python3 svo_skeletons.py -i <input_svo_path> -o <output_mat_path> -b <body_format>
```

```
❯ python3 svo_skeletons.py -h

usage: svo_skeletons.py [-h] [-i INPUT_SVO_PATH] [-o OUTPUT_MAT_PATH] [-b BODY_FORMAT]

Convert svo to mat.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_SVO_PATH, --input_svo_path INPUT_SVO_PATH
                        Input svo path, default:./test.svo
  -o OUTPUT_MAT_PATH, --output_mat_path OUTPUT_MAT_PATH
                        Output: mat path, default:./data/temp.mat
  -b BODY_FORMAT, --body_format BODY_FORMAT
                        Capatured body format, available selections: BODY_18, BODY_34, BODY_38; default:BODY_18
```

Export `.svo` to `.mp4` videos:

```
python3 svo_export.py ./test.svo ./videos/left_right.mp4 0
python3 svo_export.py ./test.svo ./videos/left_rightdepth.mp4 1
```





## Acknowledgement: 
Thanks to [Li-baster](https://github.com/QianrenLi) for acting as a model for the recording of the video.
