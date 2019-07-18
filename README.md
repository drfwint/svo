
# A flexible z-Tree and oTree implementation of the Social Value Orientation Slider Measure

### Authors
**Paolo Crosetto**,
INRA-GAEL, Institut National pour la Recherche Agronomique, Grenoble
Applied Economics Laboratory, 1241 Rue des Résidences -- Domaine
Universitaire, 38400 Saint Martin d'Hères, France

**Ori Weisel**, Coller School of Management, Organizational Behavior Department, Tel
Aviv Universityv Tel Aviv, 6997801, Israel

**Fabian Winter**, Max Planck Institute for Research on Collective Goods, MPRG "Mechanisms
of Normative Change". Kurt Schumacher Strasse 10, 53113 Bonn, Germany



### Keywords
 z-Tree, oTree, experimental software, Social Value Orientation, Slider
Measure

**JEL-Classification:** C91, D03, D64

## Abstract

This manual describes implementations of the SVO Slider Measure
[@murphy2011measuring SVOSM hereafter] in z-Tree [@fischbacher2007z] and
oTree [@chen2016otree], two of the most commonly used software packages
for computerized experiments in the social sciences. The SVOSM is
designed to measure social preferences on a continuous scale, and is
frequently used throughout the literature. Please refer to
@murphy2011measuring for further details. Both implementations can be
accessed via our github repository at <https://github.com/drfwint/svo>.

### Citation

```
Paolo Crosetto, Ori Weisel, Fabian Winter (2019) A flexible z-Tree and oTree Implementation of the Social Value Orientation Slider Measure, Journal of Behavioral and Experimental Finance, Volume 23, Pages 46-53,

```

General remarks
===============

@murphy2011measuring present two different versions of the SVOSM: a
quasi-continuous web-based measure using sliders, and a discrete
paper-based version capturing the important features of the web-based
version, which some researchers find easier to administer. For
performance reasons, the z-Tree implementation is based on the discrete
version. The oTree implementation is based on the continuous version.

Our implementation is customizable to allow the user to select different
matching protocols, multiple languages, scaling payoffs, and ordering
and subsets of items. Table
[\[tab:parameters\]](#tab:parameters){reference-type="ref"
reference="tab:parameters"} gives an overview of the important
parameters of the implementation.

`Matching`
----------

A major addition to the original publication is that we add a
`RANDOM_DICTATOR` matching protocol to the `RING` matching protocol used
by @murphy2011measuring. Assuming four decision makers, A, B, C, and D,
in the `RING` protocol A gives to B, B gives to C, C gives to D and D
gives to A (see left side of Figure [1](#matching){reference-type="ref"
reference="matching"}). Each subject is both a sender and a receiver,
but in each role is matched with a different person. The `RING` matching
works with any number of subjects *greater than 1*.

In the `RANDOM_DICTATOR` matching (right side of Figure
[1](#matching){reference-type="ref" reference="matching"}), subjects
A,B,C,D are matched in groups of 2 (say (A; B) and (C;D)). Each subject
submits his/her choices in the SVOSM. Later, one member of each group
(say A and C) is randomly selected to be the sender, and the other (B
and D, respectively) is the receiver. In this case, B receives from A
and D receives from C. The choices by B and D are recorded but not
implemented. `RANDOM_DICTATOR` matching thus limits the interaction to
two subjects, where only one choice is finally implemented. This may
reduce chains of reciprocity, where A might give to B because she
expects to be compensated by D. The `RANDOM_DICTATOR` matching works
with any number of Subjects that is a *multiple of 2*.

The `RANDOM_DICTATOR` matching uses the strategy method; decisions are
only implemented with probability 1/2. It has been argued that such
decision making may be perceived as \"colder\", and thus may lead to
more strategic [@brandts2000hot] or normative choices
[@rauhut2010sociological].

![Matching protocols[]{label="matching"}](blob/master/matching.png)
width=".7\\textwidth"}\

`Main measures`
---------------

 [\[subsec:main\_measures\]]
label="subsec:main_measures"} The `svo_angle` is the core measure of the
SVOSM. It is calculated from the primary six items as
$$\arctan\left(\frac{\texttt{mean\_to\_other} - 50*\texttt{scale}}{\texttt{mean\_to\_self} - 50*\texttt{scale}}\right)$$

