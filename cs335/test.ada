procedure Ops is
      A,B,C : Integer;  -- same as 3 separate declarations
      D : Character;
   begin
      A := 5;
      D := 'b';
      B := A * 3 + 4;   -- result is 19 (multiplication done first)
      B := A * (3 + 4); -- using parens to override the order
      C := A / 3;       -- result is 1  (division truncates)
      C := A rem 3;     -- result is 2
      C := A - 1;
      D := A + B;       -- assign type error
      A := A + D;       -- binaryop type error
      C := A ** 2;      -- exponentiation
   end;
