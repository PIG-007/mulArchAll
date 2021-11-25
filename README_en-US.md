# mulArchAll

Language: [English](https://github.com/PIG-007/mulArchAll/blob/master/README_en-US.md) | [中文简体](https://github.com/PIG-007/mulArchAll/blob/master/README.md)

Establish a heterogeneous PWN environment, and solve the problem of poor debugging of qemu and pie in a heterogeneous environment. Load all symbol tables, and use heap commands, heap, bins, etc., to facilitate problem solving.

## Pre-installation

Need to install pwndbg and gef.

## Install

```bash
cd
git clone https://github.com/PIG-007/mulArchAll.git
#git clone https://gitee.com/Piggy007/mulArchAll.git
cd mulArchAll
chmod a+x setup.sh
./setup.sh
```

### Compiler Environment

Just run the corresponding command directly after installation

![image-20211125155049704](https://pig-007.oss-cn-beijing.aliyuncs.com/img/20211125155148.png)

### Illustrate

I need to talk about it here. Due to future needs, I directly overwrite the gdb startup script `.gdbinit`, and the coverage file is obtained from `~/mulArchAll/gdbinit/`.

#### Plugin loading

```bash
source ~/pwndbg/gdbinit.py
#source ~/peda/peda.py
#source ~/gef/gef.py
source ~/Pwngdb/pwngdb.py
source ~/Pwngdb/angelheap/gdbinit.py
```

If the location of the relevant plug-in is different, please change it after installation.

#### Command load 

```bash
source ~/mulArchAll/gdbCMD/getAddrAll.py
source ~/mulArchAll/gdbCMD/add-symbol-fill-all.py
```

The command for this startup script is a command written by myself to find the address and load symbols. It has no effect, but the corresponding python3 also needs to be installed relative to the package to complete the loading. The required packages are as follows, otherwise the command loading cannot be completed, and an error will occur , Please manually pip to install python3.

```python
import re
import os
import subprocess
from time import sleep
```

## Instructions

### 1. Commands added by gdb

`getAllAddr`：

![image-20211124225014181](https://pig-007.oss-cn-beijing.aliyuncs.com/img/20211124225014.png)

That is, four parameters are given, namely the libc file path, the elf architecture category, the offset of the got table of the `__libc_start_mian_` function in elf, and gdbtool.

Setting gdbtool to pwndbg will keep the current gdb command line, and entering gef will exit.

(The reason why the got table is not automatically obtained here is that the got table of the mips architecture cannot find the corresponding got table offset using the ELF function. I don't know how to solve it, so I choose to add it manually here, but we will definitely IDA when we do pwn Open, find the given directly)

The got offset address similar to the red box below is the elf file, not the so file.

![image-20211124225332532](https://pig-007.oss-cn-beijing.aliyuncs.com/img/20211124225332.png)

#### 🔺Note:

This function is based on pwndbg's vmmap function, which can get the corresponding elf base address, otherwise it can't be used. The recent pwndbg's vmmap doesn't seem to work well?

Or after knowing the elf base address, you can directly breakpoint in the main function, and then get the real address of the function in the got table of the `__libc_start_mian_` function, write the address into the `addrAll.txt` of the current file path, and then the following situation.

`add-symbol-file-all`：

After referring to the script of the following URL, I changed some

[gdb add-symbol-file all sections and load address - Stack Overflow](https://stackoverflow.com/questions/33049201/gdb-add-symbol-file-all-sections-and-load-address)

This command originally needs to pass in the address, but it has been modified here to get it from the `addrAll.txt` file in the current file path. The format is as follows:

```
file_name:/home/hacker/glibc/2.23/arm//lib/libc.so.6
elf_addr:0xfffdc000
main_addr:0xfffdcf20
libc_addr:0xff668000
```

Modify `libc_addr` and `file_name` to correspond, and then enter the command directly in gdb.

### 2. One-click start command

#### 🔺Note:

This startup command needs terminal support, mine is `gnome-terminal` terminal, and the related commands are in the `~/mulArchAll/CMD` directory, as follows

![image-20211125145649527](https://pig-007.oss-cn-beijing.aliyuncs.com/img/20211125145649.png)

If it is another terminal, change the red box to the corresponding terminal, and then call the command behind bash. But after modification, you need to run `updateMulArchAll` to make the command take effect.

#### ①arm architecture

arm adapts to pwndbg and gef

For arm without pie, you can first gdbMulArchNoPie, then add-symbols-file-all, this uses vmmap to get the libc base address and then change addrAll.txt or changeLibc, and then directly gdbMulArchNoPie

arm has pie directly gdbMulArchPie



aarch64 adapts to pwndbg and gef

aarch64 directly without pie gdbMulArchNoPie

aarch64 has pie directly gdbMulArchPie

#### ②mips architecture

mips only adapt to gef

mips can directly gdbMulArchNoPie without pie

mips has pie directly gdbMulArchPie



mips64 only adapts to gef

mips64 can be directly gdbMulArchNoPie without pie

If mips64 has pie, you can also directly gdbMulArchPie

### 3. Combine pwntools to implement gdb.attach function

```python
def mulArchDbgPie():
    global p
    p = process(['gdbMulArchPie',binary,arch,version,localPort,gdbTool])
    pause()
mulArchDbgPie()


def mulArchDbgNoPie():
    global p
    p = process(['gdbMulArchNoPie',binary,arch,version,localPort])
    pause()
mulArchDbgNoPie()
```

The above two functions can achieve similar functions, but they need to be placed at the beginning of the program and will stop at the main function. After startup, you need to run it by yourself. For details, see the file in `~/mulArchAll/example`. It can be used after compiling with the corresponding architecture compiler.

#### 🔺Note:

To turn on pie, you need to add two pause() where you need to stop, so as to prevent the exp.py file from running and exiting directly, making gdb unable to breakpoint.

The breakpoint is to use `ctrl+c` at the place where the exp.py file is running, and send an interrupt command to gdb.

![image-20211125150747510](https://pig-007.oss-cn-beijing.aliyuncs.com/img/20211125153322.png)
