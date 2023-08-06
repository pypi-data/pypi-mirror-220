import argparse
import os
import sys
from passlib.hash import sha256_crypt, sha512_crypt, bcrypt, scrypt, \
    bsd_nthash, des_crypt, bigcrypt, bsdi_crypt, md5_crypt, sun_md5_crypt, \
    sha1_crypt
from pyescrypt import Yescrypt, Mode

DEFAULT_HASH_TYPE = "yescrypt"

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s", "--salt",
        help="hash salt",
        required=False,
    )

    parser.add_argument(
        "-t", "--type",
        help="hash type. Options: {}. Default: {}".format(
            ", ".join(HASHERS.keys()),
            DEFAULT_HASH_TYPE,
        ),
        metavar="TYPE",
        choices=HASHERS.keys(),
        default=DEFAULT_HASH_TYPE
    )

    parser.add_argument(
        "-r", "--rounds",
        help="hashing rounds",
        type=int
    )

    parser.add_argument(
        "password",
        help="password to hash. "
        "If none then stdin will be use",
        nargs="*",
    )


    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    crypt_hash = HASHERS[args.type]

    for password in read_text_targets(args.password):
        try:
            print(crypt_hash(
                password,
                salt=args.salt,
                rounds=args.rounds
            ))
        except ValueError as e:
            eprint("Error: %s" % e)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def sha1_crypt_hash(password, salt=None, rounds=None, **kwargs):
    return sha1_crypt.hash(password, salt=salt, rounds=rounds)

# https://www.akkadia.org/drepper/SHA-crypt.txt
def sha256_crypt_hash(password, salt=None, rounds=None, **kwargs):
    warning_unused_parameters(**kwargs)
    rounds = rounds or 5000
    return sha256_crypt.hash(password, salt=salt, rounds=rounds)

def sha512_crypt_hash(password, salt=None, rounds=None, **kwargs):
    warning_unused_parameters(**kwargs)
    rounds = rounds or 5000
    return sha512_crypt.hash(password, salt=salt, rounds=rounds)

def bcrypt_hash(password, salt=None, rounds=None, **kwargs):
    warning_unused_parameters(**kwargs)
    return bcrypt.hash(password, salt=salt, rounds=rounds)

def scrypt_hash(password, salt=None, rounds=None, **kwargs):
    warning_unused_parameters(**kwargs)
    hash_str = scrypt.hash(password, salt=salt, rounds=rounds)
    return hash_str.replace("$scrypt$", "$7$")

def yescrypt_hash(
        password,
        salt=None,
        block_count=None,
        block_size=None,
        time=None,
        **kwargs
):
    warning_unused_parameters(**kwargs)
    if time is None:
        time = 0
    if block_size is None:
        block_size = 32

    if block_count is None:
        block_count = 2 ** 12

    if salt is None:
        salt = os.urandom(16)
    return Yescrypt(
        mode=Mode.MCF,
        n=block_count,
        r=block_size,
        t=time,
    ).digest(
        password.encode(),
        salt=salt
    ).decode()

def nt_hash(password, **kwargs):
    warning_unused_parameters(**kwargs)
    return bsd_nthash.hash(password)

def des_hash(password, **kwargs):
    warning_unused_parameters(**kwargs)
    return des_crypt.hash(password)

def bigcrypt_hash(password, salt=None, **kwargs):
    warning_unused_parameters(**kwargs)
    return bigcrypt.hash(password, salt=salt)

def bsdi_crypt_hash(password, salt=None, rounds=None, **kwargs):
    warning_unused_parameters(**kwargs)
    return bsdi_crypt.hash(password, salt=salt, rounds=rounds)

def md5crypt_hash(password, salt=None, **kwargs):
    warning_unused_parameters(**kwargs)
    return md5_crypt.hash(password, salt=salt)

def sunmd5_hash(password, salt=None, rounds=None, **kwargs):
    warning_unused_parameters(**kwargs)
    if rounds is None:
        rounds = 0
    return sun_md5_crypt.hash(password, salt=salt, rounds=rounds)

def warning_unused_parameters(**kwargs):
    for k,v in kwargs.items():
        if v is not None:
            eprint(
                "Warning: '{}' parameter is not used in this hash method".format(k)
            )

HASHERS = {
    "y": yescrypt_hash,
    "yescrypt": yescrypt_hash,
    "7": scrypt_hash,
    "scrypt": scrypt_hash,
    "6": sha512_crypt_hash,
    "sha512": sha512_crypt_hash,
    "5": sha256_crypt_hash,
    "sha256": sha256_crypt_hash,
    "sha1": sha1_crypt_hash,
    "2a": bcrypt_hash,
    "2b": bcrypt_hash,
    "2x": bcrypt_hash,
    "2y": bcrypt_hash,
    "bcrypt": bcrypt_hash,
    "sunmd5": sunmd5_hash,
    "md5": sunmd5_hash,
    "1": md5crypt_hash,
    "md5crypt": md5crypt_hash,
    "3": nt_hash,
    "nt": nt_hash,
    "_": bsdi_crypt_hash,
    "bsdi_crypt": bsdi_crypt_hash,
    "bigcrypt": bigcrypt_hash,
    "des": des_hash,
}

def read_text_targets(targets):
    yield from read_text_lines(read_targets(targets))


def read_targets(targets):
    if not targets:
        yield from sys.stdin

    for target in targets:
        yield target


def read_text_lines(fd):
    for line in fd:
        line = line.strip()
        if line == "":
            continue
        if line.startswith("#"):
            continue

        yield line



if __name__ == '__main__':
    main()
