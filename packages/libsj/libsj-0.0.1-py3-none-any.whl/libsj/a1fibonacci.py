# get the range of numbers to generate Fibonacci sequence
lower = int(input("\n\nFibonacci\nEnter lower range: "))
upper = int(input("Enter upper range: "))

# generate Fibonacci sequence within the range
is_fibonacci = []
a, b = 0, 1
while b <= upper:
    if b >= lower:
        is_fibonacci.append(b)
    a, b = b, a+b

# print the Fibonacci sequence found
if len(is_fibonacci) > 0:
    print("Fibonacci sequence found:", is_fibonacci)
else:
    print("No Fibonacci sequence found in the given range.")
