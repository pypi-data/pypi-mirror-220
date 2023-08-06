import sys
import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import splinterglyph.shamir as shamir
from splinterglyph.readable_hex import bytes_to_words, words_to_bytes

# This should be an integer
splinterglyph_version = 1


def pack_data(data):
    out = f"SPLINTERGLYPH v{splinterglyph_version:04}\n"
    out += f"Made {data['distributed_shares']:05} shares;"
    out += f" require {data['required_shares']:05}\n"
    datestr = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    out += datestr + "\n"
    out += f"Key len: {data['key_bit_length']:04}\n"
    out += f"prime_mod length: {len(data['prime_mod']):06}\n"
    out = out.encode("utf8")

    out += data["prime_mod"]
    out += data["nonce"]
    out += data["tag"]
    out += data["ciphertext"]
    return out


def unpack_data(b):
    # Quick check of magic string
    magic = b"SPLINTERGLYPH v"
    if b[: len(magic)] != magic:
        raise ValueError("Bad data format; maybe you're reading the wrong file?")

    results = {}

    sample = [
        b"SPLINTERGLYPH v0001\n",
        b"Made 00005 shares; require 00002\n",
        b"2023-06-16 20:50:27\n",
        b"Key len: 0256\n",
        b"prime_mod length: 000001\n",
    ]
    # Cumulate length of rows in bytes
    L = [len(sample[0])]
    for i in range(1, len(sample)):
        L.append(len(sample[i]) + L[i - 1])
    # Quick sanity check of parsing
    for l in L:
        assert chr(b[l - 1]) == "\n"

    index = L[0] - 5
    results["splinterglyph_version"] = int(b[index : index+4])

    # Recover number of required shares
    index = L[1] - 6
    results["required_shares"] = int(b[index : index + 5])

    # Recover the key length
    index = L[2] + len("Key len: ")
    key_bit_length = int(b[index : index + 4])
    results["key_bit_length"] = key_bit_length

    # Recover prime_mod
    index = L[4] - 7
    prime_mod_length = int(b[index : index + 6])
    index = L[4]
    results["prime_mod"] = b[index : index + prime_mod_length]

    # Recover nonce
    nonce_length = 16
    index += prime_mod_length
    results["nonce"] = b[index : index + nonce_length]

    # Recover tag
    tag_length = 16
    index += nonce_length
    results["tag"] = b[index : index + tag_length]

    # Recover ciphertext
    index += tag_length
    results["ciphertext"] = b[index:]

    return results


def encrypt(
    plain_path=None,
    crypt_path=None,
    distributed_shares=5,
    required_shares=3,
    key_bit_length=256,
):
    assert required_shares <= distributed_shares
    assert distributed_shares < 100000  # Let's not go nuts here.
    assert key_bit_length < 10000
    assert key_bit_length in [128, 192, 256]

    with open(plain_path, "rb") as fp:
        data = fp.read()

    key = get_random_bytes(key_bit_length // 8)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    nonce = cipher.nonce

    assert len(tag) == 16
    assert len(nonce) == 16
    assert len(key) == key_bit_length / 8

    data = dict(
        key_bit_length=key_bit_length,
        nonce=nonce,
        tag=tag,
        ciphertext=ciphertext,
        distributed_shares=distributed_shares,
        required_shares=required_shares,
    )

    results = shamir.split_secret(key, required_shares, distributed_shares)
    results["prime_mod"] = results["prime_mod"]

    results["human_shares"] = []
    for share in results["shares"]:
        prefix = share[0]
        share_bytes = share[1]
        results["human_shares"].append(f"{prefix}-{bytes_to_words(share_bytes)}")
    data["prime_mod"] = results["prime_mod"]

    packed = pack_data(data)

    # Write output to file
    if crypt_path is None:
        crypt_path = plain_path + ".splinterglyph"
    with open(crypt_path, "wb") as fpout:
        fpout.write(packed)

    for human_share in results["human_shares"]:
        print(human_share)
        print()
    return results


def decrypt(
    plain_path=None,
    crypt_path=None,
    key_shares=None,
):

    with open(crypt_path, "rb") as fp:
        data = unpack_data(bytes(fp.read()))

    # We expect key_shares to look something like:
    # ["1-even,thermostat,hinted,easel",
    #  "3-odd,them,harv,wut",
    #  "4-even,vdd,haul,initiation"]
    raw_shares = []
    for word_share in key_shares:
        s_list = word_share.split("-")
        point = int(s_list[0])
        # s_list should only have two items, but just in case...
        body = "-".join(s_list[1:])
        raw_shares.append((point, words_to_bytes(body)))

    shares_data = {
        "required_shares": data["required_shares"],
        "prime_mod": data["prime_mod"],
        "shares": raw_shares,
    }
    key = shamir.recover_secret(shares_data)

    cipher = AES.new(key, AES.MODE_EAX, data["nonce"])
    try:
        plain_text = cipher.decrypt_and_verify(data["ciphertext"], data["tag"])
    except ValueError as e:
        if str(e) == "MAC check failed":
            msg = "FILE TAMPERING DETECTED"
            print()
            print((8 + len(msg)) * "#")
            print(f"##  {msg}  ##")
            print((8 + len(msg)) * "#")
            print()
            raise ValueError("File tampering") from None
        raise

    if plain_path is None:
        # Write output to STDOUT
        sys.stdout.buffer.write(plain_text)
    else:
        # Write output to file
        with open(plain_path, "wb") as fpout:
            fpout.write(plain_text)
