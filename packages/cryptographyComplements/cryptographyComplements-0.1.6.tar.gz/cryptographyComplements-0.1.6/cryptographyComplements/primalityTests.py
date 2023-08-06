from cryptographyComplements.tools import isNumber, isEven
def EulerTotientPrimalityTest(n: int):
    "Using the equation: p - 1 = phi(p), you can verify if a number is prime. \nThis primality test is 100% valid but numbers greater than 2^60 requires to much time, and computational power, to be calculated using this primality test."

    from cryptographyComplements.mathFunctions import EulerTotientFunction

    if not isNumber(n): # verifying if the input is a number 
        return False

    elif int(n) < 0: # verifying if the input belongs to N
        print("Cryptography Complements: The number entered is not a prime")
        return False

    n = int(n)
    if n == 5 or n==2: # this needs to be put because in the if condition below it would be set to false
        print("Cryptography Complements: The number entered is prime")
        return True
    

    elif isEven(n) or str(n).endswith("5"): # this skips all the nums that are not prime
        print("Cryptography Complements: The number entered is not a prime")
        return False

    phi = EulerTotientFunction(n)

    if (n - 1) == phi:
        print("Cryptography Complements: The number entered is prime")
        return True
    
    print("Cryptography Complements: The number entered is not a prime")
    return False