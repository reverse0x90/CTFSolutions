"""
ISITDTU CTF 2018 
Cool reverse challenge solution
"""
# Imports
import re, sys, time, string
from pwn import *

# Set pwntools context and log level
context(arch="amd64")
context.log_level = 'error'


def find_solution():
  """
  Finds the solution string to pass to the challenge binary.
  """
  # Running xor byte used to check solution
  xor_byte = 0

  # Solution byte array pulled from address 0x6020A8 in the binary
  solution_check_bytes = "7D4D2344360276036F5B2F46761839".decode("hex")

  # Construct the first 13 chars of the solution to pass the first checks in binary
  #ecfd4245812b86ab2a878ca8cb1200f9 = "fl4g"  (0x400DDD)
  #88e3e2edb64d39698a2cc0a08588b5fd = "_i5_"  (0x400E1B)
  #bbc86f9d0b90b9b08d1256b4ef76354b = "h3r3"  (0x400E59)
  solution = "fl4g_i5_h3r3!"

  # Calculate the running xor byte for the first part of the solution
  for i in range(len(solution)):
    xor_byte ^= ord(solution[i])
    
  # Brute force the second part of the solution by using the solution byte array
  # to check the running xor byte against
  for solution_check_byte in solution_check_bytes:
    for char in string.printable:
      if chr(xor_byte ^ ord(char)) == solution_check_byte:
        solution += char
        xor_byte ^= ord(char)

  # Return the solution string
  return solution


def main():
  """
  Runs on program execution.
  """
  # Find the solution string
  solution = find_solution()

  # Open the binary with pwntools
  cool = process('cool')

  # Read "Give me your key:" from the binary 
  print cool.recvuntil('Give me your key:')

  # Send the solution
  cool.sendline(solution)

  # Read the response
  print cool.recvline() # Congratulation~~~
  print cool.recvline() # Your flag: ISITDTU{fl4g_i5_h3r3!C0ngr4tul4ti0n!}


# Hook
if __name__ == '__main__':
  main()