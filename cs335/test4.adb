-- Logical and Relational Operators
procedure Bool is
      X,Y : Boolean;
      A : constant Integer := 3;
      B : constant Integer := 4;
   
   begin
      X := A =  3;  -- result is True
      Y := A >  3;  -- result is False
      Y := A >= 3;  -- result is True
      Y := A <  3;  -- Result is False
      Y := A <= 3;  -- Result is True
      Y := A /= 3;  -- Result is False
   
      Y := A = 3 and then B = 4; -- Result is True
      Y := A = 3 or else  B = 3; -- Result is False
   
      Y := A = 2 and then B = (1 / 0); -- False, 1/0 not executed
      Y := A = 2 and      B = (1 / 0); -- Bomb,  1/0 computed
      Y := A = 3 or else  B = (1 / 0); -- True,  1/0 not executed
      Y := A = 3 or       B = (1 / 0); -- Bomb,  1/0 computed
   end Bool;
