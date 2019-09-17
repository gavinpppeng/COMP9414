% Name: Wenxun Peng
% Student ID: z5195349
% Assignment 1 - Prolog Programming
% Date: 15/3/2019

% Q1 sums the squares of only the even numbers in a list of integers.
% list is empty, return 0
sumsq_even([],0).

% The number is even, then calculate the squares and add it to the sum.
sumsq_even([Head|Tail], Sum) :-
		0 is Head mod 2,
		sumsq_even(Tail, Result),
		Sum is Head * Head + Result.	

% The number is odd, then just skip it.
sumsq_even([Head|Tail], Sum) :-
		1 is Head mod 2,
		sumsq_even(Tail, Sum).


% Q2 Write a predicate same_name(Person1,Person2) that succeeds if it can be deduced from the facts in the database that Person1 and Person2 will have the same family name. 
% if the two people have the same family name
% find all the ancestor of the child

% step 1 : their parents(father) are same.
ancestor(Person, Father) :-
		parent(Father, Person),
		male(Father).
		
% step 2 : if their male's ancestors are same or find their ancestor when matching step 3 and step 4.
ancestor(Person, Ancestor) :-
		parent(Parent, Person),
		male(Parent),
		ancestor(Parent, Ancestor).
		
% step 3 : Person1 is Person2's Ancestor
same_name(Person1,Person2) :-
		ancestor(Person2, Person1).
		
% step 4: Person2 is Person1's Ancestor
same_name(Person1, Person2) :-
		ancestor(Person1, Person2).

% Person1 and Person2 have the same Ancestor and maybe they are the same people
same_name(Person1, Person2) :-
		ancestor(Person1, Ancestor),
		ancestor(Person2, Ancestor).
		
		
% Q3 list of pairs consisting of a number and its square root.
build_list(Num, ResultList) :-
		Result is sqrt(Num),
		ResultList = [Num, Result].
		
sqrt_list([], []).

sqrt_list([Head|Tail], [List|ResultList]) :-
		build_list(Head, List),
		sqrt_list(Tail, ResultList).
		
		
% Q4 Any list of integers can (uniquely) be broken into "sign runs" where each run is a (maximal) sequence of consecutive negative or non-negative numbers within the original list. 
% Write a predicate sign_runs(List, RunList) that converts a list of numbers into the corresponding list of sign runs. Like input: sign_runs([8,-1,-3,0,2,0,-4], RunList).
% RunList = [[8], [-1, -3], [0, 2, 0], [-4]]
% judging the number is a negative or non-negative number
negative(Num) :-
	integer(Num),
	Num < 0.

non_negative(Num) :-
	integer(Num),
	Num >= 0.

% There are two situations in finding the negative:
% 1. L2 is empty which means that there are not negative number before the non-negative appears.
% 2. L2 is not empty which means that there are some negative numbers before the non-negative appears.
classify_sign([Head|Tail], ResultList, L1, L2) :-
		non_negative(Head),
		L2 == [],
		classify_sign(Tail, ResultList, [Head|L1], []).

classify_sign([Head|Tail], [L2|ResultList], L1, L2) :-
		non_negative(Head),
		L2 \= [],
		classify_sign(Tail, ResultList, [Head|L1], []).

% There are two situations in finding the non-negative:
% 1. L1 is empty which means that there are not non-negative number before the negative appears. 
% 2. L1 is not empty which means that there are some non-negative numbers before the negative appears.
classify_sign([Head|Tail], ResultList, L1, L2) :-
		negative(Head),
		L1 == [],
		classify_sign(Tail, ResultList, [], [Head|L2]).

classify_sign([Head|Tail], [L1|ResultList], L1, L2) :-
		negative(Head),
		L1 \= [],
		classify_sign(Tail, ResultList, [], [Head|L2]).

% The last step
classify_sign([], [L1], L1, _) :-
		L1 \= [].

classify_sign([], [L2], _, L2) :-
		L2 \= [].

% Since the list is reverse, we should change the order. E.g [-1, -3] will become [-3, -1], so we should reverse it.
% reverse the list as mentioned.
reverse_element([], Result, Result).
reverse_element([Head|Tail], Result, TepList) :-
		reverse_element(Tail, Result, [Head|TepList]).

% get the list separately.
reverse_list([], []).

reverse_list([Head|Tail], [RevResult|Result]) :-
		reverse_element(Head, RevResult, []),
		reverse_list(Tail, Result).

sign_runs([],[]).

sign_runs(List, RunList) :-
		classify_sign(List, ReList, [], []),
		reverse_list(ReList, RunList).


% Q5 A binary tree of numbers is called a heap, if, for every non-leaf node in the tree, the number stored at that node is less than 
% or equal to the number stored at each of its children. For example, the following tree satisfies the heap property (3<=5,5<=8, and 5<=7).
% tree(empty,3,tree(tree(empty,8,empty),5,tree(empty,7,empty)))
% On the other hand, the following tree does not satisfy the heap property, because 6 is not less than or equal to 5.
% tree(tree(tree(empty,4,empty),3,tree(empty,5,empty)),6,tree(tree(empty,9,empty),7,empty)).

% tree is empty or the the children are empty
is_heap(empty).
is_heap(tree(empty, _,empty)).

% left child is empty
is_heap(tree(empty, Num, tree(LC, RightNum, RC))) :-
		RightNum >= Num,
		is_heap(tree(LC, RightNum, RC)).

% right child is empty
is_heap(tree(tree(LC, LeftNum, RC), Num, empty)) :-
		LeftNum >= Num,
		is_heap(tree(LC, LeftNum, RC)).

% left and right child are not empty
is_heap(tree(tree(LC, LeftNum, RC), Num, tree(LRC, RightNum, RRC))) :-
		LeftNum >= Num,
		RightNum >= Num,
		is_heap(tree(LC, LeftNum, RC)),
		is_heap(tree(LRC, RightNum, RRC)).

		