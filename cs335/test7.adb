--with Ada.Text_IO;   
function Levenshtein(prabhat,pandey : Integer) return Integer is
manav : Integer;
type day is (Mon,Tue,Wed);
type Car is record
     Identity       : Integer;
     Number_Wheels  : Integer range 1 .. 10;
     Horse_Power_kW : Float range 0.0 .. 2_000.0;
     Consumption    : Float range 0.0 .. 100.0;
  end record;
    type Car_p is access Car;
    type S is array(1..prabhat'Last,1..10) of integer;
      subtype U is S range 5..6;
      B: S;
      Q : Integer;
      A : array(1..5) of integer;
   BMW : Car ;
   E : day;
   begin
--     E := Thu; 
--     BMW := (434, 5.2,  190.0, 10.1);
      Q := 1;
      A(1) := Q*9;
      for I in Integer RANGE 1 .. 10 loop
         Q := Q + 1;
      end loop For_Loop;
      while Q <= 5 loop
         Q := Q + 1;
      end loop;
      declare 
         Q : Float;
      begin
         Q := 3;
      end;
      return Q;
   end Levenshtein;
