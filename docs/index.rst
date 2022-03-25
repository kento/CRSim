.. image:: /media/image.png
   :width: 11.6913in
   :height: 0.88298in

CRSim Documentation

Table of Contents

`1 Overview <#summary>`__\ `2 <#summary>`__

`2 Development
Details <#development-details>`__\ `2 <#development-details>`__

`2.1 simulate_cr
Function <#simulate_cr-function>`__\ `2 <#simulate_cr-function>`__

`2.2 optimize_cr
function <#optimize_cr-function>`__\ `4 <#optimize_cr-function>`__

summary
=======

(a) simulate_cr function:.
~~~~~~~~~~~~~~~~~~~~~~~~~~

Simulates multilevel C/R and outputs the results.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(b) optimize_cr function:.
~~~~~~~~~~~~~~~~~~~~~~~~~~

Find the interval and L2_freq that maximizes the efficiency of the simulate_cr function, and output the simulation results at that time.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

2. .. rubric:: Development Details
      :name: development-details

   1. .. rubric:: simulate_cr function
         :name: simulate_cr-function

tuple simulate_cr(interval, L2ckpt_freq, L1ckpt_overhead, L2ckpt_latency, ckptRestartTimes, failRates, N, SN, G, g, alpha, check_interval, n_check_ok, n_failure_max, efficiency_log)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Argument (Input)
~~~~~~~~~~~~~~~~

+---------------+----------------------------+--------+---------------+
| **argument    | **Description.**           | **type |               |
| name**        |                            | (e.g.  |               |
|               |                            | of     |               |
|               |                            | ma     |               |
|               |                            | chine, |               |
|               |                            | goods, |               |
|               |                            | e      |               |
|               |                            | tc.)** |               |
+===============+============================+========+===============+
| **Interval**  | L1 Checkpoint interval     | int    | indispensable |
+---------------+----------------------------+--------+---------------+
| **            | L2 Checkpoint Frequency    | int    | indispensable |
| L2ckpt_freq** |                            |        |               |
+---------------+----------------------------+--------+---------------+
| **L1ck        | Synchronization L1         | int    | indispensable |
| pt_overhead** | Checkpoint time            |        |               |
+---------------+----------------------------+--------+---------------+
| **L2c         | Asynchronous L2 checkpoint | int    | indispensable |
| kpt_latency** | time                       |        |               |
+---------------+----------------------------+--------+---------------+
| **ckptR       | Array of length 2          | List   | indispensable |
| estartTimes** | containing the time        |        |               |
|               | required for L1,L2         | [int   |               |
|               | recovery                   | ,int]. |               |
|               |                            |        |               |
|               | = [L1 recovery time,L2     |        |               |
|               | recovery time].            |        |               |
+---------------+----------------------------+--------+---------------+
| **failRates** | Array of length 2          | List   | indispensable |
|               | containing the number of   | [f     |               |
|               | failures requiring L1,L2   | loat,f |               |
|               | recovery per unit time =   | loat]. |               |
|               | [L1 failure times          |        |               |
|               |                            |        |               |
|               | Number,L2 Failure Count]   |        |               |
+---------------+----------------------------+--------+---------------+
| **N**         | Total number of            | int    | indispensable |
|               | computation nodes          |        |               |
+---------------+----------------------------+--------+---------------+
| **SN**        | Number of spare nodes      | int    | indispensable |
|               | \*Parameters added to the  |        |               |
|               | specification              |        |               |
+---------------+----------------------------+--------+---------------+
| **g**         | L1 Checkpoint group size   | int    | indispensable |
+---------------+----------------------------+--------+---------------+
| **g**         | L1 Checkpoint Fault        | int    | indispensable |
|               | Tolerance                  |        |               |
+---------------+----------------------------+--------+---------------+
| **alpha**     | Threshold of change in     | float  | indispensable |
|               | efficiency that terminates |        |               |
|               | the simulation             |        |               |
|               |                            |        |               |
|               | value                      |        |               |
+---------------+----------------------------+--------+---------------+
| **che         | Frequency of Efficiency    | int    | Optional,     |
| ck_interval** | change checks              |        | Default=1     |
|               |                            |        |               |
|               | Parameters added to the    |        |               |
|               | specification              |        |               |
+---------------+----------------------------+--------+---------------+
| *             | Because it is judged to be | int    | Optional,     |
| *n_check_ok** | finished by the change     |        | Default=1     |
|               | amount check of Efficiency |        |               |
|               |                            |        |               |
|               | Number of consecutive      |        |               |
|               | times of \*Parameters      |        |               |
|               | added to the specification |        |               |
+---------------+----------------------------+--------+---------------+
| **n_          | Maximum number of failures | int    | Optional,     |
| failure_max** | \*Parameters added to the  |        | D             |
|               | specification              |        | efault=500000 |
+---------------+----------------------------+--------+---------------+
| **eff         | Turn on/off the historical | bool   | Optional,     |
| iciency_log** | output of the Efficiency   |        | Default=False |
|               | change check               |        |               |
|               |                            |        |               |
|               | Parameters added to the    |        |               |
|               | specification              |        |               |
+---------------+----------------------------+--------+---------------+

