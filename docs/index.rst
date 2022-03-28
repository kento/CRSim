CRSim Documentation

summary
=======

(a) simulate_cr function:.
Simulates multilevel C/R and outputs the results.

(b) optimize_cr function:.
Find the interval and L2_freq that maximizes the efficiency of the simulate_cr function, and output the simulation results at that time.

Development Details
~~~~~~~~~~~~~~~~~~~~

simulate_cr function
~~~~~~~~~~~~~~~~~~~~

.. _tuple-simulate_crinterval-l2ckpt_freq-l1ckpt_overhead-l2ckpt_latency-ckptrestarttimes-failrates-n-sn-g-g-alpha-check_interval-n_check_ok-n_failure_max-efficiency_log-1:

tuple simulate_cr(interval, L2ckpt_freq, L1ckpt_overhead, L2ckpt_latency, ckptRestartTimes, failRates, N, SN, G, g, alpha, check_interval, n_check_ok, n_failure_max, efficiency_log)

Argument (Input)

+----------------------+----------------------------+----------+---------------+
| **argument name**    | **Description.**           | **type** |               |
+======================+============================+==========+===============+
| **Interval**         | L1 Checkpoint interval     | int      | indispensable |
+----------------------+----------------------------+----------+---------------+
| **L2ckpt_frq**       | L2 Checkpoint Frequency    | int      | indispensable |
|                      |                            |          |               |
+----------------------+----------------------------+----------+---------------+
| **L1ckpt_overhead**  | Synchronization L1         | int      | indispensable |
|                      | Checkpoint time            |          |               |
+----------------------+----------------------------+----------+---------------+
| **L2ckpt_latency**   | Asynchronous L2 checkpoint | int      | indispensable |
|                      | time                       |          |               |
+----------------------+----------------------------+----------+---------------+
| **ckptRestartTimes** | Array of length 2          | List     | indispensable |
|                      | containing the time        |          |               |
|                      | required for L1,L2         | [int     |               |
|                      | recovery                   | ,int].   |               |
|                      |                            |          |               |
|                      | = [L1 recovery time,L2     |          |               |
|                      | recovery time].            |          |               |
+----------------------+----------------------------+----------+---------------+
| **failRates**        | Array of length 2          | List     | indispensable |
|                      | containing the number of   | [f       |               |
|                      | failures requiring L1,L2   | loat,f   |               |
|                      | recovery per unit time =   | loat].   |               |
|                      | [L1 failure times          |          |               |
|                      |                            |          |               |
|                      | Number,L2 Failure Count]   |          |               |
+----------------------+----------------------------+----------+---------------+
| **N**                | Total number of            | int      | indispensable |
|                      | computation nodes          |          |               |
+----------------------+----------------------------+----------+---------------+
| **SN**               | Number of spare nodes      | int      | indispensable |
|                      | \*Parameters added to the  |          |               |
|                      | specification              |          |               |
+----------------------+----------------------------+----------+---------------+
| **g**                | L1 Checkpoint group size   | int      | indispensable |
+----------------------+----------------------------+----------+---------------+
| **g**                | L1 Checkpoint Fault        | int      | indispensable |
|                      | Tolerance                  |          |               |
+----------------------+----------------------------+----------+---------------+
| **alpha**            | Threshold of change in     | float    | indispensable |
|                      | efficiency that terminates |          |               |
|                      | the simulation             |          |               |
|                      |                            |          |               |
|                      | value                      |          |               |
+----------------------+----------------------------+----------+---------------+
| **check_interval**   | Frequency of Efficiency    | int      | Optional,     |
|                      | change checks              |          | Default=1     |
|                      |                            |          |               |
|                      | Parameters added to the    |          |               |
|                      | specification              |          |               |
+----------------------+----------------------------+----------+---------------+
| **n_check_ok**       | Because it is judged to be | int      | Optional,     |
|                      | finished by the change     |          | Default=1     |
|                      | amount check of Efficiency |          |               |
|                      |                            |          |               |
|                      | Number of consecutive      |          |               |
|                      | times of \*Parameters      |          |               |
|                      | added to the specification |          |               |
+----------------------+----------------------------+----------+---------------+
| **n_failure_max**    | Maximum number of failures | int      | Optional,     |
|                      | \*Parameters added to the  |          | D             |
|                      | specification              |          | efault=500000 |
+----------------------+----------------------------+----------+---------------+
| **efficiency_log**   | Turn on/off the historical | bool     | Optional,     |
|                      | output of the Efficiency   |          | Default=False |
|                      | change check               |          |               |
|                      |                            |          |               |
|                      | Parameters added to the    |          |               |
|                      | specification              |          |               |
+----------------------+----------------------------+----------+---------------+

