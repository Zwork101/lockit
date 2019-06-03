from argparse import ArgumentParser
from pathlib import Path
from shutil import unpack_archive
from os import remove, rename

from lock.cache import Cache
from lock.encrypt import EncryptedFile
from lock.tools import get_password, ensure_file


def encrypt_file(file_path: Path):
    cache.set_path(str(file_path.absolute()), Cache.DIRECTORY if file_path.is_dir() else Cache.FILE)
    real_path = ensure_file(file_path)
    password = get_password()
    enc_file = EncryptedFile(str(file_path.absolute()), password)
    enc_file.transfer_file(real_path)


def decrypt_file(file_path: Path, file_type: str=None):
    typ = cache.pop_type(str(file_path.absolute())[:-4])
    if typ == cache.UNKNOWN and file_type is None:
        print("Unable to find file type. Please specify the type with --type and try again.")
        exit(1)
    if not file_path.exists():
        print("Unable to find file provided.")
        exit(1)
    password = input("Password: ")
    enc_file = EncryptedFile(str(file_path.absolute()), password)
    file = enc_file.unpack_file()
    if typ == cache.DIRECTORY or (file_type is not None and file_type[0].lower() == "d"):
        new_file = file + ".archive"
        rename(file, new_file)
        unpack_archive(new_file, format="gztar", extract_dir=str(Path(file).parent))
        remove(new_file)


cache = Cache()

parser = ArgumentParser("lock")
parser.add_argument("file", type=Path, help="Target file that will be encrypted / decrypted")
parser.add_argument("--mode", help="Specify encryption / decryption (Otherwise checks for .lck file extension)")
parser.add_argument("--type", help="Specify if it's a file or directory (Not necessary unless told otherwise)")

def main():

    args = parser.parse_args()

    if args.mode and args.mode[0].lower() == "e":
        encrypt_file(args.file)
    elif args.mode and args.mode[0].lower() == "d":
        decrypt_file(args.file, None if "type" not in args else args.type)
    else:
        if args.file.name.endswith(".lck"):
            decrypt_file(args.file, None if "type" not in args else args.type)
        else:
            encrypt_file(args.file)
