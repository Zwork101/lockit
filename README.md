# lockit

Encrypt files and folders from the command line without breaking a sweat 🔒📁📄

Lockit is a very simple program for a very simple purpose. Encrypt files / folders with any password. Let me show you.

```bash
$ touch hello.txt
$ echo "Hello World" > hello.txt
$ lock hello.txt
Password: MyPassword
Confirm Password: MyPassword
$ ls
hello.txt.lck
$ cat hello.txt.lck
夒▒V▒▒6▒▒▒.▒▒
$ lock hello.txt.lck
Password: MyPassword
$ ls
hello.txt
$ cat hello.txt
Hello World
```

Keep in mind, I used a file. You can do the same with a folder with all the same commands.

```bash
$ mkdir hello
$ cd hello
$ touch test.txt
$ echo "Works with directories!" > test.txt
$ cd ..
$ lock hello
Password: Secure Folder
Confirm Password: Secure Folder
$ ls
hello.lck
$ lock hello.lck
Password: Secure Folder
$ cd hello
$ cat test.txt
Works with directories!
```

## Installing

How do you think?

```bash
$ pip install lockit  # Do this on windows if you only have 1 python installed
$ pip3 install lockit  # Do this on linux
$ py -version_here -m pip install lockit  # Python version specific installation for windows
```

## TODO:

* Hide passwords (Multi-platform)

* Better cli

* Decaprecate cache system

* Check if password worked

### All suggestions and pulls are welcome!
