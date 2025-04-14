#!pip install nltk
#import nltk
#nltk.download('stopwords')
# !pip install pylcs
# try:
#     import pyswip
# except ImportError:
#     !pip install pyswip
#     import pyswip

KB = """
%  Tell prolog that known/3 and multivalued/1 will be added later
:- dynamic known/3, multivalued/1.

%/ answers for shoppings
place(yongkang_street):- location(taipei), intention(shopping), buy(souvenirs), price(high).

place(taipei101) :-  location(taipei), intention(shopping), (buy(food); buy(clothes)), price(high).

place(gongguan_market) :-  location(taipei), intention(shopping), (buy(souvenirs); buy(clothes)),price(low).

place(raohe_market) :- location(taipei), intention(shopping), buy(food), price(low).

place(zhongshan_street) :- location(taipei), intention(shopping), buy(clothes), price(medium).

place(dihua_street) :- location(taipei), intention(shopping), (buy(souvenirs); buy(food)), price(medium).



%answers for learning
place(taipei_fine_art_museum) :- location(taipei), intention(learning), entrance_fee(yes), (about(culture); about(history)).

place(national_palace_museum) :- location(taipei), intention(learning),  entrance_fee(yes), (about(culture); about(history)).

place(chiang_shek_memorial_hall) :- location(taipei), intention(learning), entrance_fee(no), (about(culture); about(history)).

place(huashan_creative_park) :- location(taipei), intention(learning),  entrance_fee(no), (about(art); about(history)).



%answers for relaxing and destress
place(eslite_bookstore_taipei101) :- location(taipei), intention(relaxing),  crowded(yes),setting(indoor), (ambience(cozy); ambience(tranquil)).

place(elephant_mountain) :- location(taipei), intention(relaxing), crowded(no), setting(outdoor), ambience(tranquil).

place(tam_sui_river) :- location(taipei), intention(relaxing), crowded(yes), setting(outdoor), ambience(tranquil).

place(daan_park) :- location(taipei), intention(relaxing), crowded(no), setting(outdoor), ambience(cozy).

place(songshan_creative_park) :- location(taipei), intention(relaxing), crowded(no), (setting(indoor); setting(outdoor)), ambience(lively).

place(jiufen) :- location(taipei), intention(relaxing), crowded(yes), (setting(indoor); setting(outdoor)), ambience(lively).




%This checks if the user is not in taipei
place(ask_others) :- \+location(taipei).




% The code below implements the prompting to ask the user:

% Define the buy rule
buy(X) :- menuask('What would you like to buy?', X, [souvenirs, clothes, food]).

% Define the intention rule
intention(X) :- menuask('What is your intention of going to a tourist place?', X, [relaxing, learning, shopping]).

% Define the price rule
price(X) :- menuask('What is your preferred price range?', X, [low, medium, high]).

% Define the location rule
location(X) :- ask(location, X).

% Define the entrance_fee rule
entrance_fee(X) :- menuask('Do you mind paying an entrance fee?', X, [yes, no]).

% Define the about rule
about(X) :- menuask('what do you wanna learn about?', X, [art, history, culture]).

% Define the crowded rule
crowded(X) :- menuask('Do you prefer a crowded setting?', X, [yes, no]).

% Define the setting rule
setting(X) :- menuask('What type of settings do you want?', X, [indoor, outdoor]).

% Define the ambience rule
ambience(X) :- menuask('What type of ambience do you want?', X, [lively, cozy, tranquil]).


% Asking clauses
ask(A, V):-
known(yes, A, V), % succeed if true
!.	% stop looking

ask(A, V):-
known(_, A, V), % fail if false
!, fail.


% If not multivalued, and already known, don't ask again for a different value.
ask(A, V):-
\+multivalued(A),
known(yes, A, V2),
V \== V2,
!.


ask(A, V):-
read_py(A,V,Y), % get the answer
assertz(known(Y, A, V)), % remember it
Y == yes.	% succeed or fail

%Reference: http://www.amzi.com/ExpertSystemsInProlog/02usingprolog.php

menuask(A, V, _):-
known(yes, A, V), % succeed if true
!.	% stop looking

menuask(A, V, _):-
known(yes, A, V2), % If already known, don't ask again for a different value
V \== V2,
!, fail.

menuask(A, V, Menu):-
  read_menu_py(A,X,Menu),
  confirm_answer(X,A,V,Menu),
  asserta(known(yes,A,X)),
  X == V.


confirm_answer(X,_,_,Menu):-
  member(X,Menu),
  !.

confirm_answer(X,A,V,Menu):-
 dialog_response(X), dialog_response(' Please, change your input.\n'),
 menuask(A, V, Menu). 

"""