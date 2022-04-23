# 伊莉小說小載器 / eyny novel downloader
## 執行畫面
![](https://imgur.com/XNNDDES.jpg)

## 執行檔

## 使用方法
1. 準備<code>cookie.txt</code>
   1. 登錄eyny
   2. 到要下載的小說頁面按<code>F12</code>，選取網路頁籤
   3. 重整頁面，點選類似<code>thread-8899321-9-1.html</code>的名稱
   4. 右方標頭拉到最下方複製Cookie後的所有文字，存到cookie.txt中，並放到跟main.exe同一個資料夾
  
![](https://i.imgur.com/hHa1jtW.jpg)

2. 執行<code>main.exe 小說編號</code>
   1. 小說編號為網址thread後的幾碼數字，例：http://www2.eyny.com/thread-8899321-1-1.html 的編號為<code>8899321</code>
   2. 開啟cmd，移動到<code>main.exe</code>的資料夾後，執行```main.exe 小說編號```，例：```main.exe 8899321```

![](https://imgur.com/EAcH4HP.jpg)

![](https://imgur.com/fPJ3UHB.jpg)


## 資訊安全
爬蟲資料是透過cookie.txt所存cookie登入eyny後獲取，全程僅在本機執行。

## License
MIT License