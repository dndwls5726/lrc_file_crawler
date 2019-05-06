import glob
import mutagen
import requests
from bs4 import BeautifulSoup
import os
import urllib
import json

FILE_LIST = []
available_file = []
available_artist = []
available_first_artist = []
available_second_artist = []
available_album = []
available_title = []
track_artistid = []
track_albumid = []
track_trackid = []
TIME = []
LYRICS = []
mm = []
ss = []
xx = []
success = 0
fail = 0


def track_clear():
    track_albumid.clear()
    track_artistid.clear()
    track_trackid.clear()


def time_clear():
    xx.clear()
    ss.clear()
    mm.clear()
    LYRICS.clear()
    TIME.clear()


def lrc_maker():
    global success
    global data
    global i
    global available_file
    TEXT = data['result']['lyrics']
    TEXT = TEXT.replace("＃", "\n")
    x = TEXT.count("|")
    with open('%s.lrc' % available_file[i].replace(".flac", ""), 'w', encoding='UTF8') as file:  # 덮어씌우기
        file.write(TEXT)
    del TEXT
    TEXT = []
    with open('%s.lrc' % available_file[i].replace(".flac", ""), 'r', encoding='UTF8') as file:  # 한줄씩 읽어오기
        for j in range(0, x):
            TEXT.append(file.readline().rstrip())
    for j in range(0, x):  # 시간과 가사 구분하기
        TIME.append(float(TEXT[j][:TEXT[j].rfind("|")]))
        LYRICS.append(TEXT[j][TEXT[j].rfind("|") + 1:])
    for j in range(0, x):
        xx.append(str(round(TIME[j] - int(TIME[j]), 2)))
        if int(TIME[j]) % 60 < 10:
            ss.append("0" + str(int(TIME[j]) % 60))
        else:
            ss.append(str(int(TIME[j]) % 60))
        if int(TIME[j]) // 60 < 10:
            mm.append("0" + str(int(TIME[j]) // 60))
        else:
            mm.append(str(int(TIME[j]) // 60))
    with open('%s.lrc' % available_file[i].replace(".flac", ""), 'w', encoding='UTF8') as file:  # 초기화
        file.write('')
    for j in range(0, x):
        with open('%s.lrc' % available_file[i].replace(".flac", ""), 'a', encoding='UTF8') as file:  # 최종
            if j != x:
                file.write("[" + mm[j] + ":" + ss[j] + xx[j][1:] + "]" + LYRICS[j] + "\n")
            else:
                file.write("[" + mm[j] + ":" + ss[j] + xx[j][1:] + "]" + LYRICS[j])
    time_clear()
    track_clear()
    del TEXT
    print("%s. %s의 lrc파일을 가져왔습니다." % (i, available_file[i]))
    success += 1
    return success


def lrc_delete():
    global fail
    global i
    global available_file
    fail += 1
    track_clear()
    os.remove('%s.lrc' % available_file[i].replace(".flac", ""))
    print("%s 은(는) 싱크가사를 지원하지 않습니다." % available_file[i])
    return fail


for file in glob.glob("*.flac"):  # flac파일 개수 파악
    FILE_LIST.append(file)

if len(FILE_LIST) != 0:  # FLAC 곡이 있는지 확인하기
    for i in range(0, len(FILE_LIST)):
        if 'album' in mutagen.File("%s" % FILE_LIST[i]).keys() and 'artist' in mutagen.File("%s" % FILE_LIST[i]).keys() and 'title' in mutagen.File("%s" % FILE_LIST[i]).keys():  # 아티스트, 앨범, 타이틀 태그 있는지 확인
            FILE_TAG_LIST = mutagen.File("%s" % FILE_LIST[i])
            available_file.append(FILE_LIST[i])
            available_album.append(FILE_TAG_LIST['album'][0])
            available_title.append(FILE_TAG_LIST['title'][0])
            available_artist.append(FILE_TAG_LIST['artist'][0])
            if "," in FILE_TAG_LIST['artist'][0]:
                available_first_artist.append(FILE_TAG_LIST['artist'][0][:FILE_TAG_LIST['artist'][0].find(",")])
                available_second_artist.append(FILE_TAG_LIST['artist'][0][FILE_TAG_LIST['artist'][0].rfind(",")+1:])
            else:
                available_first_artist.append(FILE_TAG_LIST['artist'][0])
                available_second_artist.append('')
        else:
            print("%s의 태그가 없습니다." % FILE_LIST[i])
            fail += 1

    for i in range(0, len(available_file)):
        if available_second_artist[i] == '':
            soup_artist = BeautifulSoup(requests.get('https://music.bugs.co.kr/search/artist?q=%s' % available_artist[i]).text, 'html.parser')
        else:
            soup_first_artist = BeautifulSoup(requests.get('https://music.bugs.co.kr/search/artist?q=%s' % available_first_artist[i]).text,'html.parser')
            soup_second_artist = BeautifulSoup(requests.get('https://music.bugs.co.kr/search/artist?q=%s' % available_second_artist[i]).text,'html.parser')
        soup_album = BeautifulSoup(requests.get('https://music.bugs.co.kr/search/album?q=%s %s' % (available_artist[i], available_album[i])).text,'html.parser')
        soup_track = BeautifulSoup(requests.get('https://music.bugs.co.kr/search/track?q=%s %s' % (available_artist[i], available_title[i])).text,'html.parser')

        if available_second_artist[i] == '':
            if soup_artist.select('#container > section > div > ul > li:nth-of-type(1) > figure > figcaption > a.artistTitle'):
                for id in soup_artist.select('#container > section > div > ul > li:nth-of-type(1) > figure > figcaption > a.artistTitle'):  # 아티스트 결과
                    artist_artistid = id['href'][32:-25]
            else:
                print("%s에 대한 검색 결과가 없습니다." % available_file[i])
                fail += 1
                continue
        else:
            if soup_first_artist.select('#container > section > div > ul > li:nth-of-type(1) > figure > figcaption > a.artistTitle'):
                for id in soup_first_artist.select('#container > section > div > ul > li:nth-of-type(1) > figure > figcaption > a.artistTitle'):  # 아티스트 결과
                    artist_first_artistid = id['href'][32:-25]
            else:
                print("%s에 대한 검색 결과가 없습니다." % available_file[i])
                fail += 1
                continue
            if soup_second_artist.select('#container > section > div > ul > li:nth-of-type(1) > figure > figcaption > a.artistTitle'):
                for id in soup_second_artist.select('#container > section > div > ul > li:nth-of-type(1) > figure > figcaption > a.artistTitle'):  # 아티스트 결과
                    artist_second_artistid = id['href'][32:-25]
            else:
                print("%s에 대한 검색 결과가 없습니다." % available_file[i])
                fail += 1
                continue

        if soup_album.select('#container > section > div > ul > li:nth-of-type(1) > figure'):
            for id in soup_album.select('#container > section > div > ul > li:nth-of-type(1) > figure'):  # 앨범검색 결과
                album_artistid = id['artistid']
                album_albumid = id['albumid']
        else:
            print("%s에 대한 검색 결과가 없습니다."%available_file[i])
            fail += 1
            continue

        for id in soup_track.find_all("tr"):
            if id.get('artistid'):
                track_artistid.append(id.get('artistid'))
            if id.get('albumid'):
                track_albumid.append(id.get('albumid'))
            if id.get('trackid'):
                track_trackid.append(id.get('trackid'))

        if available_second_artist[i] == '':
            if artist_artistid == album_artistid and artist_artistid in track_artistid:
                n = track_artistid.index(artist_artistid)
                urllib.request.urlretrieve('http://api.bugs.co.kr/3/tracks/%s/lyrics?&api_key=b2de0fbe3380408bace96a5d1a76f800' % track_trackid[n],"%s.lrc" % available_file[i].replace(".flac", ""))
                with open('%s.lrc' % available_file[i].replace(".flac", ""), encoding='UTF8') as json_file:
                    data = json.load(json_file)
                if data['result'] is not None:  # 싱크 가사 있을 때,
                    if "|" in data['result']['lyrics']:  # time이 있을 때,
                        lrc_maker()
                    else:  # time이 없을 때,
                        lrc_delete()
                else:  # 싱크 가사 없을 때,
                    lrc_delete()
            else:
                print("%s에 대한 검색 결과가 없습니다." % available_file[i])
                fail += 1
                track_clear()
        else:
            if artist_first_artistid == album_artistid and artist_second_artistid in track_artistid:
                n = track_artistid.index(artist_second_artistid)
                urllib.request.urlretrieve('http://api.bugs.co.kr/3/tracks/%s/lyrics?&api_key=b2de0fbe3380408bace96a5d1a76f800' % track_trackid[n],"%s.lrc" % available_file[i].replace(".flac", ""))
                with open('%s.lrc' % available_file[i].replace(".flac", ""), encoding='UTF8') as json_file:
                    data = json.load(json_file)
                if data['result'] is not None:  # 싱크 가사 있을 때,
                    if "|" in data['result']['lyrics']:  # time이 있을 때,
                        lrc_maker()
                    else:  # time이 없을 때,
                        lrc_delete()
                else:  # 싱크 가사 없을 때,
                    lrc_delete()
            elif artist_first_artistid == album_artistid and artist_first_artistid in track_artistid:
                n = track_artistid.index(artist_first_artistid)
                urllib.request.urlretrieve('http://api.bugs.co.kr/3/tracks/%s/lyrics?&api_key=b2de0fbe3380408bace96a5d1a76f800' % track_trackid[n],"%s.lrc" % available_file[i].replace(".flac", ""))
                with open('%s.lrc' % available_file[i].replace(".flac", ""), encoding='UTF8') as json_file:
                    data = json.load(json_file)
                if data['result'] is not None:  # 싱크 가사 있을 때,
                    if "|" in data['result']['lyrics']:  # time이 있을 때,
                        lrc_maker()
                    else:  # time이 없을 때,
                        lrc_delete()
                else:  # 싱크 가사 없을 때,
                    lrc_delete()
            else:
                print("%s에 대한 검색 결과가 없습니다." % available_file[i])
                fail += 1
                track_clear()

    if i == len(available_file)-1:
        print("============완료============")
        print("가져온 lrc파일 수 : %s 개"% success)
        print("실패한 곡 수 : %s 개"% fail)
        print("============================")

else:  # flac파일이 없을 때
    print("==========ERROR===========")
    print("FLAC파일을 찾을 수 없습니다.")
    print("==========================")
