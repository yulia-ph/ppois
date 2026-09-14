class Polynomial:
    """A polynomial with coefficients ordered from highest to lowest degree.

    Internally stores them from lowest to highest degree:
    _coefficients[i] is the coefficient of x^i.
    """

    def __init__(self, coefficients):
        """Initialize the polynomial from an iterable of coefficients.

            Raises:
                TypeError: if any coefficient is not an int or float.
            """
        self._coefficients = self.validate_data(coefficients)

    @classmethod
    def validate_data(cls, coefficients):
        """Validate and normalize raw input coefficients.

            Returns:
                A list of coefficients ordered from lowest to highest degree,
                with trailing zeros removed.
            Raises:
                TypeError: if any coefficient is not an int or float.
            """
        if not coefficients:
            return [0]

        coef = [float(c) for c in reversed(coefficients)]
        coef = cls.trim(coef)

        return coef

    @staticmethod
    def trim(coefficients):
        """Remove trailing zero coefficients, keeping at least one element.

            Returns:
                The same list with trailing zeros removed.
            """
        while len(coefficients) > 1 and coefficients[-1] == 0:
            coefficients.pop()

        return coefficients

    def __str__(self):
        """Return a human-readable string representation of the polynomial."""
        if not self._coefficients:
            return "0"

        res = []
        for i, c in enumerate(self._coefficients):
            if c == 0:
                continue
            elif i == 0:
                res.append(f"{c}")
            elif i == 1:
                if abs(c) == 1:
                    res.append("-x" if c < 0 else "x")
                else:
                    res.append(f"{c}x")
            else:
                if abs(c) == 1:
                    res.append(f"-x^{i}" if c < 0 else f"x^{i}")
                else:
                    res.append(f"{c}x^{i}")

        if not res:
            return "0"

        res.reverse()
        return " + ".join(res).replace("+ -", "- ")

    @classmethod
    def _from_internal(cls, coefficients):
        """Build a polynomial from internal-ordered coefficients.

            Bypasses __init__ and assumes coefficients are already
            ordered from lowest to highest degree.
            """
        new_poly = cls.__new__(cls)
        coefficients = cls.trim(coefficients)
        new_poly._coefficients = coefficients
        return new_poly

    def __add__(self, other):
        """Return the sum of two polynomials.

            Raises:
                TypeError: if other is not a Polynomial.
            """
        if not isinstance(other, Polynomial):
            raise TypeError(f"Cannot add Polynomial with {type(other)}")

        coef1 = self._coefficients
        coef2 = other._coefficients
        n = max(len(coef1), len(coef2))
        coef = [(coef1[i] if i < len(coef1) else 0) + (coef2[i] if i < len(coef2) else 0) for i in range(n)]

        return self._from_internal(coef)

    def __sub__(self, other):
        """Return the difference of two polynomials.

            Raises:
                TypeError: if other is not a Polynomial.
            """
        if not isinstance(other, Polynomial):
            raise TypeError(f"Cannot subtract {type(other)} from Polynomial")

        coef1 = self._coefficients
        coef2 = other._coefficients
        n = max(len(coef1), len(coef2))
        coef = [(coef1[i] if i < len(coef1) else 0) - (coef2[i] if i < len(coef2) else 0) for i in range(n)]

        return self._from_internal(coef)

    def __mul__(self, other):
        """Return the product of two polynomials.

            Raises:
                TypeError: if other is not a Polynomial.
            """
        if not isinstance(other, Polynomial):
            raise TypeError(f"Cannot multiply Polynomial by {type(other)}")

        n = len(self._coefficients) + len(other._coefficients) -1
        res = [0] * n

        for i, c1  in enumerate(self._coefficients):
            for j, c2 in enumerate(other._coefficients):
                res[i+j] += c1 * c2

        return self._from_internal(res)

    def __getitem__(self, degree):
        """Return the coefficient of x^degree.

            Returns:
                The coefficient, or 0 if degree is out of range.
            Raises:
                TypeError: if degree is not an int.
            """
        if not isinstance(degree, int):
            raise TypeError("Degree must be an integer")

        if degree < 0 or degree >= len(self._coefficients):
            return 0

        return self._coefficients[degree]

    def __call__(self, x):
        """Evaluate the polynomial at x using Horner's scheme.

            Raises:
                TypeError: if x is not an int or float.
            """
        if not isinstance(x, (int, float)):
            raise TypeError("X must be an integer or float")

        result = 0
        for c in reversed(self._coefficients):
            result = result * x + c

        return result

    def __divmod__(self, other):
        """Return (quotient, remainder) of polynomial division.

            Returns:
                A tuple (Q, R) such that self == other * Q + R
                and degree(R) < degree(other).
            Raises:
                TypeError: if other is not a Polynomial.
                ZeroDivisionError: if other is the zero polynomial.
            """
        if not isinstance(other, Polynomial):
            raise TypeError(f"Cannot divide Polynomial by {type(other)}")
        if other._coefficients == [0]:
            raise ZeroDivisionError("Division by the zero polynomial")

        dividend = list(self._coefficients)
        divisor = other._coefficients

        if len(dividend) < len(divisor):
            return self._from_internal([0]), self._from_internal(dividend)

        quotient = [0] * (len(dividend) - len(divisor) + 1)

        while len(dividend) >= len(divisor) and not (len(dividend) == 1 and dividend[0] == 0):

            coef = dividend[-1] / divisor[-1]
            degree_diff = len(dividend) - len(divisor)
            quotient[degree_diff] = coef

            for i in range(len(divisor)):
                dividend[degree_diff + i] -= coef * divisor[i]

            while len(dividend) > 1 and dividend[-1] == 0:
                dividend.pop()

        return self._from_internal(quotient), self._from_internal(dividend)

    def __truediv__(self, other):
        """Return the quotient of polynomial division."""
        q, _ = divmod(self, other)
        return q

    def __mod__(self, other):
        """Return the remainder of polynomial division."""
        _, r = divmod(self, other)
        return r

    def __iadd__(self, other):
        """In-place addition. Updates self and returns it."""
        self._coefficients = (self + other)._coefficients
        return self

    def __isub__(self, other):
        """In-place subtraction. Updates self and returns it."""
        self._coefficients = (self - other)._coefficients
        return self

    def __imul__(self, other):
        """In-place multiplication. Updates self and returns it."""
        self._coefficients = (self * other)._coefficients
        return self

    def __itruediv__(self, other):
        """In-place division. Updates self and returns it."""
        self._coefficients = (self / other)._coefficients
        return self
