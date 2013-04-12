.data
choice:  .byte 1
a:  .word 1
.text
.globl main
main:
li $a0 4
sw $a0 a
lw $a0 a
sw $a0 0($sp)
addiu $sp $sp -4
el0:
li $a0 1
lw $t1 4($sp)
beq $a0 $t1 l2
j el1
l2:
lw $a0 a
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 1
lw $t1 4($sp)
add $a0 $t1 $a0
addiu $sp $sp 4
sw $a0 a
j l1
el1:
li $a0 2
lw $t1 4($sp)
beq $a0 $t1 l3
j el2
l3:
lw $a0 a
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 2
lw $t1 4($sp)
add $a0 $t1 $a0
addiu $sp $sp 4
sw $a0 a
j l1
el2:
li $a0 4
lw $t1 4($sp)
beq $a0 $t1 l4
j el3
l4:
lw $a0 a
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 3
lw $t1 4($sp)
add $a0 $t1 $a0
addiu $sp $sp 4
sw $a0 a
j l1
el3:
j l5
j el4
l5:
lw $a0 a
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 4
lw $t1 4($sp)
add $a0 $t1 $a0
addiu $sp $sp 4
sw $a0 a
j l1
el4:
l1:
addiu $sp $sp 4
li $v0 1
syscall
li $v0 10
syscall

