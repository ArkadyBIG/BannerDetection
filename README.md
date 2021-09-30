# Get Started
``` bash 
docker build -t banner_detection .
```

## In Docker Container

write down twitch links to ```streams.txt``` file as:

```
https://www.twitch.tv/mata_gg
https://www.twitch.tv/fif_tesei
```
``` Can be modified during runtime```
# Run

```
python3 main.py --dump-period 3
```
```Period of saving results in minutes: 'dump-every' (default 1 minute). Set to at least 30 minutes after testing for more accurate results.``` 


# Results

### All details are saved in ```./result``` folder as:
### ```./result/{twitch_nickname}/{day}/{time}.json```

### Each json file is represented as:
``` json 
{
    "meta": {
        "total_detection_seconds": 30.04, // Detection period
        "total_detection_count": 381, // Number of detections made
        "banner_displayed_count": 20, // Number of frames where banner was found
        "banner_displayed": 0.05249343832020997, // Percent of frames on which banner is
        "fps": 12.679267706730467 // Average number of detections on this stream per second 
    },
    "key_frames": [ // List of detections
        [
            "2021-09-30 13:56:12.295576", // date when frame was streamed on twitch
            {
                "detections": [],
                "scores": []
            }
        ],
		[
            "2021-09-30 13:56:33.149157",
            {
                "detections": [ // List of detections in relative cordinates (x1, y1, x2, y2)
                    [
                        0.853515625,
                        0.1145833358168602,
                        0.990234375,
                        0.3576388955116272
                    ]
                ],
                "scores": [
                    62
                ]
            }
        ]
}
```
