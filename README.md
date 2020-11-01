# CCTV-py
CCTV Program in python made for raspberry pi

# How did this project come about?
1. Want to have a CCTV to monitor our front door 
1. But CCTVs are very pricey
1. We have an old RaspPi lying around unused
1. We have a NAS server that can run python scripts


# Goal
Make the raspberry pi run the client script to send frames to the server to store the video files in the NAS

# Architecture
Rasp Pi --sends frames to --> Nas server (Which stores the file)
NAS and RaspPi will be on the same LAN
