-- If_Else Statement
procedure test2 is
      Ace,Patt,Cat,Bag : Integer;  -- same as 3 separate declarations
      Dog : Character;
   begin
      Ace := 5;
      Bag := 4;

      if (Bag=Ace) then Bag:=4;
      elsif (Bag>3) then Bag:=7;
      end if;
      
      Put(Bag);
      Put(newline);
   end;
