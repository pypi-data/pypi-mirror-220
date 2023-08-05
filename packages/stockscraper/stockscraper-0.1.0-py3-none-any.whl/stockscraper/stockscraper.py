'''Author: Pallav'''

#Importing Modules
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

class FetchStocks:
    def Load(self,array,filename="Default"):
        with open(filename+".txt") as fr:
            for line in tqdm(fr,desc="Loading"):
                array.append((line.strip()))
    def Store(self,array,filename="Default"):
        with open((filename+'.txt'),'w') as fw:
            for r in tqdm(range (0,len(array)), desc=("Storing....")):
                fw.write(array[r]+"\n")
    def __init__(self,stockname,stinfo):
        print("Stay Back, This Process can take upto Several Minutes")
        #Getting StockInfo : 
        for i in tqdm (range (1,2), desc="Fetching Stocks"):
            url = "https://www.screener.in/screens/71064/all-stocks/?page=" + str(i)
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser') #Making a SOUP!
            #Scraping Stock Names
            names = soup.find_all("a",target="_blank")
            #To Get List of Names of Stock
            for name in names:
                stockname.append(name.string.strip())
            # To get Particular link for each Stock
            for a in soup.find_all('a', href=True, target="_blank"):
                stinfo.append(a['href'])
            time.sleep(0.5)

        self.Store(stockname,"Stockname")
        self.Store(stinfo,"StockLink")
        return stockname,stinfo

class FetchStockData:

    def Load(self,array,filename="Default"):
        with open(filename+".txt") as fr:
            for line in tqdm(fr,desc="Loading"):
                array.append((line.strip()))

    def Store(self,array,filename="Default"):
        with open((filename+'.txt'),'w') as fw:
            for r in tqdm(range (0,len(array)), desc=("Storing....")):
                fw.write(array[r]+"\n")

    def __init__(self,stinfo):
        #To Get Ratios and Ratio Values!
        global Rvalue,Rname
        Rname=[]
        Rvalue=[]
        if not stinfo:
            self.Load(stinfo,"StockLink")

        print("This Process can take upto", str((len(stinfo)*0.6)/60) + " Minutes")
        #Temp. Sorting    
        #Visiting Every Stock Page Individually
        for q in tqdm (range (0, len(stinfo)), desc="Fetching Stocks' Data!!..."):
            Newurl = "https://www.screener.in" + str(stinfo[q]) 
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            r = requests.get(Newurl, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')

            #To Get all the Ratios 
            RatioName = soup.find_all("span",class_="name")
            RatioValue = soup.find_all("span",class_="number")
            for t in range(0,len(RatioName)):
                if t != 2:
                    Rname.append(RatioName[t].string.strip())
            for t in range(0,len(RatioValue)):
                if t != 2 and t!=3:
                    if (RatioValue[t].string) == None:
                            Rvalue.append('0.0')
                    else:
                            Rvalue.append(RatioValue[t].string)
            
            time.sleep(0.5)

    def GetRatios(self,MarketCap,CurrentPrice,StockPE,BookValue,DividendYield,ROCE,ROE,FaceValue):
        global Rvalue, Rname
        #Making Temp Arrays
        TempCap = []
        TempCurrentPrice =[]
        TempFaceValue = []
        TempStockPE =[]
        TempBookValue=[]
        TempDividendYield=[]
        TempROCE=[]
        TempROE=[]    

        StoreArrays = [TempCap,TempCurrentPrice,TempFaceValue,TempStockPE,TempBookValue,TempDividendYield,TempROCE,TempROE]
        #To Seprate Ratios from a comman Array[RatioValue]
        for m in range(0,len(Rvalue),8):
            TempCap.append(Rvalue[m])
            TempCurrentPrice.append(Rvalue[m+1])
            TempStockPE.append(Rvalue[m+2])
            TempBookValue.append(Rvalue[m+3])
            TempDividendYield.append(Rvalue[m+4])
            TempROCE.append(Rvalue[m+5])
            TempROE.append(Rvalue[m+6])
            TempFaceValue.append(Rvalue[m+7])

        #To Remove Commas:
        for n in range(0,int(len(Rvalue)/8)):
            temp = str(TempCap[n].replace(",",""))
            MarketCap.append(float(temp))
            temp = str(TempCurrentPrice[n].replace(",",""))
            CurrentPrice.append(float(temp))
            temp = str(TempStockPE[n].replace(",",""))
            StockPE.append(float(temp))
            temp = str(TempBookValue[n].replace(",",""))
            BookValue.append(float(temp))
            temp = str(TempDividendYield[n].replace(",",""))
            DividendYield.append(float(temp))
            temp = str(TempROCE[n].replace(",",""))
            ROCE.append(float(temp))
            temp = str(TempROE[n].replace(",",""))
            ROE.append(float(temp))
            temp = str(TempFaceValue[n].replace(",",""))
            FaceValue.append(float(temp))
        
        #Clearing Temp Arrays 
        for i in range(0,len(StoreArrays)):
            StoreArrays[i].clear()
        
        return MarketCap,CurrentPrice,StockPE,BookValue,DividendYield,ROCE,ROE,FaceValue

    def ExportRatios(self,stockname,MarketCap,CurrentPrice,StockPE,BookValue,DividendYield,ROCE,ROE,FaceValue):

        #To Store in a File
        StoreRatios =[]
        for r in tqdm (range (0,len(stockname)), desc="Exporint To File..."):
            StoreRatios.append(str("StockName: "+str(stockname[r])+"\n \t"+
                            "MarketCap"+str(MarketCap[r])+'\n \t'+
                            'CurrentPrice'+str(CurrentPrice[r])+'\n \t'+
                            'StockPE'+str(StockPE[r])+'\n \t'+
                            'BookValue'+str(BookValue[r])+'\n \t'+
                            'DividendYield'+str(DividendYield[r])+'\n \t'+
                            'RCOE'+str(ROCE[r])+'\n \t'+
                            'ROE'+str(ROE[r])+'\n \t'+
                            'FaceValue'+str(FaceValue[r])+'\n \n \n'))
        
        self.Store(StoreRatios,"Ratios")

