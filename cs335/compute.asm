.text
square:
move $fp $sp
sw $ra 0($sp)
addiu $sp $sp -4
lw $a0 4($fp)
sw $a0 0($sp)
addiu $sp $sp -4
lw $a0 4($fp)
lw $t1 4($sp)
mul $a0 $t1 $a0
addiu $sp $sp 4
sw $a0 4($fp)
lw $a0 4($fp)
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
.text
.globl main
main:
compute:
addiu $sp $sp -4
addiu $sp $sp -4
addiu $sp $sp -4
move $fp $sp
sw $ra 0($sp)
addiu $sp $sp -4
li $a0 4
sw $a0 12($fp)
sw $fp 0($sp)
addiu $sp $sp -4
lw $a0 12($fp)
sw $a0 0($sp)
addiu $sp $sp -4
li $v0 1
syscall
jal square
sw $a0 4($fp)
li $v0 1
syscall
lw $ra 4($sp)
addiu $sp $sp 20
lw $fp 0($sp)
jr $ra
li $v0 1
syscall
li $v0 10
syscall

