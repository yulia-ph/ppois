import pytest

from polynomial import Polynomial


def coeffs(p):
    return p._coefficients


class TestInit:
    def test_empty_list_gives_zero(self):
        assert coeffs(Polynomial([])) == [0.0]

    def test_single_coefficient(self):
        assert coeffs(Polynomial([5])) == [5.0]

    def test_input_order_high_to_low(self):
        assert coeffs(Polynomial([1, 2, 3])) == [3.0, 2.0, 1.0]

    def test_leading_zeros_trimmed(self):
        assert coeffs(Polynomial([0, 0, 1, 2])) == [2.0, 1.0]

    def test_all_zeros_collapse_to_single(self):
        assert coeffs(Polynomial([0, 0, 0])) == [0.0]

    def test_string_coefficients_accepted(self):
        assert coeffs(Polynomial(["1", "2", "3"])) == [3.0, 2.0, 1.0]

    def test_invalid_string_raises(self):
        with pytest.raises(ValueError):
            Polynomial(["abc"])

    def test_invalid_type_raises(self):
        with pytest.raises((ValueError, TypeError)):
            Polynomial([None])


class TestTrim:
    def test_trims_trailing_zeros(self):
        assert Polynomial.trim([1, 2, 0, 0]) == [1, 2]

    def test_keeps_one_zero(self):
        assert Polynomial.trim([0, 0, 0]) == [0]

    def test_empty_list_unchanged(self):
        assert Polynomial.trim([]) == []


class TestStr:
    def test_zero(self):
        assert str(Polynomial([0])) == "0"

    def test_constant(self):
        assert str(Polynomial([5])) == "5.0"

    def test_linear(self):
        assert str(Polynomial([1, 2])) == "x + 2.0"

    def test_linear_negative_one(self):
        assert str(Polynomial([-1, 2])) == "-x + 2.0"

    def test_quadratic(self):
        assert str(Polynomial([1, 2, 3])) == "x^2 + 2.0x + 3.0"

    def test_negative_coefficients(self):
        assert str(Polynomial([1, -2, 3])) == "x^2 - 2.0x + 3.0"

    def test_skips_zero_coefficients(self):
        assert str(Polynomial([1, 0, 3])) == "x^2 + 3.0"

    def test_negative_one_high_degree(self):
        assert str(Polynomial([-1, 0, 1])) == "-x^2 + 1.0"

    def test_leading_minus(self):
        assert str(Polynomial([1, 2, -3])) == "x^2 + 2.0x - 3.0"

    def test_empty_internal_list(self):
        p = Polynomial._from_internal([])
        assert str(p) == "0"


class TestFromInternal:
    def test_from_internal_basic(self):
        p = Polynomial._from_internal([3.0, 2.0, 1.0])
        assert coeffs(p) == [3.0, 2.0, 1.0]

    def test_from_internal_trims(self):
        p = Polynomial._from_internal([1.0, 2.0, 0.0, 0.0])
        assert coeffs(p) == [1.0, 2.0]


class TestAdd:
    def test_simple(self):
        p = Polynomial([1, 2]) + Polynomial([1, 3])
        assert coeffs(p) == [5.0, 2.0]

    def test_different_lengths(self):
        p = Polynomial([1, 2, 3]) + Polynomial([1])
        assert coeffs(p) == [4.0, 2.0, 1.0]

    def test_cancellation(self):
        p = Polynomial([1, 2, 3]) + Polynomial([-1, -2, -3])
        assert coeffs(p) == [0.0]

    def test_type_error(self):
        with pytest.raises(TypeError):
            Polynomial([1]) + 5


class TestSub:
    def test_simple(self):
        p = Polynomial([3, 5]) - Polynomial([1, 2])
        assert coeffs(p) == [3.0, 2.0]

    def test_result_trimmed(self):
        p = Polynomial([1, 3]) - Polynomial([1, 2])
        assert coeffs(p) == [1.0]

    def test_self_sub_gives_zero(self):
        p = Polynomial([1, 2, 3]) - Polynomial([1, 2, 3])
        assert coeffs(p) == [0.0]

    def test_type_error(self):
        with pytest.raises(TypeError):
            Polynomial([1]) - 5


