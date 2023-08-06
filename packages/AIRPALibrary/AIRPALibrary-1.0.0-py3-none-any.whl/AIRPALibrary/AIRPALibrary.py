import json
import os

class AIRPALibrary:
    def __init__(self):
        pass
    
    def read_config(self,additional=None):
        ''' fungsi untuk membaca file konfigurasi json, pengguna dapat menambahkan untuk data 
            yang dibutuhkan dengan format json object. Output dari fungsi ini adalah file konfigurasi
            dalam bentuk json object.
            
            contoh penggunaan :
                ${config}=  read_config
            
        '''
        try:
            with open(os.getcwd()+'\\config.json') as jsonfile:
                conf = json.load(jsonfile)
        except:
            raise RuntimeError('File config.json tidak ditemukan')
        
        if additional!=None:
            try:
                conf.update(json.loads(additional))
            except:
                raise RuntimeError('Pastikan kembali json object yang dimasukkan sebagai parameter')
        return conf
    