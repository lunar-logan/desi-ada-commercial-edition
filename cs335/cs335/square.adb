-- Change return type. Provides return type error
function Square (Arg: Integer) return Integer is
--   B : float;
   begin
        Arg := 3;
--      B := 4.5;
--      return B;
      return Arg * Arg;
   end Square;
