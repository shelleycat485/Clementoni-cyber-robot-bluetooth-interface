import sys, os, time, cv2, re
g_nslices = 17
g_globseq = 0

class c_reposition:
    (p, target_slice, mw, integration_counter, nslices) = (0,0,False,0,0)

    def __init__(self, nslices):
        self.nslices = nslices

    def max_min_ok(self, resarr):
        av = sum (resarr) / len(resarr)
        max1 = max(resarr)
        min1 = min(resarr)
        print(f'l:{len(resarr)} av:{av} max:{max1}, min:{min1}')
        if (max1 - av < 100) and (av - min1 < 100):
          return False

        return True

    def calc_lor(self, res):
        (m, p, return_slice) = (max(res), 1, 0)
        for i in range(0,len(res) - 1):
            if res[i] == m:
                self.target_slice = i
                if i > self.nslices/2:
                  p = 2
                if i < self.nslices/2:
                  p = 0
        self.integration_counter += 1
        if self.p != p: # a move wanted
            (self.integration_counter, self.p, self.mw) = (0, p, True)
        else:
            self.mw = False # no chahge to self.p because no move
            if self.integration_counter > 5:
                self.p = 1
        print("calc_lor target slice:", self.target_slice)
        return self.target_slice

    def send_move(self):
        global g_globseq
        pstr = ''
        if self.mw == True:
          if self.p == 2:
                pstr = "Left"
          elif self.p == 0:
                pstr = "Right"
        print ('send_move:', g_globseq, self.p, pstr)
        g_globseq += 1
        print (pstr)

reposition = c_reposition(g_nslices) # slices

def target_seek(img, slices):
    nimg = cv2.integral(img)[1:,1:]
    #nimg = nimg[1:,1:]
    (rows, cols) = nimg.shape
    (vstart, vend, horiz_inc, res) = (50, rows - 1 - 100, int(cols/slices), [])
    for i in range (0, slices):
        hstart = i * horiz_inc
        hend = hstart + horiz_inc
        res.append( nimg.item(vend, hend) - nimg.item(vend, hstart)
                - nimg.item(vstart, hend ) + nimg.item(vstart, hstart))
    if reposition.max_min_ok(res):
        return reposition.calc_lor(res)
    else:
        return -1
        
def show_target_on_image(img, slices, hilight):
    (rows, cols, channels) = img.shape
    if hilight > 0 and hilight < (slices - 1):
        cv2.rectangle(img, (hilight * int(cols/slices),50),((hilight+1) * int(cols/slices), rows - 100),  (0, 255,0), 2)

def main():
    if len(sys.argv) < 2:
      print ("CTxxx -d|-D regex_for_filenames")
    
    (oldflag, oldimg, pathname) = (False, None, '/home/pi/Videos')
    reobj = re.compile(sys.argv[2], re.I)
    for fname in sorted(os.listdir(pathname)):
        if reobj.match(fname):
            print("main:", fname)
            img = cv2.imread(os.path.join(pathname, fname))
            cv2.imshow("orig", img)
            cv2.waitKey(5)
            imgg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if oldflag:
                imgdiff = cv2.absdiff(imgg, oldimg)
                positionfound = target_seek (imgdiff, g_nslices)
                show_target_on_image (img, g_nslices, positionfound)
                reposition.send_move()
                if sys.argv[1] == '-D' and positionfound != -1:
                    cv2.imshow("hilight", img)
                    cv2.waitKey(10 * 1000)
            (oldflag, oldimg) = (True, imgg)

main()

