.data
a:  .word 1
b:  .word 1
c:  .float 0.0
.text
compute:
move $fp $sp
sw $ra 0($sp)
addiu $sp $sp -4
li $a0 4
sw $a0 a
lw $ra 4($sp)
addiu $sp $sp 8
lw $fp 0($sp)
jr $ra
li $v0 1
syscall
li $v0 10
syscall

