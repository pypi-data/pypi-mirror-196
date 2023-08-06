from . import Mvi
import threading
import os
import numpy as np
from . import mudeConstant as mc
from . import Image_Pre_Treat


class mvi_Thread(threading.Thread):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.layer = os.path.basename(path).split('_')[1]

    def run(self) -> None:
        self.result = Mvi.mvi(self.path)

    def get_result(self):
        return self.layer, self.result


class Ref:
    def __init__(self, project):
        self.project = project
        self.ref = self.mvi_read()

    def get_Image(self, layer, xy):
            x, y = xy
            ref = self.ref[layer].mvi_show_bin(int(x / 12), self.ref[layer].height - int(y / 12), 108)
            drl, dr2, drvia = np.zeros((108, 108), np.uint8), np.zeros((108, 108), np.uint8), np.zeros((108, 108), np.uint8)
            if 'DRL' in self.ref.keys():
                drl = self.ref['DRL'].mvi_show_bin(int(x / 12), self.ref['DRL'].height - int(y / 12), 108) if layer == 'GTL' else np.fliplr(
                    self.ref['DRL'].mvi_show_bin(self.ref['DRL'].width - int(x / 12), self.ref['DRL'].height - int(y / 12), 108))
            if 'DR2' in self.ref.keys():
                dr2 = self.ref['DR2'].mvi_show_bin(int(x / 12), self.ref['DR2'].height - int(y / 12), 108) if layer == 'GTL' else np.fliplr(
                    self.ref['DR2'].mvi_show_bin(self.ref['DR2'].width - int(x / 12), self.ref['DR2'].height - int(y / 12), 108))
            if 'DRVIA' in self.ref.keys():
                drvia = self.ref['DRVIA'].mvi_show_bin(int(x / 12), self.ref['DRVIA'].height - int(y / 12), 108) if layer == 'GTL' else np.fliplr(
                    self.ref['DRVIA'].mvi_show_bin(self.ref['DRVIA'].width - int(x / 12), self.ref['DRVIA'].height - int(y / 12), 108))
            return Image_Pre_Treat.Ref_Drl_Cat(ref, drl=drl, dr2=dr2, drvia=drvia)

    def mvi_read(self):
        pro_path = os.path.join(mc.Project_Path, self.project, '0_101')
        mvis = os.listdir(pro_path)
        mvis = [i for i in mvis if i.find('.mvi') > 0]
        threads = []
        for mvi in mvis:
            threads.append(mvi_Thread(path=os.path.join(pro_path, mvi)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        result = []
        for thread in threads:
            result.append(thread.get_result())
        return dict(result)


if __name__ == '__main__':
    pass
