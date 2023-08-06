from threading import Thread
import os

'''
URL of the archive web-page which provides link to
all video lectures. It would have been tiring to
download each video manually.
In this example, we first crawl the webpage to extract
all the links and then download videos.
'''

def download_files(links: list) -> None:
    for link in links:
        '''iterate through all links in links list and download them asynchronously'''
        Thread(target=download, args=(link,)).start()
        


def download(link : str) -> None:
    filename = link.split("/")[-1]

    print(f'Downloading file :: {link} ..... \n')
    os.system(rf'curl {link} --output {filename}')
    print(f'Downloading finished :: {link} .....\n')


if __name__ == "__main__":
    
    download_files(['https://sadiqhasan.com/Seerat%20Rasool%20P.B.U.H-02/seerat101.mp3'])
	

	
