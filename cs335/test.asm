ExprType(integer)
ExprType(integer)
.data
arg:  .word 1
.text
li $a0 3
sw $a0 arg
lw $a0 arg
sw $a0 0($sp)
addiu $sp $sp -4
lw $a0 arg
lw $t1 4($sp)
mul $a0 $t1 $a0
addiu $sp $sp 4
lw $ra 4($sp)
addiu $sp $sp 4
lw $fp 0($sp)
jr $ra
li $v0 10
syscall

