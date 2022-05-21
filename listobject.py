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

    Demonstration
    ----------

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
    
    @property
    def l(self) -> int:
        """The length of a listobj object"""
        return self.N

    def fadd(self,obj):
        """Add a iterable object in front."""
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
        """Add a iterable object behind."""
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
            gap = index.step
            length = ceil((end-start)/gap)
            if isinstance(value,(list,tuple,listobj)):
                if len(value) != length:
                    raise ValueError("the lengths don't match.")
                else:
                    for i in range(length):
                        self.liobj[start+i*gap] = index[i]
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
    if not isinstance(all,int):
        raise ValueError("the total number of the sequence must be integer")
    new = []
    start = Decimal(str(start))
    end = Decimal(str(end))
    q = pow(end/start,Decimal(1/(all-1)))
    for i in range(all):
        new.append(start*q**i)
    return listobj(new)
