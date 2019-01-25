### Samepl 1: RTP (local)
## Sender Command
# ./sample_camera.py \
# 	--without-preview \
# 	--stdout \
# 	-w 640 \
# 	-h 360 | \
# ffmpeg \
# 	-f rawvideo -pixel_format bgr24 -video_size 640x360 -i - \
# 	-c:v libx264 -pix_fmt yuv420p -r 10 -g 60 -b:v 2500k \
# 	-f rtp rtp://localhost:8080 -sdp_file stream.sdp
#
## Recevier Command
# ffplay -protocol_whitelist "file,udp,rtp" stream.sdp


### Sample 2 : RTMP (YouTube Live) ()
# ./sample_camera.py \
# 	--without-preview --stdout -r 30 -w 1280 -h 720 | \
# ffmpeg \
# 	-f rawvideo -pix_fmt bgr24 -r 30 -s 1280x720 -i - \
# 	-c:v libx264 -preset veryfast -maxrate 1984k -bufsize 3968k \
#   -vf "format=yuv420p" -g 60 \
# 	-f flv rtmp://a.rtmp.youtube.com/live2/dcfv-xfz4-5v1m-9ybx
### https://trac.ffmpeg.org/wiki/Encode/YouTube
### https://stackoverflow.com/questions/43586435/ffmpeg-to-youtube-live

### Sample 3: Show an exported video frame using ffplay
# ./sample_camera.py -o test.mp4 \
# 	--without-preview --stdout -w 640 -h 360 | \
# ffplay \
# 	-f rawvideo -pix_fmt bgr24 -s 640x360 -i -


### Sample 4: Export mp4 with ffmpeg
# ./sample_camera.py \
# 	--without-preview --stdout -w 640 -h 360 | \
# ffmpeg \
# 	-f rawvideo -pix_fmt bgr24 -s 640x360 -i - \
# 	-c:v libx264 -pix_fmt yuv420p -r 30 -g 60 -b:v 2500k \
# 	export.mp4
