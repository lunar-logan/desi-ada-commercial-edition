-- Function calling
function Square (Arg : Integer) return Integer is
--   B : float;
   begin
--      B := 4.5;
--      return B;
      return Arg * Arg;
   end Square;

procedure Compute is
      A : Integer := 3;    -- initializing a variable
      B : Integer;
      C : float := 3.5;
   begin
      B := Square (A + 1); -- result is 16
--      B := Square (C + 1);
   end Compute;