[see @murphy2011measuring for a detailed discussion].

The nine secondary items are used to calculate the
`inequality_aversion_score`, which distinguishes, for subjects
classified as prosocial according to the `svo_angle`, between efficiency
maximization and material equality motives. It is calculated as

$$\frac{\texttt{avg\_dist\_to\_equality}}{(\texttt{avg\_dist\_to\_equality+avg\_dist\_to\_joint})};$$

[see @murphy2011measuring for a detailed discussion].

z-Tree implementation
=====================

The z-Tree implementation of the SVOSM is a stand-alone treatment which
is easy to integrate in existing z-Tree treatments. It was created in
z-Tree 3.36 and can be used as any other treatment.

After implementing a slider-based version with real-time display of the
slider's position in z-Tree, we experienced *serious* time delays,
causing the server to freeze for up to several minutes. Whether this was
due to network traffic or to excessive read-and-write activities on the
hard drive could not finally be settled, but slightly increased
performance after switching to a solid state drive points towards the
latter cause. These problems finally led us to implement a
point-and-click version of the SVOSM, heavily reducing network traffic
as well as hard drive usage.

Our implementation of the SVOSM provides all the features of the
paper-based version of the SVOSM, except for interior decisions (i.e.,
choices which are in between the discrete values on the scale). Note
that while such interior decisions are possible in principle, they are
very rarely used in practice.[^1]

