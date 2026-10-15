"""Put the cover image in as frame 0 of an already-rendered reel (audio delayed by one frame to stay in sync).
python3 add_cover_frame.py ../reels/Reel03_x.mp4 ../reels/Reel03_Cover.jpg"""
import subprocess, sys, os, shutil, tempfile
mp4, cover = sys.argv[1], sys.argv[2]
tmp = tempfile.mktemp(suffix='.mp4')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', '30', '-t', str(1 / 30), '-i', cover, '-i', mp4,
                '-filter_complex', '[0:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p[c];[1:v]fps=30,format=yuv420p[m];[c][m]concat=n=2:v=1:a=0[v];'
                '[1:a]adelay=33.333:all=1[a]', '-map', '[v]', '-map', '[a]',
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-movflags', '+faststart',
                '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', tmp], check=True)
shutil.move(tmp, mp4)
print('ok', mp4)