Return value (output): tuple type data = (X,A,B,C,D,E,F)

+--------------+------------------------------------------+-----------+
| **argument   | **Description.**                         |           |
| name**       |                                          | **type**  |
+==============+==========================================+===========+
| **an         | Efficiency = A/(B+C+D+F)                 |    float  |
| unknown**    |                                          |           |
+--------------+------------------------------------------+-----------+
| **A**        | real computation time                    |    float  |
+--------------+------------------------------------------+-----------+
| **B**        | Time spent in the calculation state      |    float  |
+--------------+------------------------------------------+-----------+
| **c**        | L1 Time spent at checkpoint              |    float  |
+--------------+------------------------------------------+-----------+
| **D**        | L1 Time spent in recovery                |    float  |
+--------------+------------------------------------------+-----------+
| **E**        | L2 Time spent on checkpoints             |    float  |
+--------------+------------------------------------------+-----------+
| **f**        | Time spent on L2 recovery                |    float  |
+--------------+------------------------------------------+-----------+

optimize_cr function
~~~~~~~~~~~~~~~~~~~~

.. _tuple-optimize_cr-l1ckpt_overhead-l2ckpt_latency-ckptrestarttimes-failrates-n-sn-g-g-alpha-check_interval-n_check_ok-n_failure_max-n_steps-log_interval-1:

tuple optimize_cr (L1ckpt_overhead, L2ckpt_latency, ckptRestartTimes, failRates, N, SN, G, g, alpha, check_interval, n_check_ok, n_failure_max, n_steps, log_interval)

.. _argument-input-1:

Argument (Input)

+----------------------+----------------------------+----------+---------------+
| **argument name**    | **Description.**           | **type** |               |
|                      |                            |          |               |
+======================+============================+==========+===============+
| **L1ckpt_overhead**  | Synchronization L1         | int      | indispensable |
|                      | Checkpoint time            |          |               |
+----------------------+----------------------------+----------+---------------+
| **L2ckkpt_latency**  | Asynchronous L2 checkpoint | int      | indispensable |
|                      | time                       |          |               |
+----------------------+----------------------------+----------+---------------+
| **ckptRestartTimes** | Array of length 2          | List     | indispensable |
|                      | containing the time        |          |               |
|                      | required for L1,L2         | [int     |               |
|                      | recovery                   | ,int].   |               |
|                      |                            |          |               |
|                      | = [L1 recovery time,L2     |          |               |
|                      | recovery time].            |          |               |
+----------------------+----------------------------+----------+---------------+
| **failRates**        | Array of length 2          | List     | indispensable |
|                      | containing the number of   | [f       |               |
|                      | failures requiring L1,L2   | loat,f   |               |
|                      | recovery per unit time =   | loat].   |               |
|                      | [L1 failure times          |          |               |
|                      |                            |          |               |
|                      | Number,L2 Failure Count]   |          |               |
+----------------------+----------------------------+----------+---------------+
| **N**                | Total number of            | int      | indispensable |
|                      | computation nodes          |          |               |
+----------------------+----------------------------+----------+---------------+
| **SN**               | Number of spare nodes      | int      | indispensable |
|                      | \*Parameters added to the  |          |               |
|                      | specification              |          |               |
+----------------------+----------------------------+----------+---------------+
| **g**                | L1 Checkpoint group size   | int      | indispensable |
+----------------------+----------------------------+----------+---------------+
| **g**                | L1 Checkpoint Fault        | int      | indispensable |
|                      | Tolerance                  |          |               |
+----------------------+----------------------------+----------+---------------+
| **alpha**            | Threshold of change in     | float    | indispensable |
|                      | efficiency that terminates |          |               |
|                      | the simulation             |          |               |
|                      |                            |          |               |
|                      | value                      |          |               |
+----------------------+----------------------------+----------+---------------+
| **check_interval**   | Frequency of Efficiency    | int      | Optional,     |
|                      | change checks              |          | Default=1     |
|                      |                            |          |               |
|                      | Parameters added to the    |          |               |
|                      | specification              |          |               |
+----------------------+----------------------------+----------+---------------+
| **n_check_ok**       | Because it is judged to be | int      | Optional,     |
|                      | finished by the change     |          | Default=1     |
|                      | amount check of Efficiency |          |               |
|                      |                            |          |               |
|                      | Number of consecutive      |          |               |
|                      | times of \*Parameters      |          |               |
|                      | added to the specification |          |               |
+----------------------+----------------------------+----------+---------------+
| **n_failure_max**    | Maximum number of failures | int      | Optional,     |
|                      | \*Parameters added to the  |          | D             |
|                      | specification              |          | efault=500000 |
+----------------------+----------------------------+----------+---------------+
| **n_steps**          | Number of optimization     | int      | Optional,     |
|                      | iterations \*Parameters    |          | Default=5000  |
|                      | added to specification     |          |               |
+----------------------+----------------------------+----------+---------------+
| **log_interval**     | Log output interval for    | int      | Optional,     |
|                      | optimization, 0 means no   |          | Default=100   |
|                      | output                     |          |               |
|                      |                            |          |               |
|                      | Parameters added to the    |          |               |
|                      | specification              |          |               |
+----------------------+----------------------------+----------+---------------+

