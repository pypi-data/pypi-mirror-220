import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from pandas.tseries.offsets import BDay


from SharedData.Logger import Logger
from SharedData.SharedDataFrame import SharedDataFrame
from SharedData.SharedDataTimeSeries import SharedDataTimeSeries

class SharedDataPeriod:

    def __init__(self, sharedDataFeeder, period):
        self.sharedDataFeeder = sharedDataFeeder        
        self.sharedData = sharedDataFeeder.sharedData        
        self.period = period
            
        # DATA DICTIONARY
        # tags[tag]
        self.tags = {}

        # TIME INDEX
        self.timeidx = {}
        self.ctimeidx = {}        
        if self.period=='W1':
            self.periodSeconds = 7*60*60*24
            self.default_startDate = pd.Timestamp('1990-01-01')
        elif self.period=='D1':
            self.periodSeconds = 60*60*24       
            self.default_startDate = pd.Timestamp('1990-01-01')
        elif self.period=='M15':
            self.periodSeconds = 60*15
            self.default_startDate = pd.Timestamp('1990-01-01')
        elif self.period=='M1':
            self.periodSeconds = 60
            self.default_startDate = pd.Timestamp('2010-01-01')
        self.getContinousTimeIndex(self.default_startDate)

    def __setitem__(self, tag, df):
        if not tag in self.tags.keys():
            if isinstance(tag, pd.Timestamp):
                self.tags[tag] = SharedDataFrame(self, tag, df)
            else:
                self.tags[tag] = SharedDataTimeSeries(self, tag, df)
        elif isinstance(df, pd.DataFrame):
            data = self.tags[tag].data
            iidx = df.index.intersection(data.index)
            icol = df.columns.intersection(data.columns)
            data.loc[iidx, icol] = df.loc[iidx, icol].copy()

    def __getitem__(self, tag):
        if not tag in self.tags.keys():
            if isinstance(tag, pd.Timestamp):
                df = SharedDataFrame(self, tag)
                if not df.data.empty:
                    self.tags[tag] = df
                else:
                    return pd.DataFrame([])
            else:
                ts = SharedDataTimeSeries(self, tag)
                if not ts.data.empty:
                    self.tags[tag] = ts
                else:
                    return pd.DataFrame([])
        return self.tags[tag].data

    def getTimeIndex(self, startDate):
        if not startDate in self.timeidx.keys():
            nextsaturday = datetime.today() + BDay(21)\
                + timedelta((12 - datetime.today().weekday()) % 7)
                        
            if self.period=='D1':
                self.timeidx[startDate] = pd.Index(\
                    pd.bdate_range(start=startDate,\
                    end=np.datetime64(nextsaturday)))
                self.periodSeconds = 60*60*24
            
            elif self.period=='M15':
                self.timeidx[startDate] = pd.Index(\
                    pd.bdate_range(start=startDate,\
                    end=np.datetime64(nextsaturday),freq='15min'))                    
                idx = (self.timeidx[startDate].hour>8) 
                idx = (idx) & (self.timeidx[startDate].hour<19)
                idx = (idx) & (self.timeidx[startDate].day_of_week<5)
                self.timeidx[startDate] = self.timeidx[startDate][idx]
                self.periodSeconds = 60*15

            elif self.period=='M1':
                self.timeidx[startDate] = pd.Index(\
                    pd.bdate_range(start=startDate,\
                    end=np.datetime64(nextsaturday),freq='1min'))                    
                idx = (self.timeidx[startDate].hour>8) 
                idx = (idx) & (self.timeidx[startDate].hour<19)
                idx = (idx) & (self.timeidx[startDate].day_of_week<5)
                self.timeidx[startDate] = self.timeidx[startDate][idx]
                self.periodSeconds = 60
                
        return self.timeidx[startDate]
                
    def getContinousTimeIndex(self, startDate):
        if not startDate in self.ctimeidx.keys():            
            _timeidx = self.getTimeIndex(startDate)
            nsec = (_timeidx - startDate).astype(np.int64)
            periods = (nsec/(10**9)/self.periodSeconds).astype(np.int64)
            self.ctimeidx[startDate] = np.empty(max(periods)+1)
            self.ctimeidx[startDate][:] = np.nan
            self.ctimeidx[startDate][periods.values] = np.arange(len(periods))        
        return self.ctimeidx[startDate]

    def get(self, tag):
        if isinstance(tag, pd.Timestamp):
            df = SharedDataFrame(self, tag, malloc=False)
            return df.data
        else:  
            return pd.DataFrame([]) 
    
    def exists(self, tag):
        if isinstance(tag, pd.Timestamp):            
            path = Path(os.environ['DATABASE_FOLDER'])
            path = path / self.sharedData.user
            path = path / self.sharedData.database
            path = path / self.sharedDataFeeder.feeder
            path = path / self.period       
            fpath = path / (tag.strftime('%Y%m%d%H%M')+'.npy')            
            return fpath.is_file()
        else:
            return False 
 
    def create_timeseries(self,tag,startDate,columns,overwrite=False):
        self.tags[tag] = SharedDataTimeSeries(\
            self,tag,startDate=startDate,columns=columns,overwrite=overwrite)
        return self.tags[tag].data