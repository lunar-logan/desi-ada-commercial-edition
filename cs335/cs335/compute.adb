function Square(Pandey:Integer) return Integer is
   begin
   Pandey := Pandey*Pandey;
   return Pandey;
   end;

procedure Compute is
      A : Integer := 3;    -- initializing a variable
      C : float := 3.5;
      Anurag : Integer ;
   begin
 --     B := Square (C );
      A := 4;
      Anurag := Square(A);
   end Compute;

