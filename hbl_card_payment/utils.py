def pad_amount(amt):
    amount_in_cents = int((amt if amt is not None else 0) * 100)
    padded_amount = str(amount_in_cents).zfill(12)
    return padded_amount


def get_private_key(key: str):
    private_key = (
        f"-----BEGIN RSA PRIVATE KEY-----\n{key}\n-----END RSA PRIVATE KEY-----"
    )
    return private_key


def get_public_key(key: str):
    public_key = f"-----BEGIN PUBLIC KEY-----\n{key}\n-----END PUBLIC KEY-----"
    return public_key
