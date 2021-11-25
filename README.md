# mulArchAll

Language: [English](https://github.com/PIG-007/mulArchAll/blob/master/README_en-US.md) | [中文简体](https://github.com/PIG-007/mulArchAll/blob/master/README.md)

建立PWN的异构环境，同时解决异构环境下关于qemu和pie不好调试问题，加载所有符号表，可以使用堆命令，heap,bins等，方便做题。

## 前置安装

需要安装pwndbg和gef。

## 安装

```bash
cd
git clone https://github.com/PIG-007/mulArchAll.git
#git clone https://gitee.com/Piggy007/mulArchAll.git
cd mulArchAll
chmod a+x setup.sh
./setup.sh
```

### 说明

这里需要说一下，由于之后的需要，我直接把gdb启动脚本`.gdbinit`给覆盖了，覆盖文件从`~/mulArchAll/gdbinit/`中获取

#### 插件加载

```bash
source ~/pwndbg/gdbinit.py
#source ~/peda/peda.py
#source ~/gef/gef.py
source ~/Pwngdb/pwngdb.py
source ~/Pwngdb/angelheap/gdbinit.py
```

如果相关的插件位置不一样，请安装之后自行更改。

#### 命令加载

```bash
source ~/mulArchAll/gdbCMD/getAddrAll.py
source ~/mulArchAll/gdbCMD/add-symbol-fill-all.py
```

关于这个启动脚本的命令，是自己写的寻找地址，加载符号的命令，没什么影响，不过相应的python3中也需要安装相对于包才能完成加载，所需包如下，不然无法完成命令加载，会出错，请手动pip给python3安装。

```python
import re
import os
import subprocess
from time import sleep
```

## 使用方法

### 1.gdb添加的命令

`getAllAddr`：

![image-20211124225014181](https://pig-007.oss-cn-beijing.aliyuncs.com/img/20211124225014.png)

即给定四个参数，分别是libc文件路径，elf架构类别，elf中关于`__libc_start_mian_`函数的got表偏移和gdbtool。

gdbtool设置为pwndbg会保留当前gdb命令行，输入gef则会退出。

(这里没有实现自动获取got表的原因是，mips架构的got表使用ELF功能无法查找到对应的got表偏移，不知道怎么解决，所以这里选择手动添加，不过我们做pwn的时候肯定会IDA打开，直接查找给定即可)

类似以下的红色框的got偏移地址，是elf文件，不是so文件的。

![image-20211124225332532](https://pig-007.oss-cn-beijing.aliyuncs.com/img/20211124225332.png)

#### 🔺注：

这个功能是基于pwndbg的vmmap功能，可以获取到对应elf基地址，不然没办法使用，最近的pwndbg的vmmap好像不太好使?

或者知道elf基地址之后，可以直接断点在main函数，之后获取`__libc_start_mian_`函数的got表中该函数的真实地址，将地址写入当前文件路径的`addrAll.txt`，然后如下情况。

`add-symbol-file-all`：

参考以下网址的脚本后自己再更改了一些

[gdb add-symbol-file all sections and load address - Stack Overflow](https://stackoverflow.com/questions/33049201/gdb-add-symbol-file-all-sections-and-load-address)

这个命令本来是需要传入地址的，但是这里修改了一下，从当前文件路径中的`addrAll.txt`文件中获取，格式如下：

```
file_name:/home/hacker/glibc/2.23/arm//lib/libc.so.6
elf_addr:0xfffdc000
main_addr:0xfffdcf20
libc_addr:0xff668000
```

修改`libc_addr`和`file_name`为对应的，然后在gdb中直接输入该命令即可。

### 2.一键启动命令

#### 🔺注：

这个启动命令需要终端支持，我的是`gnome-terminal`终端，相关命令在`~/mulArchAll/CMD`目录下，如下

![image-20211125145649527](https://pig-007.oss-cn-beijing.aliyuncs.com/img/20211125145649.png)

如果是其他终端则将红框改为对应的终端，然后调用bash后面的命令即可。不过修改后需要运行`updateMulArchAll`使得命令生效。

#### ①arm架构

arm适应pwndbg和gef

arm无pie可以先gdbMulArchNoPie，然后add-symbols-file-all，这个使用vmmap获取libc基地址之后改掉addrAll.txt即可或者changeLibc，然后直接gdbMulArchNoPie

arm有pie直接gdbMulArchPie即可



aarch64适应pwndbg和gef

aarch64无pie直接gdbMulArchNoPie

aarch64有pie直接gdbMulArchPie

#### ②mips架构

mips只适应gef

mips无pie直接gdbMulArchNoPie即可

mips有pie直接gdbMulArchPie即可



mips64只适应gef

mips64无pie直接gdbMulArchNoPie即可

mips64有pie也直接gdbMulArchPie即可

### 3.结合pwntools实现gdb.attach功能

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

以上两个函数可以实现类似功能，不过需要放在程序开头，会停在main函数处，启动后需要自己再运行，详情看`~/mulArchAll/example`中的文件。用对应架构编译器编译后使用即可。

#### 🔺注：

开启pie的需要在需要停住的地方加两个pause()才好停下，防止exp.py文件运行直接退出使得gdb无法断点。

断点是需要在运行exp.py文件处使用`ctrl+c`，发送中断指令给gdb才行。

![image-20211125150747510](https://pig-007.oss-cn-beijing.aliyuncs.com/img/20211125150747.png)