Return value (output): tuple type data = (X,A,B,C,D,E,F)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+---------------+----------------------------------------------+------+
| **argument    | **Description.**                             |      |
| name**        |                                              |   ** |
|               |                                              | type |
|               |                                              |    ( |
|               |                                              | e.g. |
|               |                                              |      |
|               |                                              |   of |
|               |                                              |      |
|               |                                              | mach |
|               |                                              | ine, |
|               |                                              |      |
|               |                                              |   go |
|               |                                              | ods, |
|               |                                              |      |
|               |                                              |  etc |
|               |                                              | .)** |
+===============+==============================================+======+
| **an          | Efficiency = A/(B+C+D+F)                     |    f |
| unknown**     |                                              | loat |
+---------------+----------------------------------------------+------+
| **A**         | real computation time                        |    f |
|               |                                              | loat |
+---------------+----------------------------------------------+------+
| **B**         | Time spent in the calculation state          |    f |
|               |                                              | loat |
+---------------+----------------------------------------------+------+
| **c**         | L1 Time spent at checkpoint                  |    f |
|               |                                              | loat |
+---------------+----------------------------------------------+------+
| **D**         | L1 Time spent in recovery                    |    f |
|               |                                              | loat |
+---------------+----------------------------------------------+------+
| **E**         | L2 Time spent on checkpoints                 |    f |
|               |                                              | loat |
+---------------+----------------------------------------------+------+
| **f**         | Time spent on L2 recovery                    |    f |
|               |                                              | loat |
+---------------+----------------------------------------------+------+

optimize_cr function
--------------------

tuple optimize_cr (L1ckpt_overhead, L2ckpt_latency, ckptRestartTimes, failRates, N, SN, G, g, alpha, check_interval, n_check_ok, n_failure_max, n_steps, log_interval)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _argument-input-1:

Argument (Input)
~~~~~~~~~~~~~~~~

+---------------+----------------------------+--------+---------------+
| **argument    | **Description.**           | **type |               |
| name**        |                            | (e.g.  |               |
|               |                            | of     |               |
|               |                            | ma     |               |
|               |                            | chine, |               |
|               |                            | goods, |               |
|               |                            | e      |               |
|               |                            | tc.)** |               |
+===============+============================+========+===============+
| **L1ck        | Synchronization L1         | int    | indispensable |
| pt_overhead** | Checkpoint time            |        |               |
+---------------+----------------------------+--------+---------------+
| **L2c         | Asynchronous L2 checkpoint | int    | indispensable |
| kpt_latency** | time                       |        |               |
+---------------+----------------------------+--------+---------------+
| **ckptR       | Array of length 2          | List   | indispensable |
| estartTimes** | containing the time        |        |               |
|               | required for L1,L2         | [int   |               |
|               | recovery                   | ,int]. |               |
|               |                            |        |               |
|               | = [L1 recovery time,L2     |        |               |
|               | recovery time].            |        |               |
+---------------+----------------------------+--------+---------------+
| **failRates** | Array of length 2          | List   | indispensable |
|               | containing the number of   | [f     |               |
|               | failures requiring L1,L2   | loat,f |               |
|               | recovery per unit time =   | loat]. |               |
|               | [L1 failure times          |        |               |
|               |                            |        |               |
|               | Number,L2 Failure Count]   |        |               |
+---------------+----------------------------+--------+---------------+
| **N**         | Total number of            | int    | indispensable |
|               | computation nodes          |        |               |
+---------------+----------------------------+--------+---------------+
| **SN**        | Number of spare nodes      | int    | indispensable |
|               | \*Parameters added to the  |        |               |
|               | specification              |        |               |
+---------------+----------------------------+--------+---------------+
| **g**         | L1 Checkpoint group size   | int    | indispensable |
+---------------+----------------------------+--------+---------------+
| **g**         | L1 Checkpoint Fault        | int    | indispensable |
|               | Tolerance                  |        |               |
+---------------+----------------------------+--------+---------------+
| **alpha**     | Threshold of change in     | float  | indispensable |
|               | efficiency that terminates |        |               |
|               | the simulation             |        |               |
|               |                            |        |               |
|               | value                      |        |               |
+---------------+----------------------------+--------+---------------+
| **che         | Frequency of Efficiency    | int    | Optional,     |
| ck_interval** | change checks              |        | Default=1     |
|               |                            |        |               |
|               | Parameters added to the    |        |               |
|               | specification              |        |               |
+---------------+----------------------------+--------+---------------+
| *             | Because it is judged to be | int    | Optional,     |
| *n_check_ok** | finished by the change     |        | Default=1     |
|               | amount check of Efficiency |        |               |
|               |                            |        |               |
|               | Number of consecutive      |        |               |
|               | times of \*Parameters      |        |               |
|               | added to the specification |        |               |
+---------------+----------------------------+--------+---------------+
| **n_          | Maximum number of failures | int    | Optional,     |
| failure_max** | \*Parameters added to the  |        | D             |
|               | specification              |        | efault=500000 |
+---------------+----------------------------+--------+---------------+
| **n_steps**   | Number of optimization     | int    | Optional,     |
|               | iterations \*Parameters    |        | Default=5000  |
|               | added to specification     |        |               |
+---------------+----------------------------+--------+---------------+
| **l           | Log output interval for    | int    | Optional,     |
| og_interval** | optimization, 0 means no   |        | Default=100   |
|               | output                     |        |               |
|               |                            |        |               |
|               | Parameters added to the    |        |               |
|               | specification              |        |               |
+---------------+----------------------------+--------+---------------+

