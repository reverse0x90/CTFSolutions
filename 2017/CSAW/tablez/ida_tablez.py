"""
CSAW 2017 tablez reverse engineering challenge solution

This is idapython solution script and can be executed in the IDA GUI as follows:
  1. File -> Script file...
  2. Alt + F7
"""

# Imports
import idaapi
import idc

def main():
    # Local variables
    plaintext_table_bytes = []
    obfuscated_table_bytes = []
    obfuscated_flag_bytes = None

    # Set the debugger to linux
    idc.LoadDebugger(dbgname="linux", use_remote=1)

    # Set a breakpoint at the start of the executable and start the debugger
    idc.AddBpt(idc.BeginEA())
    idc.RunTo(idc.BeginEA())
    idc.GetDebuggerEvent(WFNE_SUSP,-1)

    # Get the rebased entry of the executable (binary is a .so and will be rebased on load by the linker)
    entry_point = idc.GetRegValue("RIP")

    # Calculate rebased breakpoint addresses
    fgets_bp = entry_point + 0x1f3
    get_tbl_entry_bp = entry_point + 0x24F
    get_tbl_entry_ret_bp = entry_point + 0x254

    # Set the breakpoints in ida
    idc.AddBpt(fgets_bp)
    idc.AddBpt(get_tbl_entry_bp)
    idc.AddBpt(get_tbl_entry_ret_bp)

    # Run debugger to fgets call breakpoint 
    idc.RunTo(fgets_bp)
    idc.GetDebuggerEvent(WFNE_SUSP,-1)
    stack_addr = idc.GetRegValue("RDI")

    # Simulate fgets user input by patching the fgets buffer with 0x41 bytes
    ea = stack_addr
    while ea <= stack_addr + 0x25:
        idc.PatchByte(ea, 0x41)
        ea += 1

    # Extract the obfuscated flag bytes from memory
    obfuscated_flag_bytes = idc.GetManyBytes(idc.GetRegValue("RBP") - 0xC0, 0x25)

    # Jump over fgets call
    idc.SetRegValue(fgets_bp+0x05, "RIP")

    # Enumerate get_tbl_entry output for the printable values in the ascii table
    for byte in range(0x20, 0x7f):
        # Break at get_tbl_entry function call and change input value
        idc.RunTo(get_tbl_entry_bp)
        idc.GetDebuggerEvent(WFNE_SUSP,-1)
        idc.SetRegValue(byte, "RDI")

        # Break at get_tbl_entry return and save output value
        idc.RunTo(get_tbl_entry_ret_bp)
        idc.GetDebuggerEvent(WFNE_SUSP,-1)
        idc.SetRegValue(get_tbl_entry_bp-0x02, "RIP")
        plaintext_table_bytes.append(byte)
        obfuscated_table_bytes.append(GetRegValue("RAX"))

    # Stop the debugger
    idc.StopDebugger()

    # Deobfuscate the flag string
    flag_str = ""
    for byte in obfuscated_flag_bytes:
        flag_str += chr(plaintext_table_bytes[obfuscated_table_bytes.index(ord(byte))])
    
    # Display the flag
    Message("[+] Deobfuscated flag: %s\n" % (flag_str))


if __name__ == '__main__':
    main()
