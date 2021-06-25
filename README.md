# Melody

A new, softer programming language. Code is by default squishy and is held in place by clarifying unit tests.

This mirrors how humans choose to describe complex systems. 
Boardgame rulebooks almost always have ambigious definitions followed by clarifying examples. 
Our legal system has laws that are open to interpretation punctuated by the precendents of court cases. 

Here's an example for Project Euler's Question 1. It asks

> If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
> Find the sum of all the multiples of 3 or 5 below 1000.

```
fn (int "multiple" of:int) -> bool
   mod equals 0
eg. 9 multiple 3 -> True

sum 1..999 where (multiple of 3) or (multiple of 5)
```

And here's an example for Advent of Code's [Report Repair](https://adventofcode.com/2020/day/1) problem.
> Given a file with one number per line, find the two entries that sum to 2020 and then multiply those two numbers together.
> For example, suppose your expense report contained the following:
> 
> 1721, 979, 366, 299, 675, 1456
>
> In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

```
fn ("solve" list.int) -> int
   first combination of 2 where sum == 2020
   product
eg. solve [1721, 979, 366, 299, 675, 1456] -> 514579

read file "day1.txt" as list.int
solve
```