Return value (output): tuple type data=(X,A,B,C,D,E,F, interval, L2ckpt_freq)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+---------------+----------------------------------------------+------+
| **argument    | **Description.**                             |      |
| name**        |                                              |   ** |
|               |                                              | type |
|               |                                              |    ( |
|               |                                              | e.g. |
|               |                                              |      |
|               |                                              |   of |
|               |                                              |      |
|               |                                              | mach |
|               |                                              | ine, |
|               |                                              |      |
|               |                                              |   go |
|               |                                              | ods, |
|               |                                              |      |
|               |                                              |  etc |
|               |                                              | .)** |
+===============+==============================================+======+
| **an          | Efficiency = A/(B+C+D+F) at interval,        |    f |
| unknown**     | L2ckpt_freq of optimization results          | loat |
+---------------+----------------------------------------------+------+
| **A**         | interval of optimization results, real       |    f |
|               | computation time at L2ckpt_freq              | loat |
+---------------+----------------------------------------------+------+
| **B**         | interval of optimization results, time spent |    f |
|               | in the computation state at L2ckpt_freq      | loat |
+---------------+----------------------------------------------+------+
| **C**         | interval of optimization results, time spent |    f |
|               | on L1 checkpoint at L2ckpt_freq              | loat |
+---------------+----------------------------------------------+------+
| **D**         | interval of optimization results, time spent |    f |
|               | for L1 recovery at L2ckpt_freq               | loat |
+---------------+----------------------------------------------+------+

+---------------+----------------------------------------------+------+
| **E**         | interval of optimization results, time spent |    f |
|               | on L2 checkpoints during L2ckpt_freq         | loat |
+===============+==============================================+======+
| **f**         | interval of optimization results, time spent |    f |
|               | for L2 recovery at L2ckpt_freq               | loat |
+---------------+----------------------------------------------+------+
| **interval**  | L1 checkpoint interval for optimization      |      |
|               | results                                      |  int |
+---------------+----------------------------------------------+------+
| **            | Frequency of L2 checkpoints for optimization |      |
| L2ckpt_freq** | results                                      |  int |
+---------------+----------------------------------------------+------+

-  .. rubric:: Optimization Methodology
      :name: optimization-methodology

An annealing method was used as the optimization technique.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Initial state
~~~~~~~~~~~~~

Of the following combinations of interval and L2_freq_freq (24 combinations), the one with the highest efficiency is implemented as the initial state.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

interval = 1000, 2500, 5000, 8000, 12000, 24000
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L2_freq_freq = 1, 2, 5, 10
~~~~~~~~~~~~~~~~~~~~~~~~~~

State Transition
~~~~~~~~~~~~~~~~

The following four methods were considered for state transitions.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Method 1.
~~~~~~~~~

1. randomly select which value of interval or L2ckpt_freq to change 2. increase/decrease the selected parameter by 2%.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Method 2.
~~~~~~~~~

1. randomly select which value of interval or L2ckpt_freq to change 2. increase or decrease the selected parameter by a random value within 5%.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Method 3
~~~~~~~~

1. increase/decrease both interval and L2ckpt_freq by a random value within 0-5%.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Method 4
~~~~~~~~

1. randomly select which value of interval or L2ckpt_freq to change 2. increase/decrease the selected parameter by a fixed value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As a result of the study, Method 1 was adopted because none of the methods showed much difference except for Method 4 (*).
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because the interval has a wide range, when increasing or decreasing it by a fixed value, a small value causes too many times to move within the range, while a large value causes too large a change on the small side.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The above state transition methods can be changed to any of the above methods with a simple source code modification. The 2% and 5% numbers can also be changed only by modifying the corresponding parts of the source code.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
