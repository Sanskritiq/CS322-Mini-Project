0		add	$s0	$0	$0
1		add	$s1	$0	$0
2		addi	$t0	$0	0
3		addi	$s7	$0	10
4	loop	lw	$s2	0($t0)	
5		addi	$t0	$t0	4
6		add	$s1	$s1	$s2
7		addi	$s0	$s0	1
8		beq	$s0	$s7	next
9		j	loop		
10	next	print	$s1		
12		exit			
