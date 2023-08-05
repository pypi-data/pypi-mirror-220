# -*- encoding:utf-8 -*-
import re
import os
import sys
import pandas as pd
import numpy as np
import chardet  #字符判断
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from queue import Queue
from  datetime import datetime

import xlwings as xw

def sjgsh():
    return str(datetime.now().strftime("%Y%m%d%H%M%S"))

#整理银行类
class YH(object):
    def __init__(self):
        pass
   
    def gsjr(self,p1):
        """p1:路径，因pandas写入公式，写入后读不出来，需手动打开一次，所以加这个公式"""
        VISABLE=False#是否可视化，否
        app=xw.App(visible=VISABLE,add_book=False)#界面设置
        app.display_alerts=VISABLE#关闭提示信息
        app.screen_updating=VISABLE#关闭显示更新
        wb=app.books.open(p1)#隐藏连接当前路径下的工作簿
        wb.save(p1)
        wb.close()
        return p1
    def csv_to_xlsx(self,p1):
        data=pd.read_csv(p1,encoding='gbk',index_col=False,error_bad_lines=False,dtype = 'str')
        lsp=p1+".xlsx"
        data.to_excel(lsp,index=False)
        p1=lsp
        return p1
    def txt_to_xlsx(self,p1):
        try:
            # 总列表内容
            txtlb = []
            fa = open(p1, 'rb')
            #判断编码
            encoding_message = chardet.detect(fa.read())
            fa.close()
            print(encoding_message)
            fb=open(p1,"r",encoding=encoding_message['encoding'])  # 循环遍历对每一个文件内的数据
            shu=0
            for line in fb:                
                line=ILLEGAL_CHARACTERS_RE.sub(r'错',line)
                #line='=IF(C1=C2,IF(H2*1=H1+G2*1,"贷增","借减"),"贷增") '+line
                if shu==0:
                    line='借贷 {}'.format(line)
                else:                    
                    line='=IF(b{0}=b{1},IF(g{1}*1=g{0}+f{1}*1,"贷增","借减"),"贷增") {2}'.format(shu,shu+1,line)
                hs=re.split(r"[ ]+",line.strip("\n"))  # 将数据每次按行写入f打开的文件中
                yhl=[]
                [yhl.append(hs[i]) for i in range(len(hs)) if hs[i] not in yhl or i>2]  
                if "日期时间" in yhl:
                    yhl[0]="借贷"
                    yhl[3]="日期"
                    yhl.append("备注")
                    yhl.insert(4,"时间")                        
                txtlb.append(yhl)
                shu+=1
            fb.close()
            txtlbs=pd.DataFrame(txtlb)
            lsp=p1+".xlsx"
            txtlbs.to_excel(lsp,header=None,index=False)
            p1=self.gsjr(lsp)
            return p1
        except:
            fb.close()
            print("这个{}行错误：{}".format(shu,line))            
            raise
            #return  
    
        
        
            
           

    def dlj(self,p1=None):
        """
        #1打开文件路径p1:路径
        return 路径，工作表
        """
        if p1==None:
            return 
        if p1.endswith(".csv"):
            p1=self.csv_to_xlsx(p1)
        if p1.endswith(".txt") or p1.endswith(".TXT"):
            p1=self.txt_to_xlsx(p1) 
        if p1.endswith(".xls") or p1.endswith(".xlsx") or p1.endswith(".et"):            
            xls=pd.ExcelFile(p1)
            gzbs=xls.sheet_names
            print("路径：{}\n共{}个工作表:{}\n------".format(p1,len(gzbs),gzbs))            
        return p1,gzbs    
    def dsygzb(self,lj=None):
        """
        读文件所有工作表
        """        
        xls=pd.ExcelFile(lj)
        gzbs=xls.sheet_names
        print("路径：{}\n共{}个工作表:{}\n------".format(lj,len(gzbs),gzbs))
        return  lj,len(gzbs),gzbs

    def dxls(self,lj=False,gzb=None,hs=None,jh=None,sm=""):
        """
        读文件转列表
        lj:路径,gzb:工作表,hs:标题从第几行读，首行为None,jh:读取几行
        return:返回未整理的二维列表data_list[[]]
        """
        if lj==False:
            return
        if gzb==None:
            return 
        df=pd.read_excel(os.path.abspath(lj),sheet_name=gzb,header=hs,nrows=jh,dtype="str")
        #所有内容均为字符串,dtype="str"
        nrows=df.shape[0]#最大行
        ncols=df.columns.size#最大列
        print("--{}-{}表：共{}行，{}列数据！路径：{}".format(sm,str(gzb),nrows,ncols,lj))       
        data_array = np.array(df)
        # 然后转化为list形式
        data_list =data_array.tolist()    
        return data_list
    

   
    def dc_xls(self,bclj=False,sjwj=[]):
        """
         #导出xlsx
        lj:保存路径,sjwj:准备保存的二维列表[[]]
        return:xlsx
        """  
        
        if bclj==False:   
            bclj="{}_整理后银行.xlsx".format(sjgsh())
        if len(sjwj)==0:           
           return
        dd=pd.DataFrame(sjwj)        
        dd.to_excel(bclj,header=None,index=False,engine='openpyxl')
        print(">>>保存完成:{}".format(bclj))

    def hb_xls(self,hblj=False,bclj=False):
        """
        合并所有xlsx：合并路径，保存路径
        """        
        if hblj==False:
            return    
        lbs=[]
        #所有文件
        sywj=os.listdir(hblj)
        #遍历文件夹
        shu=0
        print("文件夹路径：{}\n共{}文件，{}".format(hblj,len(sywj),sywj))
        for i in os.listdir(hblj):
            #结尾为xls的
            if i.endswith(".xlsx") or i.endswith(".xls"):
                #合并路径
                i=os.path.join(hblj,i)
                shu+=1
                print("{}:{}\n".format(shu,i))
                #遍历读取
                lbs.append(pd.read_excel(i,header=None))
    
        #合并
        dc=pd.concat(lbs)
        #保存
        if bclj==False:
            ljss="/合并后"            
            if os.path.isdir(ljss)==False:
                os.mkdir(ljss)    
            bclj="{}/{}_合并后银行.xlsx".format(ljss,sjgsh())
       
        dc.to_excel(bclj,header=None,index=False)
        print("完成！")
                


 

if __name__ == "__main__":
    #ljs=r"D:\py\0银行明细整理\UI_v15\170.xlsx" 
    pass