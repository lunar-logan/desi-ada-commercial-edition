-- Expressions
procedure test1 is
      Ace,Patt,Cat,Bag : Integer;  -- same as 3 separate declarations
      Dog : Character;
   begin
      Ace := 5;
      Put(Ace);
      Put(newline);
--       Dog := 'd';  --to handle

      Patt := Ace * 3 + 4;
      Put(Patt);
      Put(newline);

      Bag := Ace * (3 + 4); -- using parens to override the order
      Put(Bag);
      Put(newline);

      Cat := Ace / 3;       -- result is 1  (division truncates)
      Put(Cat);
      Put(newline);

--      Dog := Ace + Bag;      --Error
--      Cat := Dog ** 2;      -- Error
   end;
