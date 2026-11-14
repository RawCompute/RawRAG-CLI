
while True:
    num1 = float(input("Enter first number: "))
    operator = input("Enter operator (+, -, *, /): ")
    num2 = float(input("Enter second number: "))

    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num2 == 0:
            print("Cannot divide by zero!")
            continue
        result = num1 / num2
    else:
        print("Invalid operator!")
        continue

    print("Result:", result)

    choice = input("Continue? (y/n): ")
    if choice.lower() != "y":
        break
