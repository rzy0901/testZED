### Record `.svo`

``` 
python3 camera_control_record.py
```

### Post Processing

Play 3-d skeletons from `.svo`.

```
python3 body_tracking_real_time_svo.py ./test.svo
```

Export 3-d skeletons to `.mat` from local recorded `.svo`.

```
python3 svo_skeletons.py
```

Export `.svo` to `.mp4` videos.

```
python3 svo_export.py ./test.svo ./videos/left_right.mp4 0
python3 svo_export.py ./test.svo ./videos/left_rightdepth.mp4 1
```



