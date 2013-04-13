.data
a:  .word 1
pandey:  .word 1
c:  .word 1
d:  .byte 1
.text
.globl main
main:
li $a0 5
sw $a0 a
lw $a0 a
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 3
lw $t1 4($sp)
mul $a0 $t1 $a0
addiu $sp $sp 4
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 4
lw $t1 4($sp)
add $a0 $t1 $a0
addiu $sp $sp 4
sw $a0 pandey
lw $a0 pandey
sw $a0 0($sp)
addiu $sp $sp -4
lw $a0 a
lw $t1 4($sp)
seq $a0 $t1 $a0
addiu $sp $sp 4
beq $a0 0 l1
li $a0 4
sw $a0 pandey
j l2
l1:
lw $a0 pandey
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 19
lw $t1 4($sp)
seq $a0 $t1 $a0
addiu $sp $sp 4
beq $a0 0 l3
li $a0 7
sw $a0 c
j l4
l3:
l4:
l2:
li $v0 10
syscall

