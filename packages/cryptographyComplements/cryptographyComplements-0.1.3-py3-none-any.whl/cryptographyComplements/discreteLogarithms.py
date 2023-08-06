def shanksNO(n, g, h):
    """Algoritmo di Shanks per trovare la soluzione x alla congruenza g^x ≡ h (mod n)"""
    
    m = int(n ** 0.5) + 1
    
    # Precalcolo le liste L1 e L2
    L1 = [pow(g, j, n) for j in range(m)]
    L2 = [pow(g, m*i, n) for i in range(m)]
    
    # Calcolo le intersezioni tra L1 e L2
    for i in range(m):
        y = (h * pow(L1[i], n-2, n)) % n  # Calcolo y = h*L1[i]^(n-2) mod n
        if y in L2:
            j = L2.index(y)
            return i*m + j
    
    return None  # Se non ho trovato una soluzione, restituisco None





from cryptographyComplements.functions import EulerTotientFunction
from math import sqrt

def calculateOrder(g, p):
    k = 1
    order = 0
    while order != 1:
        order = (g**k) % p
        k += 1
    
    return int(k-1) # -1 needs to be added because +1 will be added even if the order is 1, because the iteration when order becomes 1 is not completed yet.

def shanks(g, h, p):

    n = 1 + int(sqrt(calculateOrder(g, p)))
    list1 = []

    for i in range(0, n):
        num = g**i
        list1.append(num)

    # print(list1)

    list2 = []

    print(n**n)

    num = 0
    i = 1
    # for i in range(0, n**n):
    check = num**num
    flag = True

    # while num != num**num:
    while flag:
        tempN = n**-i
        tempG = g**tempN

        num = h*tempG

        list2.append(num)
        i += 1

        if num == check:
            flag = False

    print(list2)