![Screenshot of the z-Tree decision](https://github.com/drfwint/svo/blob/master/blob/master/fig4.png)






Parameters are set in PARAMETERS
--------------------------------

This section describes parameters of the z-Tree treatment which can
easily be changed by the experimenter to match specific needs. Standard
parameters, e.g. number of subjects, are treated in the standard z-Tree
way. It is not necessary nor recommended to change the number of rounds
or groups. To change treatment specific parameters, open the globals
program "////INSERT PARAMETERS HERE ////" (see Figure
[2](#screenshot){reference-type="ref" reference="screenshot"}) and
change the respective values described below.

![Screenshot of the program indicating where to change setup
parameters](https://github.com/drfwint/svo/blob/master/blob/master/screenshot_program.png)


### `language`

Sets the language in which the SVOSM is displayed to the decision maker.
Implemented languages are English, French, German, and Italian. To add
additional languages, first declare the new language in the program
INTERNAL CONSTANTS, add the translations to all items, and finally
choose the language in the program PARAMETERS.

### `select_items`

Allows you to choose whether only the six primary items or all fifteen
items (six primary and nine secondary) are displayed. Using only the
secondary items is not possible.

### `items_in_random_order`

Determines whether items are displayed in the order presented in the
paper-based SVOSM as in @murphy2011measuring, or in random order. If the
`RANDOM` option is chosen, the order is randomized separately for each
subject.

### `matching`

Determines the matching procedure: `RING` or `RANDOM_DICTATOR` (see
subsection [1.1]
reference="subsec:matching"} and Figure
[1](#matching){reference-type="ref" reference="matching"}). `RING`
matching works with any number of subjects greater than 1.
`RANDOM_DICTATOR` matching works with any even number of subjects.

### `scale`

The scale of the circle underlying the SVOSM can be changed. The default
is `scale = 1`, which results in a circle with a diameter of 100
centered at (50,50), as in the original publication. Inputs greater than
1 scale the circle up (e.g. 2 results in a circle with a diameter of 200
centered at (100,100)); inputs smaller than 1 scale the circle down
(e.g. 0.5 results in a circle with a diameter of 50 centered at
(25,25)). Scaling may be useful if you want to present the decisions in
real monetary values and cannot afford to pay 100 €/\$/CHF/$\dots$

### `precision`

Determines the precision of the displayed values. This option is limited
to two modes---integers and two decimal digits---because z-Tree does not
allow for conditional layout of decimals. `INTEGERS` displays values as
integers, which is sensible for larger numbers, e.g. a circle with a
diameter of 100. For a circle with a small diameter, two decimals after
the point may be more appropriate (choose option
`TWO_DIGITS_AFTER_POINT`).

### `debug`

Displays debugging information, including a kill-button. Useful for
testing the treatment.

Output
------

The z-Tree treatment writes all the relevant output in the
subjects-table and calculates the important measures straight away,
making it possible to readily use the results in the experiment (e.g.
for matching purposes) and makes data analysis more convenient, since
all important measures are already in the data set. Most of the
variables in the subjects table are explained in Table
[\[tab:output\]]. Some of the output variables are only relevant
under specific parameters, e.g. `avg_dist_to_equality` is calculated
only if the secondary items are used. The rightmost column of table
[\[tab:output\]] indicates if and when the variables are used.

### `Profit`

The `Profit`-variable is built-in in z-Tree, and is automatically
written to the `TotalProfit`-variable in the session table. Thus, you
can use the profits earned in the SVOSM in later treatments. To
determine the profits, one of the sliders is randomly selected and the
corresponding earnings are written to the `Profit`-variable. If `RING`
matching is used, `Profit` contains the sum of the amount received as a
receiver and the amount kept as a sender. When the `RANDOM_DICTATOR`
option is chosen, `Profit` depends on the subjects role: If she was
chosen to be a sender, `Profit` returns the amount kept, and if she was
chosen to be a receiver, it returns the amount sent to her by the
sender.

### `svo_angle`

The `svo_angle` is the core measure of the SVOSM. The `svo_angle` is
stored in the subjects table *and* in the session table. Storing values
in the session table is useful if some of the SVOSM information is
required in other treatments later in the session.

### `svo_type`

`svo_type` assigns SVO types to specific value ranges of the
`svo_angle`. The following values are used: 1 = Altruist, 2 = Prosocial,
3 = Individualist, 4 = Competitive. Thresholds for assigining labers are
taken from @murphy2011measuring. `svo_type` is stored in the subjects
table *and* in the session table.

### `inequality_aversion_score`

The `inequality_aversion_score` is calculated from the secondary items
and is computed only if they are used. It is calculated only if the
subject is classified as being "prosocial" (see subsection
[\[subsec:main\_measures\]](#subsec:main_measures) above). In all other cases it is set
to -99. `inequality_aversion_score` is stored in the subjects table
*and* in the session table.

oTree implementation
====================

The oTree implementation of the SVOSM is implemented as a normal
oTree-app [@chen2016otree] and can be easily integrated in larger
experiments.[^2] Different from the z-Tree version, the oTree version is
based on the continuous version of the SVOSM and has a somewhat more
up-to-date layout. The interface includes a bar chart to show the
allocations to each player, but is fully customizable using HTML and
JavaScript. When implementing the SVOSM, we tried to use as much of the
standard oTree-dialect as possible, and only rely on common JavaScript
libraries compatible with oTree such as `HighCharts` or `jquery` when
necessary. These libraries are either already included or referenced in
the source code, so there is no need to install them manually. Important
parts of the code are implemented in JavaScript, so a fair amount of
knowledge may be helpful to make fundamental changes. Debugging for both
the oTree and JavaScript parts is possible with the internal oTree
debugger (See the oTree documentation). The JavaScript parts use cookies
to temporarily store information in the client's browser and issues a
notification the first time the page is opened.

![Screenshot of the oTree decision
screen](![Alternate image text](https://github.com/drfwint/svo/blob/master/blob/master/slider_moved.png)

[\[fig:otree\_screenshot\]]
label="fig:otree_screenshot"}

Setting the Parameters
----------------------

All relevant parameters can be set either in the file `settings.py` or,
more conveniently, directly in the oTree web interface when creating a
new session. Simply click on \"Sessions\" in the top panel of the admin
page and change the parameters described below as required. If you want
to set specific defaults, change them in `settings.py`.

In most cases the options available to the user are the same in the
oTree implementation as in the z-Tree one. In these cases we refer to
the relevant sections above. Other cases are discussed below.

### `LANGUAGE_CODE`

Sets the language in which the SVOSM is displayed to the decision maker.
Implemented languages are English, German, Italian, and French. Set
`LANGUAGE_CODE` to `’en’`, `’de’`, `’it’`, or `’fr’`. Please refer to
the oTree documentation on localization to learn how to add further
languages. `LANGUAGE_CODE` also sets the language for the cookie
warning.

### `select_items`

See section [2.1.2].

### `items_in_random_order`

See section [2.1.3].

### `matching`

See section [2.1.4].

### `scale`

See section [2.1.5].

### `precision`

See section [2.1.6].

Output
------

All relevant output, including the SVO-angle etc, can be downloaded in
CSV or XLS format in the standard oTree way via the web browser. The
data is stored internally, ready to be used within the experiment (e.g.
for matching purposes). Other than these differences, all details
regarding the output are the same as in the z-Tree implementation (see
[2.2].

### `payoff`

The `payoff`-variable is the standard oTree variable to calculate
payoffs. It is highly suggested to use this variable name, because it
makes e.g. the summing of payoffs over different apps easier. To
determine the profits, one of the sliders is randomly selected and the
corresponding earnings are written to the `payoff`-variable. If `RING`
matching is used, `payoff` contains the sum of the amount received as a
receiver and the amount kept as a sender. When the `RANDOM_DICTATOR`
option is chosen, `payoff` depends on the subjects role: If she was
chosen to be a sender, `payoff` returns the amount kept, and if she was
chosen to be a receiver, it returns the amount sent to her by the
sender.

### `svo_angle`

See section [2.2.2].

### `svo_type`

See section [2.2.3].

### `inequality_aversion_score`

See section [2.2.4].

Disclaimer
==========

The z-Tree treatment of the SVOSM is thoroughly tested and has been used
in several labs and experiments over the years. The oTree implementation
has also been tested thoroughly, but is much younger. As it has not been
circulated widely so far, it should be used with somewhat greater care
than the z-Tree version. Nevertheless, the authors disclaim all
warranties, expressed or implied, regarding the Software, including any
implied warranties of satisfactory quality, merchantability or fitness
for a particular purpose. The authors shall have no liability whatsoever
to the User of the Software for any direct, indirect, special or
consequential loss and/or expense (including loss of profit) suffered by
the User and arising out of a malfunctioning of the Software.

You can use, modify and distribute the corresponding treatments if you
agree with the above points. If you use these implementations of the
SVOSM, please cite the SVOSM as @murphy2011measuring and make sure to
follow the license agreements associated with z-Tree or oTree (in
particular to cite @fischbacher2007z, or @chen2016otree, respectively).

References
==========

Appendix
========




### Parameters in the z-Tree treatment

|  Parameter                | Values      | Description |
|----	|----	|---	|
| `language`               |`ENGLISH`                 | Language is English
||             `GERMAN`                  | Language is German
||             `ITALIAN`                 | Language is Italian
| `select_items`           |`PRIMARY`                 | only the primary items (items 1-6) are elicited.|
||               `FULL`     | primary and secondary items (items 1-15) are elicited|
| `items_in_random_order`  |`ORDERED`                 | items are presented according to the order in Murphy et al. (2011)|
||               `RANDOM`                  | items are presented in random order
| `matching`               |`RING`     | Subject A,B,C,D are ordered on a ring-structure as in Murphy et a. (2011). In this case, A gives to B, B gives to C, C gives to D and D gives to A, which makes everyone a sender AND a receiver.
||               `RANDOM_DICTATOR`         | Subjects A,B,C,D are matched in groups of 2 (say (A; B) and (C;D). One member of each group (say A and C) is selected to be the sender, the other one as receiver. In this case, B receives from A and D receives from C.
| `precision`              |`TWO_DIGITS_AFTER_POINT`  | values on sliders are rounded to two digits after decimal point|
||               `INTEGERS`                | values on sliders are rounded to integers
| `scale`                  |$(0, +\infty]$            | Parameter to scale up $(>1$) or down $(<1)$ all the numbers on a slider Default is 1, resulting in a circle of diameter 100
| `debug`                  |{1;0}      | set to 1 to display some debug info; set to 0 while running actual sessions|



  ### Relevant Variables in the Subjects Table

  | Relevant Variables in the Subjects Table  | Description |Relevant for Parameters
  | ----    | ----    | ----    |
 | `Subject`                     |unique identifier for the Subject               | always
 | `Group`                       |matching group of the Subject.                  | `matching=RANDOM_DICTATOR`
 | `Profit`                      |Profit of the Subject                           |   always
 | `input_self[i]`               |allocation to self in item `i`                  | always
 | `input_other[i]`              |allocation to other in item `i`                 | always
 | `random_order[i] `            |order of item `i` in `RANDOM` order             | `items_in_random_order = RANDOM`
 | `chosen_option[i]`            |chosen option on item i, counted from left to right (leftmost option = 1, rightmost option = 9)              |always
 | `mean_to_self`                |mean allocation to self in primary items        | always
 | `mean_to_other`               |mean allocation to other in primary items       | always
 | `svo_angle`    |svo angle calculated as $$\arctan\left(\frac{\texttt{mean\_to\_other} - 50*\texttt{scale}}{\texttt{\texttt{mean\_to\_self}} - 50*\texttt{scale}}\right)$$               |always
 | `svo_type`    | svo type,          |always|
||                 1 = Altruist $\Leftrightarrow$ `svo_angle` $>57.15$,
||                 2 = Prosocial $\Leftrightarrow$ $57.15 \geq$ `svo_angle` $>22.45$,            |
||                 3 = Individualist $\Leftrightarrow$ $22.45 \geq$ `svo_angle` $>-12.04$,       |
||                 4 = Competitive $\Leftrightarrow$ `svo_angle` $\geq-12.04$                    |
 | `avg_dist_to_equality`        |average standardized distance of the choice to the choice which would maximize equality       |`select_items = FULL`|
 | `avg_dist_to_altruist`        |average standardized distance of the choice to the choice which would maximize altruism       |`select_items = FULL`|
 | `avg_dist_to_joint`           |average standardized distance of the choice to the choice which would maximize joint earnings                |`select_items = FULL`
 | `avg_dist_to_indiv`           |average standardized distance of the choice to the choice which would maximize individual gains              |`select_items = FULL`
 | `not_altru_indiv`             |Dummy taking the value 1 if `avg_dist_equality`, `avg_dist_joint` $>$ `avg_dist_altruist`, `avg_dist_indiv` |                 `select_items = FULL`
 | `inequality_aversion_score`   |Degree of inequality aversion calculated as $$\frac{\texttt{avg\_dist\_to\_equality}}{(\texttt{avg\_dist\_to\_equality+avg\_dist\_to\_joint})}$$ if `not_altru_indiv` == 1, else -99)  | `select_items = FULL`|
 | `paid_slider`                 |slider selected for payment as sender            |always
 | `slider_as_receiver`          |slider selected for payment as receiver          |`matching=RING`
 | `kept_of_sender`              |amount kept by the sender         |`always`
 | `received_from_sender`        |amount received from the sender                  |`always`
 | `kept_as_sender`              |amount kept as sender             |`matching=RING`
 | `sent_as_sender`              |amount sent as sender             |`matching=RING`



### Parameters in the oTree treatment

 | Parameter                 | Values      | Description |
 |---- |---- |---- |
 | `language`              | `EN`       | Language is English
|                          |`DE`        | Language is German
|                          |`IT`        | Language is Italian
 | `select_items`          | `PRIMARY`   | only the primary items (items 1-6) are elicited.
|                          |`FULL`      | primary and secondary items (items 1-15) are elicited
 | `items_in_random_order` | `ORDERED`   | items are presented according to the order in Murphy et al. (2011)
|                          |`RANDOM`    | items are presented in random order
 | `matching`              | `RING`      | Subject A,B,C,D are ordered on a ring-structure as in Murphy et al. (2011). In this case, A gives to B, B gives to C, C gives to D and D gives to A, which makes everyone a sender AND a receiver.
|                          |`RANDOM_DICTATOR` | Subjects A,B,C,D are matched in groups of 2 (say (A; B) and (C;D). One member of each group (say A and C) is selected to be the sender, the other one as receiver. In this case, B receives from A and D receives from C.
 | `precision`             | `TWO_DIGITS_AFTER_POINT` | values on sliders are rounded to two digits after decimal point
|                          | `INTEGERS`                | values on sliders are rounded to
| `scale`                  |  $(0, +\infty]$           |Parameter to scale up $(>1$) or down $(<1)$ all the numbers on a slider. Default is 1, resulting in a circle of diameter 100
 | `random_payoff`         | `RAND`     | the payoff will be calculated as a random choice
|                          |  `SUM`     |  the payoff is the sum of all choices of the player
 | `item_initialization`   | `RAND`     | initialize the items in random manner
|                          |  `AVG`     |  initialize the items using average between min and max

### Relevant variables in the subjects table of the oTree


  |Relevant Variables |                Description         |Relevant for Parameters |
  |--- |--- |--- |
  |`payoff`                    | Profit of the Subject             | always
  |`input_self_X`              | The amount of money that the user has chosen for himself for item `X`          | always
  |`input_other_X`             | The amount of money that the user has chosen for others for item `X`            |always
  |`random_orderX `            | order of item `X` in `RANDOM` order              |`items_in_random_order = RANDOM`
  |`mean_to_self`              | mean allocation to self in primary items         | always
  |`mean_to_other`             | mean allocation to other in primary items        | always
  |`svo_angle`                 | svo angle calculated as $$\arctan\left(\frac{\texttt{mean\_to\_other} - 50*\texttt{scale}}{\texttt{\texttt{mean\_to\_self}}  - 50*\texttt{scale}}\right)$$                 |always
  |`svo_type`                  |svo type,          | always
||                            1 = Altruist $\Leftrightarrow$ `svo_angle` $>57.15$,
||                            2 = Prosocial $\Leftrightarrow$ $57.15 \geq$ `svo_angle` $>22.45$,
||                            3 = Individualist $\Leftrightarrow$ $22.45 \geq$ `svo_angle` $>-12.04$,
||                            4 = Competitive $\Leftrightarrow$ `svo_angle` $\geq-12.04$
  |`avg_dist_to_equality`      | average standardized distance of the choice to the choice which would maximize equality        |`select_items = FULL`
  |`avg_dist_to_altruist`      | average standardized distance of the choice to the choice which would maximize altruism        |`select_items = FULL`
  |`avg_dist_to_joint`         | average standardized distance of the choice to the choice which would maximize joint earnings                | `select_items = FULL`
  |`avg_dist_to_indiv`         | average standardized distance of the choice to the choice which would maximize individual gains              | `select_items = FULL`
  |`altru_indiv`               | Dummy taking the value `true` if `avg_dist_equality`, `avg_dist_joint` $\leq$ `avg_dist_altruist`, `avg_dist_indiv`          |`select_items = FULL`
  |`inequality_aversion_score` | Degree of inequality aversion calculated as $$\frac{\texttt{avg\_dist\_to\_equality}}{(\texttt{avg\_dist\_to\_equality+avg\_dist\_to\_joint})}$$ if `altru_indiv` == `true`, else -99)  | `select_items = FULL`
  |`paid_slider`               | slider selected for payment as sender            | `always`
  |`slider_as_receiver`        | slider selected for payment as receiver          | `always`
  |`kept_of_sender`            | amount kept by the sender          `always`
  |`received_from_sender`      | amount received from the sender                  |`always`


[^1]: Personal communication with R. Murphy.

[^2]: This version app was implemented in oTree version 2.1.9. Please
    update the app according to the documentation if a new version of
    oTree is released.
