import bottle
from bottle import *
import requests,os,json

import wave
import contextlib

def getlen(fn):
    with contextlib.closing(wave.open('./wav/'+fn,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        len=int(duration)
    return(len)



@bottle.route('/')
@view('index.tpl')
def index():     
    return "hello!"




@bottle.route('/info',method='GET')       
def info():       
    res={'code':0,
        'msg':'ok'}
    name = bottle.request.GET.get('name')
    if name==None: 
        res={'code':1,
        'msg':'name error'}
        return json.dumps(res)           # filer invalid input
    else:
        data=[]
        lt=os.listdir('./wav')     
        for w in lt:
            if w.find(name)>=0:           
                wl=getlen(w)     
                data.append({'name':w,'len':wl})      
        res.update({'data':data})      
        return json.dumps(res)         


@bottle.route('/list',method='GET')   
def list():       
    
    maxlen = bottle.request.GET.get('maxlen')     
    if maxlen==None  or  maxlen.isdigit==False :
        res={'code':1,
        'msg':'maxlen error'}
        return json.dumps(res)           
    else:
        maxlen=int(maxlen)    
        res={'code':0,
        'msg':'ok'}
        data=[]
        lt=os.listdir('./wav')     
        for w in lt:
            wl=getlen(w)     
            if wl<maxlen:                 
                data.append(w)          
        res={'code':0,
            'msg':'ok',
            'data':data}    
        res.update({'data':data})
        return json.dumps(res)           

@bottle.route('/download',method='GET')
def download():
    name = bottle.request.GET.get('name')
    if name==None:    
        res={'code':1,
        'msg':'name error!'}
        return json.dumps(res)           
    elif os.path.exists('./wav/%s.wav'%name)==False:
        res={'code':1,
        'msg':'%s.wav no found!'%name}
        return json.dumps(res) 
    else:
        return static_file('%s.wav'%name, root=r'./wav/', download=True)
    
 
    
@bottle.route('/upload',method='POST')
def upload_do():    
    upload = bottle.request.files.get('file')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.wav'):
        res={'code':1,
        'msg':'ext error!'}
        return json.dumps(res)
    save_path = './wav/'+name+ext
    try:
    
        upload.save(save_path) # appends upload.filename automatically
        res={'code':0,
        'msg':'ok'}
    except Exception as e:
        res={'code':1,
        'msg':'error :'+str(e)}
    
    return json.dumps(res) 

   
bottle.run(host = '0.0.0.0', port = 7104)  