class TestMul:
    def test_simple(self):
        p = Polynomial([1, 1]) * Polynomial([1, 1])
        assert coeffs(p) == [1.0, 2.0, 1.0]

    def test_by_zero(self):
        p = Polynomial([1, 2]) * Polynomial([0])
        assert coeffs(p) == [0.0]

    def test_by_constant(self):
        p = Polynomial([1, 2]) * Polynomial([3])
        assert coeffs(p) == [6.0, 3.0]

    def test_type_error(self):
        with pytest.raises(TypeError):
            Polynomial([1]) * 5


class TestGetItem:
    def test_valid_indices(self):
        p = Polynomial([1, 2, 3])
        assert p[0] == 3.0
        assert p[1] == 2.0
        assert p[2] == 1.0

    def test_out_of_range_returns_zero(self):
        p = Polynomial([1, 2, 3])
        assert p[5] == 0

    def test_negative_returns_zero(self):
        p = Polynomial([1, 2, 3])
        assert p[-1] == 0

    def test_non_integer_raises(self):
        p = Polynomial([1])
        with pytest.raises(TypeError):
            p[1.5]


class TestCall:
    def test_values(self):
        p = Polynomial([1, 2, 3])
        assert p(0) == 3.0
        assert p(1) == 6.0
        assert p(2) == 11.0

    def test_negative_argument(self):
        p = Polynomial([1, 2, 3])
        assert p(-1) == 2.0

    def test_float_argument(self):
        p = Polynomial([1, 0])
        assert p(2.5) == 2.5

    def test_type_error(self):
        with pytest.raises(TypeError):
            Polynomial([1])("abc")


class TestDivMod:
    def test_exact_division(self):
        p = Polynomial([1, 0, -1])
        q = Polynomial([1, -1])
        quotient, remainder = divmod(p, q)
        assert coeffs(quotient) == [1.0, 1.0]
        assert coeffs(remainder) == [0.0]

    def test_with_remainder(self):
        p = Polynomial([1, 2, 3])
        q = Polynomial([1, 1])
        quotient, remainder = divmod(p, q)
        assert coeffs(quotient) == [1.0, 1.0]
        assert coeffs(remainder) == [2.0]

    def test_dividend_shorter(self):
        p = Polynomial([1])
        q = Polynomial([1, 1])
        quotient, remainder = divmod(p, q)
        assert coeffs(quotient) == [0.0]
        assert coeffs(remainder) == [1.0]

    def test_zero_dividend_same_length(self):
        p = Polynomial([0])
        q = Polynomial([5])
        quotient, remainder = divmod(p, q)
        assert coeffs(quotient) == [0.0]
        assert coeffs(remainder) == [0.0]

    def test_division_by_zero_polynomial(self):
        with pytest.raises(ZeroDivisionError):
            divmod(Polynomial([1, 2]), Polynomial([0]))

    def test_type_error(self):
        with pytest.raises(TypeError):
            divmod(Polynomial([1]), 5)

    def test_same_degree(self):
        p = Polynomial([3, 5])
        q = Polynomial([2, 1])
        quotient, remainder = divmod(p, q)
        assert coeffs(quotient) == [1.5]
        assert coeffs(remainder) == [3.5]

    def test_identity_restores_dividend(self):
        p = Polynomial([2, -3, 1, 4])
        q = Polynomial([1, -2])
        quotient, remainder = divmod(p, q)
        restored = q * quotient + remainder
        assert coeffs(restored) == coeffs(p)


class TestTrueDiv:
    def test_truediv_returns_quotient(self):
        p = Polynomial([1, 0, -1]) / Polynomial([1, -1])
        assert coeffs(p) == [1.0, 1.0]


class TestMod:
    def test_mod_returns_remainder(self):
        p = Polynomial([1, 2, 3]) % Polynomial([1, 1])
        assert coeffs(p) == [2.0]


class TestInPlace:
    def test_iadd(self):
        p = Polynomial([1, 2])
        p += Polynomial([1, 3])
        assert coeffs(p) == [5.0, 2.0]

    def test_isub(self):
        p = Polynomial([1, 3])
        p -= Polynomial([1, 1])
        assert coeffs(p) == [2.0]

    def test_imul(self):
        p = Polynomial([1, 1])
        p *= Polynomial([1, 1])
        assert coeffs(p) == [1.0, 2.0, 1.0]

    def test_itruediv(self):
        p = Polynomial([1, 0, -1])
        p /= Polynomial([1, -1])
        assert coeffs(p) == [1.0, 1.0]