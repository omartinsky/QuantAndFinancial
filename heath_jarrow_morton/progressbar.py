import sys

class ProgressBar:
    def __init__(self, title, n):
        self.title = title
        self.last, self.n = None, n
    def update(self, i):
        p = int(100*(i+1)/self.n)
        p = int(p)
        if i==0:
            print("%s " % self.title)
        if self.last is not None and self.last == p and i!=self.n-1:
            return
        self.last = p
        if (p%10==0):
            sys.stdout.write("%i%%" % p), sys.stdout.flush()
        elif (p%2==0):
            sys.stdout.write("."), sys.stdout.flush()