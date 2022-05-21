# -*- coding:utf8 -*-
from decimal import Decimal
from copy import deepcopy
from math import ceil

class listobj:
    """
    Create a sequence which can be broadcasted, just the same as the array object in numpy.
    
    Attention
    ----------
    The Decimal class will be replaced by pyfloat object in the later version, which also surpports 
    accurate decimal operation.

    Params
    ----------
    liobj :
    This param allows you to convey a iterable object to build a listobj object, and
    only numbers can exsits in it. Or the 'invalid list' error will emerge. The elements
    in the listobject will be conversed to Decimal object.

    Property
    ----------
    l :
    Return the length of a listobj.
    :return : int

    min :
    Return the minimum number of the listobj
    :return : Decimal

    max :
    Return the maximum number of the listobj
    :return : Decimal

    avg :
    Return the average number of the listobj
    :return : Decimal

    middle :
    Return the median number of the listobj
    :return : Decimal

    Method
    ----------
    fadd :
    The name is short for 'add forward'. It can add a iterable object or a number in front of a listobj.
    :return : listobj

    badd :
    The name is shrot for 'add backward'. It can add a iterable object or a number at the back of a listobj.
    :return : listobj

    Built-in Methods
    ----------
    These methods determine the broadcast function of a listobj.
    {'__add__','__radd__','__mul__','__rmul__','__sub__','__rsub__','__truediv__','__rturediv__',
     '__eq__','__pow__','__rpow__','__repr__','__len__','__getitem__','__setitem__','__delitem__'}
    """
    def __init__(self,liobj):
        """Initialize a iterable object to listobj class."""
        self.liobj = []
        self.N = len(liobj)
        if isinstance(liobj,listobj):
            self.liobj = liobj.liobj
        else:
            for i in range(self.N):
                if isinstance(liobj[i],(list,tuple,str)):
                    raise ValueError("invlid list value")
                self.liobj.append(liobj[i])
    
    @staticmethod
    def order_(arr:list,by="asc"):
        """
        Ordering method associated with min, max and avg property, 
        and it won't change the original order.
        """
        for i in range(len(arr)-1):
            for j in range(i,len(arr)):
                if by == "asc":
                    if arr[i] > arr[j]:
                        arr[i],arr[j] = arr[j],arr[i]
                elif by == "des":
                    if arr[i] < arr[j]:
                        arr[i],arr[j] = arr[j],arr[i]
                else:
                    raise ValueError(f"unknown ordering rule '{by}'")
        return arr
    
    @property
    def l(self) -> int:
        """The length of a listobj object"""
        return self.N

    @property
    def max(self):
        """the maximum number in the sequence"""
        li = deepcopy(self.liobj)   # must copy self.liobj, avoiding the shallow copy problem
        new = listobj.order_(li)
        del li
        return new[-1]

    @property
    def min(self):
        """the minimum number in the sequence"""
        li = deepcopy(self.liobj)
        new = listobj.order_(li)
        del li
        return new[0]

    @property
    def avg(self):
        """the average number of the sequence"""
        tmp = 0
        for i in range(self.N):
            tmp += self.liobj[i]
        return tmp/self.N

    @property
    def middle(self):
        """the median number of the sequence"""
        li = deepcopy(self.liobj)
        new = listobj.order_(li)
        del li
        if self.N % 2 == 0:
            return Decimal(str((new[int(self.N/2)] + new[int(self.N/2-1)] / 2)))
        else:
            return Decimal(str(new[int((self.N-1)/2)]))

    def order(self,by):
        """
        It is used to order the list

        Params
        ----------
        by : 'asc' for ascending order while 'des' for descending order.
        """
        if by == "asc":
            self.liobj = listobj.order_(self.liobj,by)
        elif by == "des":
            self.liobj = listobj.order_(self.liobj,by)
        else:
            raise ValueError(f"unknown ordering rule '{by}'")
        return self

    def fadd(self,obj):
        """
        Add a iterable object in front. And it return a listobj.

        Params
        ----------
        obj : This parameter can be int, float, Decimal, list, tuple or listobj.
        """
        if isinstance(obj,(int,float,Decimal)):
            self.liobj.insert(0,Decimal(str(obj)))
            self.N += 1
            del obj
            return self
        if isinstance(obj,(list,tuple,listobj)):
            another = listobj(obj)
            another.liobj.extend(self.liobj)
            self.liobj = deepcopy(another.liobj)
            self.N += len(obj)
            del another
            del obj
            return self
        del obj
        raise ValueError(f"got unsurpported type {type(obj)}")

    def badd(self,obj):
        """
        Add a iterable object behind. And it return a listobj.

        Params
        ----------
        obj : This parameter can be int, float, Decimal, list, tuple or listobj.
        """
        if isinstance(obj,(int,float,Decimal)):
            self.liobj.extend([Decimal(str(obj))])
            self.N += 1
            del obj
            return self
        if isinstance(obj,(list,tuple,listobj)):
            another = listobj(obj)
            self.liobj.extend(another.liobj)
            self.N += len(obj)
            del another
            del obj
            return self
        del obj
        raise ValueError(f"got unsurpported type {type(obj)}")

    def __add__(self,other):
        if isinstance(other,(Decimal,int,float)):
            for i in range(self.N):
                self.liobj[i] += Decimal(str(other))
            return self
        if isinstance(other,(list,tuple)):
            if len(other) == self.N:
                for i in range(self.N):
                    self.liobj[i] += Decimal(str(other[i]))
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {len(other)}")
        if isinstance(other,listobj):
            if self.N == other.N:
                for i in range(self.N):
                    self.liobj[i] += other.liobj[i]
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {other.N}")
        raise ValueError(f"invalid type of {type(other)}")

    def __radd__(self,other):
        if isinstance(other,(Decimal,int,float)):
            for i in range(self.N):
                self.liobj[i] += Decimal(str(other))
            return self
        if isinstance(other,(list,tuple)):
            if len(other) == self.N:
                for i in range(self.N):
                    self.liobj[i] += Decimal(str(other[i]))
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {len(other)}")
        raise ValueError(f"invalid type of {type(other)}")

    def __mul__(self,other):
        if isinstance(other,(Decimal,int,float)):
            for i in range(self.N):
                self.liobj[i] *= Decimal(str(other))
            return self
        if isinstance(other,(list,tuple)):
            if len(other) == self.N:
                for i in range(self.N):
                    self.liobj[i] *= Decimal(str(other[i]))
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {len(other)}")
        if isinstance(other,listobj):
            if self.N == other.N:
                for i in range(self.N):
                    self.liobj[i] *= other.liobj[i]
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {other.N}")
        raise ValueError(f"invalid type of {type(other)}")

    def __rmul__(self,other):
        if isinstance(other,(Decimal,int,float)):
            for i in range(self.N):
                self.liobj[i] *= Decimal(str(other))
            return self
        if isinstance(other,(list,tuple)):
            if len(other) == self.N:
                for i in range(self.N):
                    self.liobj[i] *= Decimal(str(other[i]))
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {len(other)}")
        raise ValueError(f"invalid type of {type(other)}")

    def __sub__(self,other):
        if isinstance(other,(Decimal,int,float)):
            for i in range(self.N):
                self.liobj[i] -= Decimal(str(other))
            return self
        if isinstance(other,(list,tuple)):
            if len(other) == self.N:
                for i in range(self.N):
                    self.liobj[i] -= Decimal(str(other[i]))
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {len(other)}")
        if isinstance(other,listobj):
            if self.N == other.N:
                for i in range(self.N):
                    self.liobj[i] -= other.liobj[i]
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {other.N}")
        raise ValueError(f"invalid type of {type(other)}")

    def __rsub__(self,other):
        if isinstance(other,(Decimal,int,float)):
            for i in range(self.N):
                self.liobj[i] = Decimal(str(other)) - self.liobj[i]
            return self
        if isinstance(other,(list,tuple)):
            if len(other) == self.N:
                for i in range(self.N):
                    self.liobj[i] = Decimal(str(other[i])) - self.liobj[i]
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {len(other)}")
        raise ValueError(f"invalid type of {type(other)}")

    def __truediv__(self,other):
        if isinstance(other,(Decimal,int,float)):
            for i in range(self.N):
                self.liobj[i] = self.liobj[i]/Decimal(str(other))
            return self
        if isinstance(other,(list,tuple)):
            if len(other) == self.N:
                for i in range(self.N):
                    self.liobj[i] = self.liobj[i]/Decimal(str(other[i]))
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {len(other)}")
        if isinstance(other,listobj):
            if self.N == other.N:
                for i in range(self.N):
                    self.liobj[i] = self.liobj[i]/other.liobj[i]
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {other.N}")
        raise ValueError(f"invalid type of {type(other)}")

    def __rtruediv__(self,other):
        if isinstance(other,(Decimal,int,float)):
            for i in range(self.N):
                self.liobj[i] = Decimal(str(other))/self.liobj[i]
            return self
        if isinstance(other,(list,tuple)):
            if len(other) == self.N:
                for i in range(self.N):
                    self.liobj[i] = Decimal(str(other[i]))/self.liobj[i]
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {len(other)}")
        raise ValueError(f"invalid type of {type(other)}")

    def __eq__(self,other):
        if not isinstance(other,listobj):
            raise ValueError(f"only listobj could use '=', got type {type(other)}")
        if self.N == other.N:
            return True
        return False

    def __pow__(self,other):
        if isinstance(other,(Decimal,int,float)):
            for i in range(self.N):
                self.liobj[i] = self.liobj[i]**Decimal(str(other))
            return self
        if isinstance(other,(list,tuple)):
            if len(other) == self.N:
                for i in range(self.N):
                    self.liobj[i] = self.liobj[i]**Decimal(str(other[i]))
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {len(other)}")
        if isinstance(other,listobj):
            if self.N == other.N:
                for i in range(self.N):
                    self.liobj[i] = self.liobj[i]**other.liobj[i]
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {other.N}")
        raise ValueError(f"invalid type of {type(other)}")

    def __rpow__(self,other):
        if isinstance(other,(Decimal,int,float)):
            for i in range(self.N):
                self.liobj[i] = Decimal(str(other))**self.liobj[i]
            return self
        if isinstance(other,(list,tuple)):
            if len(other) == self.N:
                for i in range(self.N):
                    self.liobj[i] = Decimal(str(other[i]))**self.liobj[i]
                return self
            else:
                raise ValueError(f"cannot add the two sequences with length {self.N} and {len(other)}")
        raise ValueError(f"invalid type of {type(other)}")

    def __len__(self):
        return self.N

    def __repr__(self):
        string = "["
        for i in range(self.N):
            string += str(self.liobj[i]) + "  "
            if i == 5:
                string += "\n"
        return string + "]"

    def __getitem__(self,index):
        if isinstance(index,int):
            if index >= self.N:
                raise ValueError("list index out of range")
            return self.liobj[index]
        if isinstance(index,slice):
            start = index.start
            end = index.stop
            gap = index.step
            new = self.liobj[start:end:gap]
            self.liobj = deepcopy(new)
            self.N = end-start
            del new
            return self
        del index
        raise ValueError(f"cannot receive the {type(index)} as index.")

    def __setitem__(self,index,value):
        if isinstance(index,int):
            if isinstance(value,(int,float,Decimal)):
                self.liobj[index] = Decimal(str(value))
            else:
                raise ValueError(f"liobj cannot be assigned by {type(value)}")
            return self
        if isinstance(index,slice):
            start = index.start
            end = index.stop
            if index.step is None:
                gap = 1
            else:
                gap = index.step
            length = ceil((end-start)/gap)
            if isinstance(value,(list,tuple,listobj)):
                if len(value) != length:
                    raise ValueError("the lengths don't match.")
                else:
                    for i in range(length):
                        self.liobj[start+i*gap] = value[i]
            else:
                raise ValueError(f"liobj cannot be assigned by {type(value)}")
            return self
        del index,value
        raise ValueError(f"cannot receive the {type(index)} as index.")

    def __delitem__(self,index):
        if isinstance(index,int):
            del self.liobj[index]
            self.N -= 1
            return self
        if isinstance(index,slice):
            start = index.start
            end = index.stop
            if index.step is None:
                gap = 1
            else:
                gap = index.step
            length = ceil((end-start)/gap)
            for i in range(start,end,gap):
                del self.liobj[i]
            self.N -= length
            return self
        del index
        raise ValueError(f"cannot receive the {type(index)} as index.")


