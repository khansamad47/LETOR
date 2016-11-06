import numpy as np
import pandas as pd
import logging
import os
import mimetypes
import re

#File logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
filename='LETOR'
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('log_'+filename+'.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

class Data_Reader(object):
    
      
    __doc__="""
    Data_Reader
    Class for reading the input data excel file
    
    Notes
    -----
    **Attributes**
    filename : xlsx file
        The name the input file containing the data to be read.
        Default is None
    input_filepath : str
        The path of the folder where the above input file is to be read from.
        Default is current working directory
    
     Final Script Usage Examples
    ---------
    1.) Example 1
        >>> inst_dr=Data_Reader()
        >>> inst_lr=Logistic_Model.model_fit(inst_dr)
            
    """
    
    __slots__=('_filename','_input_filepath','df_out')
    
    #Initializing Data_Reader Class 
    def __init__(self,**kwargs):
        self._filename=kwargs.pop('filename',"Querylevelnorm.txt")
        self._input_filepath=kwargs.pop('input_filepath',os.getcwd())
        self.df_out=self.file_parser()
        if kwargs:
            raise TypeError("Unexpected **kwargs: %r" % kwargs)

    #Setting property attributes for class instance variables
    @property
    def filename(self):
        return self._filename
     
    @filename.setter
    def filename(self,filename):
        if not os.path.isfile(os.path.join(self.filepath,filename)):
            logging.debug("%s does not exist in this folder: %s!" %(filename,self.filepath))
        if mimetypes.guess_type(os.path.join(self.filepath,filename))[0]	 == 'text/plain':
            logging.debug("%s file does not appear to be in xlsx format" %filename)
        else:
            fileloc=self.filepath+"\\"+filename
            logging.debug("%s file does not appear to be in xlsx format" %fileloc)
        
        self._filename=filename

    @filename.deleter
    def filename(self):
        del self._filename


    @property
    def input_filepath(self):
        return self._input_filepath
    
    
    @input_filepath.setter
    def input_filepath(self,value):
        if type(value)!=str:
           logging.debug("Please set the attribute in str form!") 
        self._input_filepath=value
    
    
    @input_filepath.deleter
    def input_filepath(self):
        del self._input_filepath

    
    def file_parser(self):
        input_file=self.filename
        pattern = r'(^\d+)|((?<=:)([\d.]+)(?=\s+))'
        feature_cols=["feature_"+str(x) for x in range(1,47)]
        col_names=["relevance_lbl","qid"]+feature_cols
        with open(input_file) as f:
            numlines = len(f.readlines())
        f.close()
        df=pd.DataFrame(index=np.arange(numlines),columns=col_names)
        with open(input_file,'r') as rdr:
            for line_number, line in enumerate(rdr):
                init_list = [match.group(0) for match in re.finditer(pattern,line)]
                df.loc[line_number]=init_list
                
        return df
        
    
    
    #Returns a clean dataframe for feeding to the logistic regression model
    #def clean_df(self):
    #    raw_df = pd.read_excel(self.filename)
    #    #Determining columns with all NaNs
    #    colnames = raw_df.columns[pd.isnull(raw_df).all()].tolist()
    #    cleandf = raw_df[raw_df.columns[~raw_df.columns.str.contains('Unnamed:')]]
    #    return cleandf
 