a:=9.84E1;
b:=98.4e0;
c:=984.0e-1;
e:=984e-1;
f:=2#101#;
g:=16#B#E2;
h:=1900;
i:=19E2;
j:=19_0_1e+1;
A:="He\"\"llo Duniya Walon";
with Ada.Text_IO;  use Ada.Text_IO;
 
procedure Test_Recursive_Binary_Search is
   Not_Found : exception;
 
   generic
      type Index is range <>;
      type Element is private;
      type Array_Of_Elements is array (Index range <>) of Element;
      with function "<" (L, R : Element) return Boolean is <>;
   function Search (Container : Array_Of_Elements; Value : Element) return Index;
 
   function Search (Container : Array_Of_Elements; Value : Element) return Index is
      Mid : Index;
   begin
      if Container'Length > 0 then
         Mid := (Container'First + Container'Last) / 2;
         if Value < Container (Mid) then
            if Container'First /= Mid then
               return Search (Container (Container'First..Mid - 1), Value);
            end if;
         elsif Container (Mid) < Value then
            if Container'Last /= Mid then
               return Search (Container (Mid + 1..Container'Last), Value);
            end if;
         else
            return Mid;
         end if;
      end if;
      raise Not_Found;
   end Search;
 
   type Integer_Array is array (Positive range <>) of Integer;
   function Find is new Search (Positive, Integer, Integer_Array);
 
   procedure Test (X : Integer_Array; E : Integer) is
   begin
      New_Line;
      for I in X'Range loop
         Put (Integer'Image (X (I)));
      end loop;
      Put (" contains" & Integer'Image (E) & " at" & Integer'Image (Find (X, E)));
   exception
      when Not_Found =>
         Put (" does not contain" & Integer'Image (E));
   end Test;
begin
   Test ((2, 4, 6, 8, 9), 2);
   Test ((2, 4, 6, 8, 9), 1);
   Test ((2, 4, 6, 8, 9), 8);
   Test ((2, 4, 6, 8, 9), 10);
   Test ((2, 4, 6, 8, 9), 9);
   Test ((2, 4, 6, 8, 9), 5);
end Test_Recursive_Binary_Search;
----------Edit Distance------
function Levenshtein(Left, Right : String) return Natural is
    D : array(0 .. Left'Last, 0 .. Right'Last) of Natural;
  begin
    for I in D'range(1) loop D(I, 0) := I;end loop;
 
    for J in D'range(2) loop D(0, J) := J;end loop;
 
    for I in Left'range loop
      for J in Right'range loop
        D(I, J) := Natural'Min(D(I - 1, J), D(I, J - 1)) + 1;
        D(I, J) := Natural'Min(D(I, J), D(I - 1, J - 1) + Boolean'Pos(Left(I) /= Right(J)));
      end loop;
    end loop;
 
    return D(D'Last(1), D'Last(2));
  end Levenshtein;
 -----Edit distance ends Here
