add $s0, $0, $0
add $s1, $0, $0
addi $t0, $0, 0
addi $s7, $0, 10

loop: lw $s2, 0($t0)
addi $t0, $t0, 4
add $s1, $s1, $s2
addi $s0, $s0, 1
beq $s0, $s7, next
j loop
next: print $s1
exit