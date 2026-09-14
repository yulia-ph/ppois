import polynomial


def show_menu():
    """Print the main menu."""
    print("-------------MENU-------------")
    print("1. Show all saved polynomials")
    print("2. Add polynomial")
    print("3. Show polynomial")
    print("4. Delete polynomial")
    print("5. Enter operation with polynomials")
    print("0. Exit")
    print("------------------------------")

def evaluate_expression(expression, polynomials):
    """Evaluate an expression on the polynomial storage.

    Supports plain expressions ('a + b'), assignments ('c = a + b'),
    and in-place operators ('a += b'). Returns the resulting Polynomial.
    """
    expression = expression.strip()

    if "=" in expression:
        lhs = expression.split("=", 1)[0]
        name = lhs.rstrip("+-*/").strip()
        exec(expression, {"__builtins__": {}}, polynomials) # noqa: S102
        return polynomials[name]

    return eval(expression, {"__builtins__": {}}, polynomials)

def main():
    polynomials = {}
    while True:
        show_menu()
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                print("----------POLYNOMIALS---------")
                for k, v in polynomials.items():
                    print(f"{k} : {v}")

            case "2":
                key = input("Enter variable's name: ").strip()
                if not key:
                    print("Error: variable name cannot be empty")
                    continue
                if not key.isidentifier():
                    print(f"Error: '{key}' is not a valid identifier")
                    continue

                try:
                    coefficients = input("Enter polynomial's coefficients: ").split()
                    poly = polynomial.Polynomial(coefficients)
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
                    continue

                if key in polynomials:
                    print(f"Warning: '{key}' already exists and will be overwritten")
                polynomials[key] = poly

            case "3":
                key = input("Enter variable's name: ").strip()
                try:
                    print(f"{key} : {polynomials[key]}")
                except KeyError:
                    print(f"Error: '{key}' is not defined")

            case "4":
                key = input("Enter variable's name: ").strip()
                try:
                    del polynomials[key]
                    print(f"'{key}' deleted")
                except KeyError:
                    print(f"Error: '{key}' is not defined")

            case "5":
                expression = input("Enter expression: ")
                if not expression:
                    print("Error: empty expression")
                    continue
                try:
                    print(evaluate_expression(expression, polynomials))
                except (SyntaxError, NameError, KeyError, ValueError, TypeError, ZeroDivisionError) as e:
                    print(f"Error: {e}")
            case "0":
                print("Exiting...")
                break
            case _:
                print("Input error")

if __name__ == '__main__':
    main()