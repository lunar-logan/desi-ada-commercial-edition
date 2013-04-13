-- Case Statement
procedure Exercise is
   Choice : Character;
   A : Integer;
begin
   A := 4;
   case A is
      when 1 =>
         A := A+1;
      when 2 =>
         A := A+2;
      when 4 =>
         A := A+3; 
      when others =>
         A := A+4;     
   end case;
end Exercise;
