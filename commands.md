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



