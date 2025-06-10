import urllib.request
import os
import threading
import math
import shutil
import re
import time

def extract_ts(m3, base):
    lines = m3.readlines()
    urls = []
    for line in lines:
        if '.ts' in line:
            urls.append(base+line.split('\n')[0])
    return urls

def download_ts_files(start, end, urls, tstemps):
        for ts in range(start, end):
            urllib.request.urlretrieve(urls[ts], f"{tstemps}/media{ts}")
        print(f"thread {threading.current_thread().name} finished")

def convert_ts_to_mp4(ts_path, tempdir, output):
    with open(f"{tempdir}/input_list", "w") as f:
        for ts in ts_path:
            f.write(f"file ../'{ts}'\n")
    return os.system(f'ffmpeg -f concat -safe false -i {tempdir}/input_list -i {tempdir}/FFMETADATAFILE -map_metadata 1 -c copy "{output}"')

def workers_threads(thread_num, tsurls, tstemps):
    urls_num = len(tsurls)
    delta = math.floor(urls_num / thread_num)
    start = 0
    end = delta
    threads = []
    for worker in range(thread_num):
        thread = threading.Thread(target=download_ts_files, args=(start,end, tsurls, tstemps), name=f"Thread-{worker}")
        threads.append(thread)
        thread.start()
        start = end
        if worker == thread_num - 2:
            end = urls_num
        else:
            end = end + delta
    for thread in threads:
        thread.join()

def import_chapters(temp_folder, chapters):
    text = ";FFMETADATA1\n"
    with open(chapters, 'r') as f:
        in_chapter = False
        chapter_line = 0
        start_time = []
        end_time = []
        for line in f:
            ch_title = re.match(r"(C|c)hapter", line)
            if bool(ch_title):
                in_chapter = True
                chapter_line = 1
                continue
            if ch_title or in_chapter:
                if chapter_line == 1:
                    x = re.findall(r"(\d*:\d{2}:\d{2}.\d*)", line)
                    start = re.findall(r"(\d{2})",x[0])
                    end = re.findall(r"(\d{2})",x[1])
                    for num in start:
                        start_time.append(int(num))
                    for num in end:
                        end_time.append(int(num))
                    chapter_line = 2
                    continue
                title = line
                start = ((((start_time[0]*60)+start_time[1])*60)+start_time[2])*1000
                end =  ((((end_time[0]*60)+end_time[1])*60)+end_time[2])*1000
                text_appen = f"""
[CHAPTER]
TIMEBASE=1/1000
START={start}
END={end}
title={title}
"""
                text += text_appen
                chapter_line = 0
                in_chapter = False
                start_time = []
                end_time = []
    with open(f"{temp_folder}/FFMETADATAFILE", "a") as myfile:
        myfile.write(text)

def main():
    chunklistUrl = "https://souvod.bynetcdn.com/vod/smil:vod/openu/PRV5/xLd9gbRknz/App/xLd9gbRknz_10.smil/chunklist_b1800000.m3u8?md5=c0aIRCzUVi3YO2u7cblUDA&expires=1749638977"
    vidname = 'מפגש 9 - גוף קשיח'
    thread_num = 8
    tstemps = f"temp{math.floor(time.time())}"
    chaptersUri = "chapters.vtt"

    os.mkdir(tstemps)

    basestr = chunklistUrl[0:chunklistUrl.find("chunklist")]
    chunklist = open(urllib.request.urlretrieve(chunklistUrl, f"{tstemps}/chunklist.m3u8")[0])

    import_chapters(tstemps, chaptersUri)
    tsurls = extract_ts(chunklist, basestr)
    workers_threads(thread_num, tsurls, tstemps)

    tslocations = []
    for i in range(len(tsurls)):
        tslocations.append(f"{tstemps}/media{i}")
    
    vid_name = f"{vidname}.mp4"
    ok = convert_ts_to_mp4(tslocations, tstemps, f'{vid_name}')
    if ok == 0:
        shutil.rmtree(f"{tstemps}/")
    
main()