# LRC FILE Crawler (실시간 가사 or 싱크 가사 다운)


벅스(BUGS MUSIC)를 통해 실시간 가사를 한꺼번에 크롤링하여 각각의 lrc파일로 만들어주는 파이썬 파일입니다.

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
1. py파일 다운받기

2. FLAC곡이 위치한 폴더에 py실행
```

#### ● 주의사항
```
1. FLAC파일에만 적용됩니다.

2. 음악파일내의 저장된 태그(아티스트명, 앨범명, 곡명)를 이용하여 LRC파일을 찾으므로 정식음원에서만 적용됩니다.

3. 아티스트가 2명 이상일 경우 검색이 되지 않거나 에러가 납니다. 예) 권진아,샘김-HONEY MOON

4. 벅스에서만 검색하므로 원하시는 lrc파일이 없을 수 있으니 양해바랍니다.
```
#### ● 코멘트
```
제가 처음 올리는 파이썬 파일이라 오류가 있을 수 있습니다. 

에러난 부분을 어떻게 하면 되는지 알려주시면 감사합니다.

추후에 벅스 검색관련 코드 개선하겠습니다.
```
