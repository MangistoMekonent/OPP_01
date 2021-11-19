# Elevator routing system
*OOP 2021 course assignment 1

The goal of this assignment is to create an offline algorithm
assigning smart elevators to calls.

We have consulted the following sources for reference and inspiration
when designing the algorithm and understanding the issue it solves:

https://thesai.org/Downloads/Volume10No2/Paper_3-Smart_Buildings_Elevator_with_Intelligent_Control.pdf
https://dergipark.org.tr/tr/download/article-file/539296
https://gist.github.com/benbuckman/3150822

## Algorithm description

While there are calls left (in the input):
1. Choose the next (or first) elevator.
2. Assign the current floor and finish time to 0.
3. Iterate over the calls until a call which occurs before the last
   finish time is found, and assign it the current elevator (removing
   it from the input list).
   Calculate the finish time according to this call (this will be the
   last call in the current path), assign the floor to the destination
   floor of this call and the direction to the direction of the call.
4. Iterate over the rest of the calls.
   If a call is in the same direction of the call and its source and
   destination are within the bounds of the first call, assign the
   elevator and record the floor as with the first call.
   If a call occurs after the finish time of the first call, stop
   iteration (to prevent needlessly iterating over all of the calls).
5. If there are elevators left, go back to step 1.
