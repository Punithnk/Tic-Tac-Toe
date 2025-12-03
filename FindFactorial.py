def main():
    try:
        number = int(input("Enter a positive integer: "))
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    if number <= 0:
        print("Please enter a positive integer greater than zero.")
        return

    factors = []
    limit = int(number ** 0.5)
    for i in range(1, limit + 1):
        if number % i == 0:
            factors.append(i)
            paired = number // i
            if paired != i:
                factors.append(paired)

    factors.sort()
    factor_list = ", ".join(str(factor) for factor in factors)
    print(f"Factors of {number} are: {factor_list}")


if __name__ == "__main__":
    main()

