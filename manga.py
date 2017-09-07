##########################################################
# This script By : Mr Kara				                       #
# 							                                         #
#		Manga Downloader		                              	 #
#							                                           #
#			K :3				                                       #
##########################################################
import os
import sys
from urllib import urlopen
import requests
import shutil
import re
from string import punctuation as punct

# Change this to the manga you want to download (each word must start with a capital letter)

name = "Berserk"


start_chapter = int(sys.argv[1]) if len(sys.argv) > 1 else 1
end_chapter   = int(sys.argv[2]) if len(sys.argv) == 3 else sys.maxsize

if start_chapter > end_chapter:
  start_chapter, end_chapter = end_chapter, start_chapter

url = 'http://www.mangareader.net/' + (''.join(ch for ch in name if ch not in punct)).lower().replace(" ","-") + '/'

current_page = url + str(start_chapter) + '/1'

# Make the download path
if not os.path.exists(name):
  os.makedirs(name)
if not os.path.exists(name + '/' + str(start_chapter)):
  os.makedirs(name + '/' + str(start_chapter));

# Go to the website
f = urlopen(current_page)

# Downloading all images 
chapter = start_chapter
cont = True
while cont:
  # Read the HTML
  html = f.read() 

  # Find the direct URL to image
  current_page = int(re.search(b"<span class='c1'>Page (.+?)&nbsp;-&nbsp;</span>", html).group(1))
  image_url = re.search(b'src="http://(.+?).jpg" alt="' + name.encode('utf-8'), html)

  # If a direct link to the image is found, then we know the chapter has been released
  # Otherwise, we know the chapter has not been released.
  if image_url and chapter <= end_chapter:
    image_url = 'http://' + image_url.group(1).decode('utf-8') + '.jpg'

    # Download the image using the direct link
    r = requests.get(image_url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
    if r.status_code == 200:
      with open(name + '/' + str(chapter) + '/' + ("%02d"%current_page) + '.jpg', "wb") as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw,f)

    # When we reach the end of the chapter, go to the next chapter
    page_count = int(re.search(b'</select> of (.+?)</div>',html).group(1))
    if current_page == page_count:
      print("Successfully downloaded chapter " + str(chapter) + ".")

      # Make a folder to store the new chapter
      chapter = chapter + 1
      if not os.path.exists(name):
        os.makedirs(name)
      if not os.path.exists(name + '/' + str(chapter)):
        os.makedirs(name + '/' + str(chapter));

      # Start at the first page of the new chapter
      f = urlopen(url + str(chapter) + '/1')

    # Otherwise, go to the next page
    else:
      f = urlopen(url + str(chapter) + '/' + str(current_page + 1))
  else:
    cont = False
