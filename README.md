# virus-game


The main code for the virus game is in virus_sim.py

To convert ./points/all_points to a mp4-file use:

ffmpeg -framerate 3 -i "./points/all_points%d.png"   -c:v libx264 -r 30 -pix_fmt yuv420p virus.mp4
