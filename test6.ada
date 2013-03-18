-- Case Statement
procedure Exercise is
   Choice : Character;
   A : Integer;
begin
   A := 4;
   case Choice is
      when 'a' =>
         A := A+1;
      when 'b' =>
         A := A+2;
      when 'c' =>
         A := A+3; 
      when 4 =>
         A := A+3;     
   end case;
end Exercise;
