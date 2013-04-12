.data
pandey:  .word 1
.text
square:
move $fp $sp
sw $ra 0($sp)
addiu $sp $sp -4
lw $a0 pandey
sw $a0 0($sp)
addiu $sp $sp -4
lw $a0 pandey
lw $t1 4($sp)
mul $a0 $t1 $a0
addiu $sp $sp 4
sw $a0 pandey
lw $a0 pandey
lw $ra 4($sp)
addiu $sp $sp 12
lw $fp 0($sp)
li $v0 1
syscall
jr $ra
li $v0 1
syscall
lw $ra 4($sp)
addiu $sp $sp 12
lw $fp 0($sp)
jr $ra
.data
a:  .word 1
c:  .float 0.0
anurag:  .word 1
.text
.globl main
main:
compute:
move $fp $sp
sw $ra 0($sp)
addiu $sp $sp -4
li $a0 4
sw $a0 a
sw $fp 0($sp)
addiu $sp $sp -4
lw $a0 a
sw $a0 0($sp)
addiu $sp $sp -4
li $v0 1
syscall
jal square
sw $a0 anurag
li $v0 1
syscall
lw $ra 4($sp)
addiu $sp $sp 8
lw $fp 0($sp)
jr $ra
li $v0 1
syscall
li $v0 10
syscall

