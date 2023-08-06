import time
from . import util
from . import user

class AECC():
    opt = None
    runtime = {}
    out = ""

    def __init__(self, opt):
        self.opt = opt

    def run(self):
        self.opt['log'].info('COMMAND: ' + self.opt['cmd'])
        t0 = time.time()
        self.dispatch()
        t2 = time.time()

        self.opt['log'].info('Total running time: ' + str(round(t2-t0, 1))+' sec')
        self.opt['log'].info('END')

    def dispatch(self):
        if self.opt['download_token']:
            user.download_token()
        if self.opt['signup']:
            user.signup()
        
        # if self.opt['run']:
        #     ct = OOO(self.opt)
        #     ct.run()
        # if self.opt['download']:
        #     ct = OOO(self.opt)
        #     ct.donwload()
        
    
    def connector(self):
        pass

