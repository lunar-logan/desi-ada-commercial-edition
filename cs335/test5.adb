-- Loops + Exit Statements
procedure Loops is
      Q : Integer;

   begin
      Q := 1;
      while Q <= 5 loop
         Q := Q + 1;
      end loop;

      for J in 1 .. 5 loop
         Q := Q + 4;
      end loop;

      Q := 1;
      loop
         exit when Q;
         Q := Q + 1;
      end loop;
   end Loops;
