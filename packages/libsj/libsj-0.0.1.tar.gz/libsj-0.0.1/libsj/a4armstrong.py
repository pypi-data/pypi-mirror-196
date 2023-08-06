def armstrong_range(lower, upper):
    """
    Generates Armstrong numbers within a given range
    """
    armstrong_nums = []
    for num in range(lower, upper+1):
        digits = [int(d) for d in str(num)]
        sum_of_digits = sum([d**len(digits) for d in digits])
        if sum_of_digits == num:
            armstrong_nums.append(num)
    return armstrong_nums

# Take user input for lower and upper range
lower = int(input("\n\nArmstrong\nEnter lower range: "))
upper = int(input("Enter upper range: "))

# Call the function to get Armstrong numbers within the range
armstrong_nums = armstrong_range(lower, upper)

# Print the Armstrong numbers within the range
print("Armstrong numbers between", lower, "and", upper, "are:")
for num in armstrong_nums:
    print(num)
