# Openu download
* dont expect this script to work forever, if the univirsity change their site it might well break
* the scrip origanly was designed for linux, it will work on Windows (probaly) but there could be problems.
## Requiements:
* Python
* ffmpeg

both can be downloaded from the internet.

# how to use:
1. go to the course you want to download from and press F12 to open dev tool.
   ![image](https://github.com/user-attachments/assets/e4af24f2-2129-4b54-8c5b-d54d834432be)
2. press the video you want to download and pasue it.
   ![image](https://github.com/user-attachments/assets/f4031ea9-f232-4b17-b12e-f94fa7e40126)
we looking for two files:
one: vtt.php, we will copy the content of the response and paste it in the chapters.vtt file in our script
![image](https://github.com/user-attachments/assets/3d8e106f-4ec7-4589-b484-07d5cb0179b2)
![image](https://github.com/user-attachments/assets/f10e86c8-f3e6-43d4-9f99-618586e16d03)
two: chunklist_b.....  we want to copy the url of the request and past it in the chunklistUrl verible.
![image](https://github.com/user-attachments/assets/e4f85c70-f0a0-422a-bb90-27e748a51d21)
![image](https://github.com/user-attachments/assets/9f0a4b88-bda6-4f7a-afb3-a4f0a8ea8299)
3. name the video how you wish and write in console "python run_streaming.py" and enjoy

# downloading ffmpeg on windows.
while i could write the code to use diffrent lib in windows(not gonna happen), the best way to download ffmpeg is to just do "winget install ffmpeg" in powershell
![image](https://github.com/user-attachments/assets/602db12d-342b-4c7b-89c2-32c6311b1ac8)
