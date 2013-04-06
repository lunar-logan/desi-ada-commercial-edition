/* Compute fibonacci numbers */

var a int = 1;
var c float = 3.0;
var b int = 1;
var d int = b + c;
var t int;
var n int = 0;
const LAST = 20;

while n < LAST {
    print a;
    t = a + b;
    a = b;
    b = t;
    n = n + 1;
}
