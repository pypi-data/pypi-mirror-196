from cryptographyComplements.mathFunctions import EulerTotientFunction
from cryptographyComplements.tools import isNumber
def EulerTotientPrimalityTest(n: int):
    "Using the equation: p - 1 = phi(p), you can verify if a number is prime. \nThis primality test is 100% valid but numbers greater than 2^60 requires to much time, and computational power, to be calculated using this primality test."

    if n < 0 and not isNumber(n): # verifying if the input is a number and belongs to N
        return None
    

    phi = EulerTotientFunction(n)

    if (n - 1) == phi:
        print("Cryptography Complements: The number entered is prime")
        return True
    
    print("Cryptography Complements: The number entered is not a prime")
    return False