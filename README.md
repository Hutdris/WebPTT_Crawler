# 函數說明 
## webptt_title_crawler：
給定版名，關鍵字，搜尋深度後，會從最新的文章向後尋找符合的標題，最後回傳符合的文章url list。
```python
from WebPTT_Photo_Crawler.pttcrawler import webptt_title_crawler
# 在nb-shopping版，找標題包含"pro"(區分大小寫)的文章，從最新一頁往後找80頁，回傳符合的urls
urls = webptt_title_crawler(board_name="nb-shopping", title_keywords='pro', search_depth=100)
```
## price_extrater:
會在給定的網址中解析符合pattern的字句，再把數字部分解析出來，回傳一個list=[(price0, title0, url0), ...]
```python
from WebPTT_Photo_Crawler.pttcrawler import price_extrater
# urls = webptt_tile_crawler(...)
report = price_extrater(urls, price_patten=r"""交易價格[：:].*\d*[.,]*\d{3,}""") #這是nb-shopping的pattern
# 附送一個macshop版的pattern =  "\[交易價格\]：\d*.*\d\b"
```
## report2csv:
把得到的report轉成csv
```python
# report = price_extrater(...)
report2csv(report, path='./report.csv')
```
## photo_crawler:
給定文章url，指定的根目錄，會在根目錄下以文章標題建立資料夾，並依序編號抓取圖片存入，並將文章資訊存成info.txt。
PS:符合條件的文章內未必有照片，而沒有照片的文章不會生成資料夾。

## crawler:
結合webptt_title_crwaler, photo_crawler，實現批次抓取。


# 結論
1. 抓資料很快，但維護資料很麻煩.之後希望新增管理抓下來的urls，或是能記憶每次抓的urls，不要重複抓。
1. webptt_title_crawler還很陽春:目前title關鍵字只能一個，且區分大小寫。
1. 新增的title_crawler/price_extrater幾乎沒有作例外處理，有需要的請自行調校。目前只有在macshop/nb-shopping測試過。
1. 剛爬下來的編碼不是utf8，想修改的要注意。
1. 下次更新應該就是又要敗家的時候了吧(誤)


# ~~如果有時間的預計功能~~
~~1. 用telnet來改寫webptt_title_crawler，因為web版搜尋就要把所有文章掃過一次，很麻煩。~~
~~2. 用PyQt增加GUI界面。~~
