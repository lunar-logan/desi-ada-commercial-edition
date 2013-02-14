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


-- Function Max_Subsequence_Sum is the O(N log N) algorithm in Figure 2.7
-- A short test program is provided
-- Max3 is implemented; it returns the maximum of three integers

with Ada.Text_IO; use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Fig2_7 is

    type Input_Array is array( Integer range <> ) of Integer;

    An_Array : Input_Array( 1..8 ) := ( 4, -3, 5, -2, -1, 2, 6, -2 );


    -- Return the maximum of A, B, and C
    function Max3( A, B, C: Integer ) return Integer is
    begin
        if A > B then
            if A > C then
                return A;
            else
                return C;
            end if;
        else
            if B > C then
                return B;
            else
                return C;
            end if;
        end if;
    end Max3;

    function Max_Subsequence_Sum( A: Input_Array ) return Integer is
        Max_Left_Sum, Max_Left_Border_Sum : Integer := 0;
        Max_Right_Sum, Max_Right_Border_Sum : Integer := 0;
        Left_Border_Sum, Right_Border_Sum : Integer := 0;
        Center 			  : Integer := ( A'First + A'Last ) / 2;
    begin
        if A'Length = 1 then  -- Base case 
            if A( A'First ) > 0 then
                return A( A'First );
            else
                return 0;
            end if;
        end if;

        -- Compute the maximum for each of the two halves recursively
        Max_Left_Sum  := Max_Subsequence_Sum( A( A'First..Center ) );
        Max_Right_Sum := Max_Subsequence_Sum( A( Center+1..A'Last ) );

        -- Compute the maximum sum of the sequence that includes
        -- the last element in the first half
        for I in reverse A'First..Center loop
            Left_Border_Sum := Left_Border_Sum + A( I );
            if Left_Border_Sum > Max_Left_Border_Sum then
                Max_Left_Border_Sum := Left_Border_Sum;
            end if;
        end loop;

        -- Compute the maximum sum of the sequence that includes
        -- the first element in the second half
        for I in Center+1..A'Last loop
            Right_Border_Sum := Right_Border_Sum + A( I );
            if Right_Border_Sum > Max_Right_Border_Sum then
                Max_Right_Border_Sum := Right_Border_Sum;
            end if;
        end loop;

        -- Return the maximum of the three possibilities
        return Max3( Max_Left_Sum, Max_Right_Sum,
                Max_Left_Border_Sum + Max_Right_Border_Sum );

    end Max_Subsequence_Sum;

begin
    Put( Max_Subsequence_Sum( An_Array ) ); New_Line;
end Fig2_7;
----------------------------------

procedure Subt is
      subtype Day is Integer range 1 .. 7;
      Q : Day;
   
      M : Natural;  -- built in subtype: Integer range 0 .. max integer
      N : Positive; -- built in subtype: Integer range 1 .. max integer
   
   begin
      Q := 8;  -- raises runtime exception (error)
      M := -1;  -- so does this
   end;
-------------------------------------------

----------------------------------------------------
with Ada.Text_IO; use Ada.Text_IO;

procedure Hello is
type Day_type   is range    1 ..   31;
type Month_type is range    1 ..   12;
type Year_type  is range 1800 .. 2100;
type Hours is mod 24;
type Weekday is (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday); 
 
type Date is
   record
     Day   : Day_type;
     Month : Month_type;
     Year  : Year_type;
   end record;
begin
  Put_Line ("Hello, world!");
end Hello;
----------------------------------------------------
