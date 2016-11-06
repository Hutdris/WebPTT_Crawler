#函數說明@main.py
##webptt_title_crawler：
    給定版名，指定抓取文章數，推文下限後，會從最新的文章向後尋找符合的標題，最後回傳符合的文章url list。

##photo_crawler:
    給定文章url，指定的根目錄，會在根目錄下以文章標題建立資料夾，並依序編號抓取圖片存入，並將文章資訊存成info.txt。
    PS:符合條件的文章內未必有照片，而沒有照片的文章不會生成資料夾。

##crawler:
    結合webptt_title_crwaler, photo_crawler，實現批次抓取。

#預計功能
1. 增加webptt_title_crwaler搜尋的條件(符合的標題，以re實現)。
2. 針對拍賣版面的資料探勘：
    ex:在手機拍賣版(MobileComm)尋找所有LG V20的價格，依照買/賣/時間軸/賣家並輸出。

#如果有時間的預計功能
1. 用telnet來改寫webptt_title_crawler，因為web版搜尋就要把所有文章掃過一次，很麻煩。
2. 用PyQt增加GUI界面。