Return value (output): tuple type data=(X,A,B,C,D,E,F, interval, L2ckpt_freq)

+-------------------+-------------------------------------------------+---------+
| **argument name** | **Description.**                                | **type**|
+===================+=================================================+=========+
| **an unknown**    | Efficiency = A/(B+C+D+F) at interval,           |         |
|                   | L2ckpt_freq of optimization results             | float   |
+-------------------+-------------------------------------------------+---------+
| **A**             | interval of optimization results, real          |         |
|                   | computation time at L2ckpt_freq                 | float   |
+-------------------+-------------------------------------------------+---------+
| **B**             | interval of optimization results, time spent in |         |
|                   | the computation state at L2ckpt_freq            | float   |
+-------------------+-------------------------------------------------+---------+
| **C**             | interval of optimization results, time spent on |         |
|                   | L1 checkpoint at L2ckpt_freq                    | float   |
+-------------------+-------------------------------------------------+---------+
| **D**             | interval of optimization results, time spent    |         |
|                   | for L1 recovery at L2ckpt_freq                  | float   |
+-------------------+-------------------------------------------------+---------+
| **E**             | interval of optimization results, time spent on |         |
|                   | L2 checkpoints during L2ckpt_freq               | float   |
+-------------------+-------------------------------------------------+---------+
| **f**             | interval of optimization results, time spent    |         |
|                   | for L2 recovery at L2ckpt_freq                  | float   |
+-------------------+-------------------------------------------------+---------+
| **interval**      | L1 checkpoint interval for optimization results |         |
|                   |                                                 |   int   |
+-------------------+-------------------------------------------------+---------+
| **L2ckpt_freq**   | Frequency of L2 checkpoints for optimization    |         |
|                   | results                                         |   int   |
+-------------------+-------------------------------------------------+---------+

Optimization Methodology
~~~~~~~~~~~~~~~~~~~~~~~~

An annealing method was used as the optimization technique.

Initial state
=============

Of the following combinations of interval and L2_freq_freq (24 combinations), the one with the highest efficiency is implemented as the initial state.

interval = 1000, 2500, 5000, 8000, 12000, 24000

L2_freq_freq = 1, 2, 5, 10

State Transition
================

The following four methods were considered for state transitions.

Method 1.
1. randomly select which value of interval or L2ckpt_freq to change 2. increase/decrease the selected parameter by 2%.

Method 2.
1. randomly select which value of interval or L2ckpt_freq to change 2. increase or decrease the selected parameter by a random value within 5%.

Method 3
1. increase/decrease both interval and L2ckpt_freq by a random value within 0-5%.

Method 4
1. randomly select which value of interval or L2ckpt_freq to change 2. increase/decrease the selected parameter by a fixed value


As a result of the study, Method 1 was adopted because none of the methods showed much difference except for Method 4 (*).

Because the interval has a wide range, when increasing or decreasing it by a fixed value, a small value causes too many times to move within the range, while a large value causes too large a change on the small side.

The above state transition methods can be changed to any of the above methods with a simple source code modification. The 2% and 5% numbers can also be changed only by modifying the corresponding parts of the source code.
