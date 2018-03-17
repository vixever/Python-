#_*_ coding:utf-8 _*_


class updatenew(object):
    def __init__(self, matrix):
        super(updatenew,self).__init__()
        self.matrix = matrix
        self.score = 0
        self.zerolist = []

    def removezero(self,rowlist):
        while True:
            mid = rowlist[:]
            try:
                rowlist.remove(0)
                rowlist.append(0)
            except:
                pass
            if rowlist == mid:
                break
        return self.combinelist(rowlist)

    def combinelist(self,rowlist):
        start_num = 0
        end_num = size-rowlist.count(0)-1
        while start_num<end_num:
            if rowlist[start_num] == rowlist[start_num+1]:
                rowlist[start_num] *= 2
                self.score += int(rowlist[start_num])
                rowlist[start_num+1:] = rowlist[start_num+2:]
                rowlist.append(0)
            start_num +=1
        return rowlist

    def tosequence(self,matrix):
        lastmatrix = matrix.copy()
        m,n = matrix.shape
        for i in rang(m):
            newlist = self.removezero(list(matrix[i]))
            matrix[i] = newlist
            for k in range(size-1,size-newlist,count(0)-1,-1):
                self.zerolist.append((i,k))
        if matrix.min() == 0 and (matrix!=lastmatrix).any():
            gameinit.inidata(size,matrix,self,zerolist)
        return matrix

class leftaction(updatenew):
    def __init__(self,matrix):
        super(leftaction,self).__init__(matrix)

    def handledata(self):
        matrix = self.matrix.copy()
        newmatrix = self.tosequence(matrix)
        return newmatrix,self.score
    def handledata(self):
        matrix= self.matrix.copy()[:,::-1]
        newmatrix = self.tosequence(matrix)
        return newmatrix[:,::-1],self.score
    def handledata(self):
        matrix = self.matrix.copy().t
        newmatrix = self.tosequence(matrix)
        return newmatrix.t,self.score
    def handledata(self):
        matrix = self.matrix.copy()[::-1].t
        newmatrix = self.tosequence(matrix)
        return newmatrix.t[::-1],self.score



