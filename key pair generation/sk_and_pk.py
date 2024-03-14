import random
from dataclasses import dataclass

@dataclass
class Curve:
  p: int
  a: int
  b: int

#see https://en.bitcoin.it/w/index.php?title=Secp256k1 for the hex of each parameter
bitcoin_curve = Curve(
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    a = 0x0000000000000000000000000000000000000000000000000000000000000000,
    b = 0x0000000000000000000000000000000000000000000000000000000000000007
)

@dataclass
class Point:
  curve: Curve
  x: int
  y: int


G = Point(bitcoin_curve,
          x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
          y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


#Check whether G is on the curve
print('Generator is on the curve - true or false:', (G.y**2 - G.x**3-7) % bitcoin_curve.p == 0)


@dataclass
class Generator:
  G: Point
  n: int

bitcoin_gen = Generator(
    G=G,
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
)


#generate secret key (sk) - THIS IS NOT A SECURE WAY OF DOING IT. IT'S JUST FOR EDUCATIONAL PURPOSE! 
sk = random.randrange(1, bitcoin_gen.n)
assert 1 <= sk < bitcoin_gen.n # check whether sk is truly between 1 and n 
print(sk)


#Elliptic curve addition and multiplication

INF = Point(None, None, None) # special point at "infinity", kind of like a zero

def extended_euclidean_algorithm(a, b):
    """
    Returns (gcd, x, y) such that a * x + b * y == gcd(a,b) (größter gemeinsamer Teiler)
    This function implements the extended Euclidean
    algorithm and runs in O(log b) in the worst case,
    taken from Wikipedia.
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s, old_t

def inv(n, p):
    """ returns modular multiplicate inverse m s.t. (n * m) % p == 1 """
    gcd, x, y = extended_euclidean_algorithm(n, p) # pylint: disable=unused-variable
    return x % p

def elliptic_curve_addition(self, other: Point) -> Point:
    # handle special case of P + 0 = 0 + P = 0
    if self == INF:
        return other
    if other == INF:
        return self
    # handle special case of P + (-P) = 0
    if self.x == other.x and self.y != other.y:
        return INF
    # compute the "slope"
    if self.x == other.x: # (self.y = other.y is guaranteed too per above check)
        m = (3 * self.x**2 + self.curve.a) * inv(2 * self.y, self.curve.p)
    else:
        m = (self.y - other.y) * inv(self.x - other.x, self.curve.p)
    # compute the new point
    rx = (m**2 - self.x - other.x) % self.curve.p
    ry = (-(m*(rx - self.x) + self.y)) % self.curve.p
    return Point(self.curve, rx, ry)

Point.__add__ = elliptic_curve_addition # monkey patch addition into the Point class


def double_and_add(self, k: int) -> Point:
    assert isinstance(k, int) and k >= 0
    result = INF
    append = self
    while k:
        if k & 1:
            result += append
        append += append
        k >>= 1
    return result

Point.__rmul__ = double_and_add


#generate public key (pk) by multiplying sk with G
pk = sk*G
print(pk)

#Check whether point is on the curve
print('Point of pk is on the curve - true or false:', (pk.y**2 - pk.x**3-7) % bitcoin_curve.p == 0)





