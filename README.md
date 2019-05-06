# LRC FILE Crawler (실시간 가사 or 싱크 가사 다운)

벅스(BUGS MUSIC)를 통해 실시간 가사를 한꺼번에 크롤링하여 각각의 lrc파일로 만들어주는 파이썬 파일입니다.

안드로이드 오레오 삼성뮤직에서 정상적으로 적용됩니다.

<img src="https://user-images.githubusercontent.com/44944839/48315668-8898fb00-e61c-11e8-8804-3c21c558be00.jpg" width="300px"></img>

#### ● 필수 install 모음
```
import glob
import mutagen
import requests
from bs4 import BeautifulSoup
import os
import urllib
import json
```
#### ● 사용방법
```
1. py파일을 FLAC곡이 위치한 폴더로 다운받기

2-1. 명령 프롬프트에서 python lrc_parsing(FLAC).py 입력하여 실행 또는

2-2. 파이참과 같은 에디터에서 실행
```

#### ● 유의사항
```
1. FLAC파일에만 적용됩니다.

2. 음악파일내의 저장된 태그(아티스트명, 앨범명, 곡명)를 이용하여 LRC파일을 찾으므로 정식음원에서만 적용됩니다.

3. 복면가왕과 같은 아티스트 명이 바뀌는 경우 검색이 되질 않을 수 있습니다.

4. 벅스에서만 검색하므로 원하시는 lrc파일이 없을 수 있으니 양해바랍니다.

5. api key값이 변동되는 경우가 있어서 안되는 경우가 있습니다.
```
#### ● 코멘트
```
제가 처음 올리는 파이썬 파일이라 오류가 있을 수 있습니다. 

추후에 벅스 검색관련 코드 개선하겠습니다.
```