def ariseq(start,end,all:int) -> listobj:
    """
    Create an arithmetic sequence. It can do the same thing as the function of numpy.linspace.
    This function will automatically work out the common difference.

    Params
    ----------
    start : The start number of the arithmetic sequence.
    end : The ending number of the arithmetic sequence.
    all : The total number of the arithmetic sequence.

    Return
    ----------
    The returning type of the value is listobj

    Demonstration
    ----------
    a = arisec(0,3,5)
    print(a)
    >>> [0.00  0.75  1.50  2.25  3.00  ]
    """
    if not isinstance(all,int):
        raise ValueError("the total number of the sequence must be integer")
    new = []
    start = Decimal(str(start))
    end = Decimal(str(end))
    gap = (end-start)/(Decimal(all-1))
    for i in range(all):
        new.append(start+gap*i)
    return listobj(new)


def proseq(start,end,all:int) -> listobj:
    """
    Create a proportional sequence. Once the three params are given, this function
    wil automatically work out the common ratio.

    Params
    ----------
    start : The start number of the proportional sequence.
    end : The ending number of the proportional sequence.
    all : The total number of the proportional sequence.

    Return
    ----------
    The returning type of the value is listobj

    Demonstration
    ----------
    a = proseq(1,3,5)
    print(a)
    >>> [1  1.31607401  1.73205080  2.27950705  3.00000000  ]
    """
    if start == 0:
        raise ValueError("A proportional sequence cannot start with 0")
    if not isinstance(all,int):
        raise ValueError("the total number of the sequence must be integer")
    new = []
    start = Decimal(str(start))
    end = Decimal(str(end))
    q = pow(end/start,Decimal(1/(all-1)))
    for i in range(all):
        new.append(start*q**i)
    return listobj(new)

