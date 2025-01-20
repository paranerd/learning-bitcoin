# Signing Bitcoin Transactions

[Source](https://learnmeabitcoin.com/technical/keys/signature/)

This shows how to sign and verify a Bitcoin transaction. It also highlights the importance of using (and not re-using!) a random nonce by showcasing private key recovery.

## Glossary

$G$ = Generator point

$Q$ = Public key

$R$ = Random point

$k$ = Nonce

$m$ = Message

$z$ = Message hash

$x$ = Private key

$s$ = Second half of signature

$r$ = x-coordinate of random point

## Signing

1. Generate a random(!) nonce $k$

1. Use $k$ to get a random point on the curve

    $R = k * G$

1. Use $R$ to get the first half of the signature

    $r$ = The x-coordinate of $R$

    If $r$ is 0, we need to start over

1. Get second half of the signature

    $s = \frac{(z + r * d)}{k}$

    If $s$ is 0, we need to start over

## Verification

[Source](https://learnmeabitcoin.com/technical/cryptography/elliptic-curve/ecdsa/#verify)

[Source](https://medium.com/coinmonks/ecdsa-the-art-of-cryptographic-signatures-d0bb254c8b96)

To verify an ECDSA signature, we need to calculate a point on the curve and show that the x-coordinate of that point is the same as the $r$ value taken from the signature.

1. General equation to calculate a point on the curve

    $R = k * G$

    The problem is that the verifier doesn't know $k$

1. Substitute $k$

    When signing a message, we used

    $s = \frac{(z + r * d)}{k}$

    => Multiply by $k$ and divide by $s$:

    $k = \frac{(z + r * d)}{s}$

    Substitute k in equation (1)

    $R = \frac{(z + r * d)}{s} * G$

1. Substitute $d$

    The verifyer doesn't have the private key $d$, but they can leverage the fact that $d * G = Q$

    To do that we first need to rewrite the equation:

    $R = \frac{z * G}{s} + \frac{r * d * G}{s}$

    Now substitute $d$:

    $R = \frac{z * G}{s} + \frac{r * Q}{s}$

1. Verify

    $x_R == r$

    If this condition is true, the signature is valid.

## Private key recovery

[Source](https://crypto.stackexchange.com/questions/57846/recovering-private-key-from-secp256k1-signatures)

[Source](https://github.com/pcaversaccio/ecdsa-nonce-reuse-attack/blob/main/scripts/recover_private_key.py)

If the the nonce is used in two signatures for two distinct messages but with the same private key, then that private key is revealed.

### Calcule the nonce

1. Starting off with the formula to compute a signature

    $s = \frac{z + xr}{k}$

1. Multiply with $k$:

    $s * k = z + xr$

1. Subtract $z$:

    $(s * k) - z = xr$

1. Do the same for a second signature:

    $(s_2 * k) - z_2 = xr$

1. Set both equal

    Because we expect $x$ to be equal and the $r$ values of two signatures are identical if the same $k$ is used:

    $(s_1 * k) - z_1 = (s_2 * k) - z_2$

1. Subtract $z_1$ and $(s_2 * k)$ to swap sides:

    $(s_1 * k) - (s_2 * k) = z_1 - z_2$

1. Get $k$ out of the parantheses:

    $(s_1 - s_2) * k = z_1 - z_2$

1. Divide by $(s_1 - s_2)$:

    $k = \frac{z_1 - z_2}{s_1 - s_2}$

### Use the nonce to calculate the private key

1. Again, starting off with the formula to compute a signature

    This time eventually solving for $x$

    $s = \frac{z + xr}{k}$

1. Multiply with $k$:

    $s * k = z + xr$

1. Subtract $z$

    $(s * k) - z = xr$

1. Divide by $r$

    $x = \frac{(s * k) - z}{r}$