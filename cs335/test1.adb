procedure Ops is
      A,Pandey,C : Integer;  -- same as 3 separate declarations
      D : Character;
   begin
      A := 5;
--      D := 'b';
      Pandey := A * 3 + 4;   -- result is 19 (multiplication done first)
      if (Pandey=A) then Pandey:=4;
      elsif (Pandey=19) then C:=7;
      end if;
--      B := A * (3 + 4); -- using parens to override the order
--      C := A / 3;       -- result is 1  (division truncates)
--      C := A rem 3;     -- result is 2
--      C := A - 1;
--      D := A + B;      --Error
--      C := D ** 2;      -- Error
   end;
