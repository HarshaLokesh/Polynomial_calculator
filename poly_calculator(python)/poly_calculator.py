import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from itertools import zip_longest
import getch
class _PolyTermNode(object):
 """
 linked list containing the degree, coefficient and the next pointer
 """
 def __init__(self, degree, coefficient):
     self.degree = degree
     self.coefficient = coefficient
     self.next = None
class Polynomial:
 """
 A polynomial is a mathematical expression of a variable constructed of one or
more
 terms.Each term is of the form a_i*x^i where a_i is a scalar coefficient and x^i is
the unknown variable of degree i.
 """
 def __init__(self, degree=None, coefficient=None):
    """
    Using default parameters:
     i. Creates a new polynomial initialized to be empty and thus containing not
    terms.
    ii.Creates a new polynomial initialized with a single term constructed from
    the degree and coefficient arguments.
    """
    if degree is None:
        self._polyHead = None
    else:
        self._polyHead = _PolyTermNode(degree, coefficient)
        self._polyTail = self._polyHead
 def degree(self):

    if self._polyHead is None:
        return -1
    else:
        return self._polyHead.degree

 def __getitem__(self, degree):
    """
    Returns the coefficient for the term of the provided degree. Thus,if the
    expression of
    this polynomial is x^3 + 4x + 2 and a degree of 1 is provided, this operation
    returns 4.
    The coefficient cannot be returned for an empty po
    Returns the coefficient for the term of the provided degree. Thus,if the
    expression of
    this polynomial is x^3 + 4x + 2 and a degree of 1 is provided, this operation
    returns 4.
    The coefficient cannot be returned for an empty polynomial.
    """
    assert self.degree() >= 0, \
    "Operation not permitted on an empty polynomial."
    curNode = self._polyHead
    while curNode is not None and curNode.degree >= degree:
        curNode = curNode.next
    if curNode is None or curNode.degree != degree:
        return 0
    else:
        return curNode.coefficient
 def evaluate(self, scalar):
    """
    Evaluates the polynomial at the given scalar value and returns the result. An
    empty
    polynomial cannot be evaluated.
    """
    # assert self.degree >= 0, \
    # "Only non-empty polynomials can be evaluated."

    result = 0
    curNode = self._polyHead
    while curNode is not None:
        result += curNode.coefficient * (scalar ** curNode.degree)
        curNode = curNode.next
    return result


 def __add__(self, rhsPoly):
    """
    Creates and returns a new Polynomial that is the result of adding this
    polynomial and
    the rhsPoly.This operation is not defined if either polynomial is empty.
    """
    if(self.degree() >= 0 and rhsPoly.degree() >= 0):
        #"Addition only allowed on non-empty polynomials."
        newPoly = Polynomial()
        nodeA = self._polyHead
        nodeB = rhsPoly._polyHead
        while nodeA is not None and nodeB is not None:
            if nodeA.degree > nodeB.degree:
                degree = nodeA.degree
                coefficient = nodeA.coefficient
                nodeA = nodeA.next
            elif nodeA.degree < nodeB.degree:
                degree = nodeB.degree
                coefficient = nodeB.coefficient
                nodeB = nodeB.next
            else:
                degree = nodeA.degree # or degree = nodeB.degree
                coefficient = nodeA.coefficient + nodeB.coefficient
                nodeA = nodeA.next
                nodeB = nodeB.next
            newPoly._appendTerm(degree, coefficient)
            while nodeA is not None:
                newPoly._appendTerm(nodeA.degree, nodeA.coefficient)
                nodeA = nodeA.next

            while nodeB is not None:
                newPoly._appendTerm(nodeB.degree, nodeB.coefficient)
                nodeB = nodeB.next

        return newPoly
    else:
        print("empty polynomial")
 def __sub__(self, rhsPoly):
    """
    Almost the same as the __add__() method, whearas when the nodeA's
    degree is smaller than the nodeB's
    degree, the new coefficient will be the -nodeB.coefficient.
    """
    assert self.degree() >= 0 and rhsPoly.degree() >= 0, \
    "Substraction only allowed on non-empty polynomials."


    newPoly = Polynomial()
    nodeA = self._polyHead
    nodeB = rhsPoly._polyHead
    while nodeA is not None and nodeB is not None:
        if nodeA.degree > nodeB.degree:
            degree = nodeA.degree
            coefficient = nodeA.coefficient
            nodeA = nodeA.next
        elif nodeA.degree < nodeB.degree:
            degree = nodeB.degree
            coefficient = -nodeB.coefficient # -nodeB.coefficient
            nodeB = nodeB.next
        else:
            degree = nodeA.degree # or degree = nodeB.degree
        # cannot exchange A and B's position
            coefficient = nodeA.coefficient - nodeB.coefficient
            nodeA = nodeA.next
            nodeB = nodeB.next
            newPoly._appendTerm(degree, coefficient)
        while nodeA is not None:
            newPoly._appendTerm(nodeA.degree, nodeA.coefficient)
            nodeA = nodeA.next
        while nodeB is not None:
            newPoly._appendTerm(nodeB.degree, nodeB.coefficient)
            nodeB = nodeB.next

    return newPoly

 def __mul__(self, rhsPoly):
    """
    Computing the product of two polynomials requires multiplying the second
    polynomial by each term.This
    generates a series of intermediate polynomials, which are then be added to
    create the final product.
    """
    assert self.degree() >= 0 and rhsPoly.degree() >= 0,\
    "Multiplication only allowed on non-empty polynomials."
    node = self._polyHead
    newPoly = rhsPoly._termMultiply(node)
    node = node.next
    while node is not None:
        tempPoly = rhsPoly._termMultiply(node)
        newPoly += tempPoly
        node = node.next
    return newPoly

 def _termMultiply(self, termNode):
    """
    Helper method which creates a new polynomial from multiplying an existing
    polynomial by another term.
    """
    newPoly = Polynomial()
    curr = self._polyHead
    while curr is not None:
        newDegree = curr.degree + termNode.degree
        newCoefficient = curr.coefficient * termNode.coefficient
        newPoly._appendTerm(newDegree, newCoefficient)
        curr = curr.next
    return newPoly

 def _appendTerm(self, degree, coefficient):
    """
    Helper method which accepts the degree and coefficient of a polynomial
    term, creates a new node to store the term
    and appends the node to the end of the list.
    """
    if coefficient != 0:
        newTerm = _PolyTermNode(degree, coefficient)

        if self._polyHead is None:
            self._polyHead = newTerm
        else:
            self._polyTail.next = newTerm

        self._polyTail = newTerm

 def printPoly(self):
    """
    Extra method which is not necessary for the Polynomial ADT.Just using it to
    show up the result of the operations
    between two or more polynomials.
    """
    curNode = self._polyHead
    while curNode is not None:
        if curNode.next is not None:
 # string format based on the dictionary.
            print("%(coefficient)sx^%(degree)s + " % {"coefficient": curNode.coefficient, "degree": curNode.degree},end=""),
        else:
            print ("%(coefficient)sx^%(degree)s" % {"coefficient": curNode.coefficient,"degree": curNode.degree},end="")
        curNode = curNode.next

