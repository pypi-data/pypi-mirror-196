# get the range of numbers to check
lower = int(input("\n\nPrime\nEnter lower range: "))
upper = int(input("Enter upper range: "))

# function to check if a number is prime
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
    return True

# loop through the range and check for prime numbers
primes = []
for num in range(lower, upper+1):
    if is_prime(num):
        primes.append(num)

# print the prime numbers found
if len(primes) > 0:
    print("Prime numbers found:", primes)
else:
    print("No prime numbers found in the given range.")
