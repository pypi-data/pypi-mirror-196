# get the range of numbers to check
lower = int(input("\n\nPalindrome\nEnter lower range: "))
upper = int(input("Enter upper range: "))

# function to check if a number is a palindrome
def is_palindrome(num):
    return str(num) == str(num)[::-1]

# loop through the range and check for palindromic numbers
palindromes = []
for num in range(lower, upper+1):
    if is_palindrome(num):
        palindromes.append(num)

# print the palindromic numbers found
if len(palindromes) > 0:
    print("Palindromic numbers found:", palindromes)
else:
    print("No palindromic numbers found in the given range.")
