.data
prabhat: .word 1
fl: .asciiz ""
temp: .asciiz "hi"
.text
.globl main
main:
la $t3 fl
la $t2 temp
sw $t2 0($t3) 
la $a0 fl
li $v0 4
syscall
li $t1 123
sw $t1 prabhat
lw $a0 prabhat
li $v0 1
syscall
.data
manav: .word 1
.text
li $t1 456
sw $t1 prabhat
lw $a0 prabhat
li $v0 1
syscall
li $v0 10
syscall