def extended_synthetic_division(dividend, divisor):
    out = list(dividend) # Copy the dividend
    normalizer = divisor[0]
    for i in range(len(dividend)-(len(divisor)-1)):
        out[i] /= normalizer
        coef = out[i]
        if coef != 0:
            for j in range(1, len(divisor)):
                out[i + j] += -divisor[j] * coef
    separator = -(len(divisor)-1)
    return out[:separator], out[separator:] # return quotient, remainder.

class Graphical_Polynomial:
 def __init__(self, coefficients=None):
    """
    input: coefficients are in the form a_n, ...a_1, a_0
    """
    self.coefficients = list(coefficients) # tuple is turned into a list

 def __repr__(self):
    """
    method to return the canonical string representation
    of a polynomial.
    """
    return "Polynomial" + str(self.coefficients)
 def __call__(self, x):
    res = 0
    for coeff in self.coefficients:
        res = res * x + coeff
    return res

 def degree(self):
    return len(self.coefficients)

def print_there(x, y, text):
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
    sys.stdout.flush()

if __name__ == "__main__":
    temp1=True
    while(temp1):
        os.system('cls')
        print("\n")
        print("------------------------------------------------------------------------------")
        print("\n")
        print_there(5,5," _____   ____")
        print_there(6,5,"|     | |    | |    \   /")
        print_there(7,5,"|_____| |    | |     \ /")
        print_there(8,5,"|       |    | |      | ")
        print_there(9,5,"|       |____| |_____ | ")
        print_there(11,7," CALCULATOR")
        print_there(13,0,"------------------------------------------------------------------------------")
        print_there(15,4,"1. Solve")
        print_there(16,4,"2. About the project")
        print_there(17,4,"3. Exit")
        print_there(20,10,"Press enter after the input!!!")
        ch=input()
        if ch=='1' :
            os.system('cls')
            temp=True
            while(temp):
                print("\n \n Insert the polynomials before add,sub,mul and division\n\n 0.insert(polynomial)\n 1.add\n 2.sub\n 3.multiply\n 4.divide\n 5.evaluate\n 6.Graph \n 7.exit \n\n")
                print("Note: Division in done in the form of extended_synthetic_division\n i.e the input and output is given in the form of lists which contain the coefficients of the polynomial")
                print(" Graphical representation also requires separate inputs (continuous polynomial)")
                choice = input("\nEnter choice:")
                if choice =='0':
                    os.system('cls')
                    print("\nEnter the 1st polynomial:")
                    print("\nEnter the degree:")
                    de = list(map(float, input("Enter multiple values: ").split()))
                    print("\nEnter the coefficient:")
                    co = list(map(float, input("Enter multiple values: ").split()))
                    poly1=Polynomial(0,0)

                    for i in range(len(de)):
                        poly1 += Polynomial(de[i],co[i])

                    print("\nEnter the 2st polynomial:")
                    print("\nEnter the degree:")
                    de = list(map(float, input("Enter multiple values: ").split()))
                    print("\nEnter the coefficient:")
                    co = list(map(float, input("Enter multiple values: ").split()))

                    poly2=Polynomial(0,0)

                    for i in range(len(de)):
                        poly2 += Polynomial(de[i],co[i])

                    print("\nEntered polynomials are :\n")
                    poly1.printPoly()
                    print("\n")
                    poly2.printPoly()
                    print("\n Enter anykey to continue....")
                    char = getch.getch()
                    os.system('cls')

                if choice=='1':
                    os.system('cls')
                    addpoly=poly1+poly2
                    print("\nThe polynomial addition gives: ")
                    addpoly.printPoly()
                    print("\n Enter anykey to continue....")
                    char = getch.getch()
                    os.system('cls')

                if choice=='2':
                    os.system('cls')
                    subpoly1=poly1-poly2
                    subpoly2=poly2-poly1
                    print("\nThe polynomial Substraction (1-2) gives: ")
                    subpoly1.printPoly()
                    print("\nThe polynomial Substraction (2-1) gives: ")
                    subpoly2.printPoly()
                    print("\n Enter anykey to continue....")
                    char = getch.getch()
                    os.system('cls')

                if choice=='3':
                    os.system('cls')
                    mulPoly=poly1*poly2
                    print("\nTHe polynomial Multiplication gives:")
                    mulPoly.printPoly()
                    print("\n Enter anykey to continue....")
                    char = getch.getch()
                    os.system('cls')

                if choice=='4':
                    os.system('cls')
                    print("Division is in the form of extended_synthetic_division \n i.e the expression must in the ax^3 + bx^2 + cx^1+ x^0 the degree is always continuous only coefficient in entered of the two polynomials")
                    N = list(map(int, input("Enter the dividend coefficient (with space):").split()))
                    D = list(map(int, input("Enter the divisor coefficient (with space):").split()))
                    print("The quotient and remainder coefficients are respective::")
                    print(extended_synthetic_division(N, D))
                    print("\n Enter anykey to continue....")
                    char = getch.getch()
                    os.system('cls')

                if choice=='5':
                    os.system('cls')
                    n=int(input("Enter the evaluate integer for the polynomial:"))
                    print("The polynomial 1:",poly1.evaluate(n))
                    print("The polynomial 2:",poly2.evaluate(n))
                    mulPoly=poly1*poly2
                    print("The multiple :" , mulPoly.evaluate(n))
                    subpoly1=poly1-poly2
                    subpoly2=poly2-poly1
                    print("The Substraction (1-2):" ,subpoly1.evaluate(n))
                    print("The Substraction (2-1):" ,subpoly2.evaluate(n))
                    addpoly=poly1+poly2
                    print("The Addition :" , addpoly.evaluate(n))
                    print("\n Enter anykey to continue....")
                    char = getch.getch()
                    os.system('cls')
                if choice =='6':
                    os.system('cls')
                    print("\nEnter the polynomial in the form a_n, ...a_1, a_0..... ")
                    print("\nEnter the no of polynomials:")
                    n=int(input())
                    for i in range(0,n):
                        print("\nEnter the polynomial:")
                        print("\nEnter the coefficient:")
                        co = list(map(float, input("Enter multiple values: ").split()))
                        p1 = Graphical_Polynomial(co)
                        X = np.linspace(-3, 3, 50, endpoint=True)
                        F1 = p1(X)
                        plt.plot(X, F1, label="polynomial Graph")
                        plt.legend()
                        plt.show()

                    print("\n Enter anykey to continue....")
                    char = getch.getch()
                    os.system('cls')
                if choice=='7':
                    temp=False
        if ch=='2':
            os.system('cls')
            print_there(7,5,"This program is the help use calculator all the required need for given polynomial")
            print_there(8,5,"The program can determine the additive, subtractive, multiplicative and also evalution for polynomial")
            print_there(9,5,"The divison part is done for a continuous polynomial")
            print_there(10,5,"The Graphical representation is can also be given for a continuous polynomial in the program")
            print_there(11,5,"The Graphical representation is also provides various options to save the Graph image, fine points,zoon and adjust")
            print_there(15,5,"Press any key to continue....")
            char = getch.getch()

        if ch=='3':
            os.system('cls')
            print("\n Exiting...")
            time.sleep(1)
            os.system('cls')
            sys.exit(0)
