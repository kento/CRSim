# Checkpoint restart simulator
#  version: 1.0
#  date: 2021/02/04

import random
import math

def main():
    # sample settings
    interval = 2000
    L2ckpt_freq = 4
    L1ckpt_overhead = 200
    L2ckpt_latency = 6000
    ckptRestartTimes = [200, 6000]
    failRates = [1e-5, 1e-6]
    N = 1000
    SN = 1000000
    G = 4
    g = 1
    alpha = 1e-3
    chk_interval = 1000
    n_check_ok = 1

    # set debug print flag
    #CheckpointRestartSimulator.debug_flag = True
    #CheckpointRestartSimulator.debug_level = 2  # 1 or 2
    #CheckpointRestartSimulator.debug_flag_opt = True

    mode = 0 # 0:simulation(simulate_cr), 1:optimization(optimize_cr)

    # simulation
    if mode == 0:
        print("*** Simulation Start ***")
        rtn_vals = simulate_cr(interval, L2ckpt_freq, L1ckpt_overhead,
            L2ckpt_latency, ckptRestartTimes, failRates, N, SN, G, g, alpha,
            check_interval=chk_interval, n_check_ok=n_check_ok,
            n_failure_max = 500000, efficiency_log=True)

        print("efficiency               = %f" % rtn_vals[0])
        print("actual computation time  = %f" % rtn_vals[1])
        print("total compute state time = %f" % rtn_vals[2])
        print("total L1 overhead time   = %f" % rtn_vals[3])
        print("total L1 recovery time   = %f" % rtn_vals[4])
        print("total L2 overhead time   = %f" % rtn_vals[5])
        print("total L2 recovery time   = %f" % rtn_vals[6])
        print("*** Simulation Complete ***")

    # optimization
    if mode == 1:
        print("*** Optimization Start ***")
        rtn_vals = optimize_cr(L1ckpt_overhead, L2ckpt_latency,
            ckptRestartTimes, failRates, N, SN, G, g, alpha,
            check_interval=chk_interval, n_check_ok=n_check_ok,
            n_steps=100, log_interval=10)

        print("\ninterval = %d  L2ckpt_freq = %d" % (rtn_vals[7], rtn_vals[8]))
        print("efficiency               = %f" % rtn_vals[0])
        print("actual computation time  = %f" % rtn_vals[1])
        print("total compute state time = %f" % rtn_vals[2])
        print("total L1 overhead time   = %f" % rtn_vals[3])
        print("total L1 recovery time   = %f" % rtn_vals[4])
        print("total L2 overhead time   = %f" % rtn_vals[5])
        print("total L2 recovery time   = %f" % rtn_vals[6])
        print("*** Optimization Complete ***")

def simulate_cr(
        interval, L2ckpt_freq, L1ckpt_overhead, L2ckpt_latency,
        ckptRestartTimes, failRates, N, SN, G, g, alpha,
        check_interval=1, n_check_ok=1, n_failure_max=500000,
        efficiency_log=False):
    """
    Simulate checkpoint restart process and return efficiency etc.

    arguments:
        interval(int) -- interval between L1 checkpoints
        L2ckptfreq(int) -- frequency of L2 checkpoints
        L1ckpt_overhead(int) -- overhead time of L1 checkpoint
        L2ckpt_latency(int) -- latency time of L1 checkpoint
        ckptRestartTimes(list) -- recovery time [L1, L2]
        failRates(list) -- failure frequency per sec. [L1, L2]
        N(int) -- number of nodes
        SN(int) -- number of spare nodes
        G(int) -- number of nodes in group
        g(int) -- disability tolerance
        alpha(float) -- threshold value to finish simulation
        check_interval(int) -- interval of checking amount of change in efficiency
        n_check_ok(int) -- number of continuous ok at checking efficiency
        n_failure_max(int) -- maximum failure occurrence limit
        efficiency_log(bool) -- flag to specify output of efficiency log

    return (X, A, B, C, D, E, F)
        X -- efficiency = A/(B+C+D+F)
        A -- actual computation time
        B -- total spent time of compute state
        C -- total spent time to create L1 checkpoints
        D -- total spent time to recovery from L1 checkpoints
        E -- total spent time to create L2 checkpoints
        F -- total spent time to recovery from L2 checkpoints
    """

    # check list parameters
    if type(ckptRestartTimes) is not list:
        print("[Error] ckptRestartTimes is not list!")
        return (0, 0, 0, 0, 0, 0, 0)
    if len(ckptRestartTimes) < 2:
        print("[Error] invalid list size of ckptRestartTimes!")
        return (0, 0, 0, 0, 0, 0, 0)
    if type(failRates) is not list:
        print("[Error] failRates is not list!")
        return (0, 0, 0, 0, 0, 0, 0)
    if len(failRates) < 2:
        print("[Error] invalid list size of failRates!")
        return (0, 0, 0, 0, 0, 0, 0)

    latency_times = [L1ckpt_overhead, L2ckpt_latency]
    overhead_times = [L1ckpt_overhead, 0]

    # create CheckpointRestartSimulator object
    cr = CheckpointRestartSimulator(
        interval, L2ckpt_freq, latency_times, overhead_times,
        ckptRestartTimes, failRates, N, SN, G, g, alpha)

    # following parameters are set by setter function.
    cr.set_eff_print(efficiency_log)
    cr.set_check_interval(check_interval)
    cr.set_n_check_ok(n_check_ok)
    cr.set_num_failure_max(n_failure_max)

    # execute simulation
    efficiency = cr.simulate()

    # get times
    time_info = cr.get_time_info()

    # get actual failure count
    #cnt_fail = cr.get_cnt_failure()

    # delete CheckpointRestartSimulator object
    del cr

    return (efficiency,
            time_info[0], time_info[1], time_info[2],
            time_info[3], time_info[4], time_info[5])

def optimize_cr(
        L1ckpt_overhead, L2ckpt_latency,
        ckptRestartTimes, failRates, N, SN, G, g, alpha,
        check_interval=1, n_check_ok=1, n_failure_max=500000,
        n_steps=5000, log_interval=100):
    """
    Optimize checkpoint restart process and return the optimized efficiency,
    interval and L2ckpt_freq.

    arguments:
        L1ckpt_overhead(int) -- overhead time of L1 checkpoint
        L2ckpt_latency(int) -- latency time of L1 checkpoint
        ckptRestartTimes(list) -- recovery time [L1, L2]
        failRates(list) -- failure frequency per sec. [L1, L2]
        N(int) -- number of nodes
        SN(int) -- number of spare nodes
        G(int) -- number of nodes in group
        g(int) -- disability tolerance
        alpha(float) -- threshold value to finish simulation
        check_interval(int) -- interval of checking amount of change in efficiency
        n_check_ok(int) -- number of continuous ok at checking efficiency
        n_failure_max(int) -- maximum failure occurrence limit
        n_steps(int) -- number of iterations in optimazation
        log_interval(int) -- interval of log output


    return (X, A, B, C, D, E, F, interval, L2ckpt_freq)
        X -- efficiency = A/(B+C+D+F)
        A -- actual computation time
        B -- total spent time of compute state
        C -- total spent time to create L1 checkpoints
        D -- total spent time to recovery from L1 checkpoints
        E -- total spent time to create L2 checkpoints
        F -- total spent time to recovery from L2 checkpoints
        interval -- optimized interval between L1 checkpoints
        L2ckpt_freq -- optimized frequency of L2 checkpoints
    """

    # check list parameters
    if type(ckptRestartTimes) is not list:
        print("[Error] ckptRestartTimes is not list!")
        return (0, 0, 0, 0, 0, 0, 0, 0, 0)
    if len(ckptRestartTimes) < 2:
        print("[Error] invalid list size of ckptRestartTimes!")
        return (0, 0, 0, 0, 0, 0, 0, 0, 0)
    if type(failRates) is not list:
        print("[Error] failRates is not list!")
        return (0, 0, 0, 0, 0, 0, 0, 0, 0)
    if len(failRates) < 2:
        print("[Error] invalid list size of failRates!")
        return (0, 0, 0, 0, 0, 0, 0, 0, 0)

    latency_times = [L1ckpt_overhead, L2ckpt_latency]
    overhead_times = [L1ckpt_overhead, 0]

    # create CheckpointRestartSimulator object
    cr = CheckpointRestartSimulator(
        1, 1, latency_times, overhead_times,
        ckptRestartTimes, failRates, N, SN, G, g, alpha)
    cr.set_check_interval(check_interval)
    cr.set_n_check_ok(n_check_ok)
    cr.set_num_failure_max(n_failure_max)

    # execute optimization
    efficiency, interval, L2ckpt_freq = cr.optimize(
        n_steps=n_steps, delta=[2, 2], log_interval=log_interval)
    #efficiency, interval, L2ckpt_freq = cr.optimize(
    #    n_steps=n_steps, delta=[10, 5], move_mode=1, log_interval=log_interval)
    #efficiency, interval, L2ckpt_freq = cr.optimize(
    #    n_steps=n_steps, delta=[10, 5], move_mode=2, log_interval=log_interval)
    #efficiency, interval, L2ckpt_freq = cr.optimize_simple()

    # get times
    time_info = cr.get_time_info()

    # delete CheckpointRestartSimulator object
    del cr

    if efficiency is None:
        return (0, 0, 0, 0, 0, 0, 0, 0, 0)

    return (efficiency, time_info[0], time_info[1], time_info[2],
            time_info[3], time_info[4], time_info[5], interval, L2ckpt_freq)


class CheckpointRestartSimulator():
    """ Simulate checkpoint restart process. """

    print_flag = True # Flag to specify if print error/warning messages.
    debug_flag = False # Flag to specify if print debug messages.
    debug_level = 1 # 1:print basic parameters. 2:print detail parameters.
    debug_flag_opt = False # Flag to specify if print debug messages in optimization.

    def __init__(self, interval = 1, L2ckpt_freq = 10,
                 latency_times = [0, 0], overhead_times = [0, 0],
                 ckptRestartTimes = [0, 0], failRates = [0, 0],
                 n_nodes = 1000000, n_spare_nodes = 1000000,
                 n_nodes_in_group = 4, disability_tolerance = 1,
                 alpha = 1e-6):
        self.interval = interval
        self.L2ckpt_freq = L2ckpt_freq
        if len(latency_times) == 2:
            self.ckpt_latency_times = [0, latency_times[0], latency_times[1]]
        else:
            self.ckpt_latency_times = [0, 0, 0]
        if len(overhead_times) == 2:
            self.ckpt_overhead_times = [0, overhead_times[0], overhead_times[1]]
        else:
            self.ckpt_overhead_times = [0, 0, 0]
        if len(ckptRestartTimes) == 2:
            self.restart_times = [0, ckptRestartTimes[0], ckptRestartTimes[1]]
        else:
            self.restart_times = [0, 0, 0]
        if len(failRates) == 2:
            self.fail_rates = [0, failRates[0], failRates[1]]
        else:
            self.failRates = [0, 0, 0]
        self.n_nodes = n_nodes
        self.n_spare_nodes = n_spare_nodes
        self.n_nodes_in_group = n_nodes_in_group
        self.disability_tolerance = disability_tolerance
        self.alpha = alpha

        self.eff_print = False
        self.check_interval = 100
        self.num_failure_max = 500000 # to avoid endless loop
        self.n_check_ok = 1

        self.cnt_check_ok = 0 # count of continuous ok at checking efficiency
        self.cnt_failures = [0, 0, 0, 0, 0, 0] # count of failures
        self.cnt_group_failure = 0 # count of checkpoint level up (L1 -> L2)
        self.elapsed_time = 0
        self.time_compute_act = 0.0
        self.time_compute = 0.0
        self.time_ckpt = [0.0, 0.0, 0.0]
        self.time_recovery = [0.0, 0.0, 0.0]

    # setter and getter functions
    def set_interval(self, ival):
        self.interval = ival

    def get_interval(self):
        return self.interval

    def set_L2ckpt_freq(self, ival):
        self.L2ckpt_freq = ival

    def get_L2ckpt_freq(self):
        return self.L2ckpt_freq

    def set_ckpt_latency_times(self, ivals):
        if type(ivals) is list:
            if len(ivals) == 2:
                self.ckpt_latency_times = [0, ivals[0], ivals[1]]

    def get_ckpt_latency_times(self):
        return self.ckpt_latency_times[1:3]

    def set_ckpt_overhead_times(self, ivals):
        if type(ivals) is list:
            if len(ivals) == 2:
                self.ckpt_overhead_times = [0, ivals[0], ivals[1]]

    def get_ckpt_overhead_times(self):
        return self.ckpt_overhead_times[1:3]

    def set_restart_times(self, ivals):
        if type(ivals) is list:
            if len(ivals) == 2:
                self.restart_times = [0, ivals[0], ivals[1]]

    def get_restart_times(self):
        return self.restart_times[1:3]

    def set_fail_rates(self, fvals):
        if type(fvals) is list:
            if len(fvals) == 2:
                self.fail_rates = [0, fvals[0], fvals[1]]

    def get_fail_rates(self):
        return self.fail_rates[1:3]

    def set_n_nodes(self, ival):
        self.n_nodes = ival

    def get_n_nodes(self):
        return self.n_nodes

    def set_n_spare_nodes(self, ival):
        self.n_spare_nodes = ival

    def get_n_spare_nodes(self):
        return self.n_spare_nodes

    def set_n_nodes_in_group(self, ival):
        self.n_nodes_in_group = ival

    def get_n_nodes_in_group(self):
        return self.n_nodes_in_group

    def set_disability_tolerance(self, ival):
        self.disability_tolerance = ival

    def get_disability_tolerance(self):
        return self.disability_tolerance

    def set_alpha(self, fval):
        self.alpha = fval

    def get_alpha(self):
        return self.alpha

    def set_check_interval(self, ival):
        self.check_interval = ival

    def get_check_interval(self):
        return self.check_interval

    def set_eff_print(self, bval):
        self.eff_print = bval

    def get_eff_print(self):
        return self.eff_print

    def set_num_failure_max(self, ival):
        self.num_failure_max = ival

    def get_num_failure_max(self):
        return self.num_failure_max

    def set_n_check_ok(self, ival):
        self.n_check_ok = ival

    def get_n_check_ok(self):
        return self.n_check_ok

    def get_cnt_failure(self):
        return self.cnt_failures[0]

    def check_params(self):
        """ Check parameters and return result(True/False). """
        if type(self.interval) is not int:
            self.error_print("interval is NOT integer!")
            return False
        if self.interval < 0:
            self.error_print("invalid interval!")
            return False

        if type(self.L2ckpt_freq) is not int:
            self.error_print("L2ckpt_freq is NOT integer!")
            return False
        if self.L2ckpt_freq < 0:
            self.error_print("invalid L2ckpt_freq!")
            return False

        if type(self.ckpt_overhead_times[1]) is not int:
            self.error_print("L1ckpt_overhead is NOT integer!")
            return False
        if self.ckpt_overhead_times[1] < 0:
            self.error_print("invalid L1ckpt_overhead!")
            return False

        if type(self.ckpt_latency_times[2]) is not int:
            self.error_print("L2ckpt_latency is NOT integer!")
            return False
        if self.ckpt_latency_times[2] < 0:
            self.error_print("invalid L2ckpt_latency!")
            return False

        for i in range(3):
            if type(self.restart_times[i]) is not int:
                self.error_print("restart_times contains non-integers!")
                return False
            if self.restart_times[i] < 0:
                self.error_print("invalid restart_times!")
                return False

        for i in range(3):
            if type(self.fail_rates[i]) is not float:
                if type(self.fail_rates[i]) is not int:
                    self.error_print(
                        "failRates contains non-numeric values!"
                        )
                    return False
                else:
                    self.fail_rates[i] = float(self.fail_rates[i])
            if self.fail_rates[i] < 0:
                self.error_print("invalid failRates!")
                return False

        if type(self.n_nodes) is not int:
            self.error_print("N is NOT integer!")
            return False
        if self.n_nodes < 1:
            self.error_print("invalid N! (N > 0)")
            return False

        if type(self.n_spare_nodes) is not int:
            self.error_print("SN is NOT integer!")
            return False
        if self.n_spare_nodes < 0:
            self.error_print("invalid SN!")
            return False

        if type(self.n_nodes_in_group) is not int:
            self.error_print("G is NOT integer!")
            return False
        if self.n_nodes_in_group < 1 or self.n_nodes_in_group > self.n_nodes:
            self.error_print("invalid G! (1 <= G <= N)")
            return False

        if type(self.disability_tolerance) is not int:
            self.error_print("g is NOT integer!")
            return False
        if self.disability_tolerance < 1 or \
                self.disability_tolerance > self.n_nodes_in_group:
            self.error_print("invalid g! (1 <= g <= G)")
            return False

        if type(self.alpha) is not float:
            if type(self.alpha) is not int:
                self.error_print("alpha is non-numeric value!")
                return False
            else:
                self.alpha = float(self.alpha)
        if self.alpha <= 0.0 or self.alpha > 1.0:
            self.error_print("invalid alpha!")
            return False

        if type(self.check_interval) is not int:
            self.error_print("check_interval is NOT integer!")
            return False
        if self.check_interval < 1:
            self.error_print("invalid check_interval!")
            return False

        if type(self.n_check_ok) is not int:
            self.error_print("n_check_ok is NOT integer!")
            return False
        if self.n_check_ok < 1:
            self.error_print("invalid n_check_ok!")
            return False

        if type(self.num_failure_max) is not int:
            self.error_print("n_failure_max is NOT integer!")
            return False
        if self.num_failure_max < 1:
            self.error_print("invalid n_failure_max!")
            return False

        if type(self.eff_print) is not bool:
            self.error_print("efficiency_log is NOT bool!")
            return False

        return True

    def get_time_info(self):
        """ Return time information of the current simulation. """
        time_info = (
            self.time_compute_act, self.time_compute,
            self.time_ckpt[1], self.time_recovery[1],
            self.time_ckpt[2], self.time_recovery[2]
            )
        return time_info

    def simulate(self):
        """ Execute simulation and return efficiency. """
        # parameter check
        if not self.check_params():
            return 0.0

        self.debug_print("interval=%d" % self.interval)
        self.debug_print("L2ckpt_freq=%d" % self.L2ckpt_freq)
        self.debug_print("latency=%d, %d" % (self.ckpt_latency_times[1],
                                        self.ckpt_latency_times[2]))
        self.debug_print("overhead=%d, %d" % (self.ckpt_overhead_times[1],
                                         self.ckpt_overhead_times[2]))
        self.debug_print("restart=%d, %d" % (self.restart_times[1],
                                        self.restart_times[2]))
        self.debug_print("failure=%e, %e" % (self.fail_rates[1],
                                        self.fail_rates[2]))
        self.debug_print("N=%d" % self.n_nodes)
        self.debug_print("SN=%d" % self.n_spare_nodes)
        self.debug_print("G=%d" % self.n_nodes_in_group)
        self.debug_print("g=%d" % self.disability_tolerance)
        self.debug_print("alpha=%e" % self.alpha)
        self.debug_print("check_interval=%d" % self.check_interval)
        self.debug_print("n_check_ok=%d" % self.n_check_ok)
        self.debug_print("n_failure_max=%d" % self.num_failure_max)
        self.debug_print("efficiency_log=%s" % str(self.eff_print))

        ckpt = [None, 0, None]
        progress = 0
        self.elapsed_time = 0
        self.time_compute_act = 0.0
        self.time_compute = 0.0
        self.time_ckpt = [0.0, 0.0, 0.0]
        self.time_recovery = [0.0, 0.0, 0.0]
        self.cnt_failures = [0, 0, 0, 0, 0, 0] # count of failures
        self.cnt_group_failure = 0 # count of Checkpoint Level up (L1->L2)

        if self.interval == 0:
            # no L1 checkpoint
            if self.L2ckpt_freq == 0:
                time_to_fail, failure_level = self.next_failure(self.fail_rates)
                self.time_compute_act = time_to_fail
                self.time_compute = time_to_fail
                self.cnt_failures[0] += 1
                self.cnt_failures[failure_level] += 1
                self.note_print(
                    "interval and L2ckpt_freq are 0."
                    )
                return 1.0
            else:
                self.error_print(
                    "invalid condition: interval = 0 and L2ckpt_freq > 0"
                    )
                return 0.0
        else:
            segA = int(math.ceil(
                float(self.ckpt_latency_times[2])
                / (self.ckpt_latency_times[1]+self.interval)
                ))
            self.debug_print("segA=%d" % segA)
            if self.L2ckpt_freq > 0:
                ckpt[2] = -segA
                # check L2ckpt_freq
                if self.L2ckpt_freq - segA < 0:
                    self.error_print("too small L2ckpt_freq for interval, "
                        + "L1ckpt_overhead and L2ckpt_latency settings!\n"
                        + "        L2ckpt_freq >= %d" % segA)
                    return 0.0

        # both failure rates are 0.0: return 1.0
        if self.fail_rates[1] == 0.0 and self.fail_rates[2] == 0.0:
            self.note_print("both failure rates are 0.0.")
            eff = float(self.interval) \
                / (self.interval + self.ckpt_overhead_times[1])
            return eff

        # Create NodeManagement object.
        node_info = NodeManagement(self.n_nodes, self.n_spare_nodes,
                          self.n_nodes_in_group, self.disability_tolerance)

        state = 0 #0: compute + ckpt, n(>0) n-level recovery
        eff = -1.0
        flag_exit = False
        exit_msg = ""
        if self.eff_print:
            print("   count, efficiency, difference,   progress")
        for i in range(self.num_failure_max+1):
            if i == self.num_failure_max:
                flag_exit = True
                exit_msg = "beyond the maximum failure occurrence limit"
            if self.L2ckpt_freq == 0 and state == 2:
                exit_msg = "L2 failure occurred although L2ckpt_freq is 0."
            if flag_exit or (self.L2ckpt_freq == 0 and state == 2):
                self.time_compute_act = self.interval * progress + surplus_time
                if self.time_compute_act < 0.0:
                    self.time_compute_act = 0.0
                eff_new = self.time_compute_act / self.elapsed_time
                eff_delta = abs(eff - eff_new)
                if self.eff_print:
                    prog_print = progress
                    if prog_print < 0:
                        prog_print = 0
                    if i < self.check_interval:
                        print("%8d, %10.8f, ----------, %10d"
                                % (self.cnt_failures[0], eff_new, prog_print))
                    else:
                        print("%8d, %10.8f, %6.4e, %10d"
                            % (self.cnt_failures[0], eff_new, eff_delta, prog_print))
                if flag_exit:
                    self.warning_print("Simulation stopped! (" + exit_msg + ")")
                    self.warning_print("Efficiency was set to zero.")
                    eff = 0.0
                else:
                    self.note_print(exit_msg)
                    eff = eff_new
                break
            time_to_fail, failure_level = self.next_failure(self.fail_rates)
            current_time_to_fail = time_to_fail
            self.debug_print("=== time_to_fail: " + str(time_to_fail) + "===",2)
            surplus_time = 0.0 # surplus time of compute state when a failure occuerd.
            while True: # While time_to_fail > 0
                self.debug_print("STAR: PROG=" + str(progress)
                    + " STAT=" + str(state)
                    + " FLVL=" + str(failure_level)
                    + " CKPT=" + str(ckpt), 2)
                if state == 0: # compute state + ckpt state
                    current_time_to_fail -= self.interval
                    if current_time_to_fail < 0: # failure in comptue state
                        self.debug_print("failure in comptue state", 2)
                        self.cnt_failures[0] += 1
                        self.cnt_failures[failure_level] += 1
                        self.cnt_failures[3] += 1 # failure count of comp state
                        # calculate surplus time of compute state
                        surplus_time = current_time_to_fail + self.interval
                        self.time_compute += surplus_time
                        # register failure node
                        node_info.set_failure_node()
                        state = failure_level
                        progress_bk = progress
                        progress = self.rollback_to(ckpt, failure_level)
                        if progress is None:
                            if self.L2ckpt_freq == 0:
                                progress = progress_bk
                            else:
                                progress = 0
                        self.debug_print("  FAIL: PROG=" + str(progress)
                            + " STAT=" + str(state)
                            + " FLVL=" + str(failure_level)
                            + " TTFA=" + str(current_time_to_fail)
                            + " CKPT=" + str(ckpt), 2)
                        break
                    self.time_compute += self.interval
                    ckpt_level = 1
                    current_time_to_fail -= self.ckpt_overhead_times[ckpt_level]
                    if current_time_to_fail < 0: # failure in ckpt state
                        self.debug_print("failure in ckpt state", 2)
                        self.cnt_failures[0] += 1
                        self.cnt_failures[failure_level] += 1
                        self.cnt_failures[4] += 1 # failure count of chpt state
                        self.time_ckpt[ckpt_level] += (current_time_to_fail
                            + self.ckpt_overhead_times[ckpt_level])
                        # register failure node
                        node_info.set_failure_node()
                        state = failure_level
                        progress_bk = progress
                        progress = self.rollback_to(ckpt, failure_level)
                        if progress is None:
                            if self.L2ckpt_freq == 0:
                                progress = progress_bk
                            else:
                                progress = 0
                        self.debug_print("  FAIL: PROG=" + str(progress)
                            + " STAT=" + str(state)
                            + " FLVL=" + str(failure_level)
                            + " TTFA=" + str(current_time_to_fail)
                            + " CKPT=" + str(ckpt), 2)
                        break
                    self.time_ckpt[1] += self.ckpt_overhead_times[1]
                    self.debug_print("  SUCC: NEXT=" + str(progress)
                         + " STAT=" + str(state)
                         + " CLVL=" + str(ckpt_level)
                         + " TTFA=" + str(current_time_to_fail)
                         + " CKPT=" + str(ckpt), 2)
                    if self.L2ckpt_freq > 0:
                        ckpt_level = 2
                        if (progress + segA) % self.L2ckpt_freq == 0:
                            #self.time_ckpt[2] += self.ckpt_latency_times[2]
                            self.debug_print("  START L2CKPT SAVE", 2)
                        if progress > 0 and (progress % self.L2ckpt_freq == 0):
                            self.time_ckpt[2] += self.ckpt_latency_times[2]
                            ckpt[2] = progress - segA
                            self.debug_print("  SUCC: NEXT=" + str(progress)
                                 + " STAT=" + str(state)
                                 + " CLVL=" + str(ckpt_level)
                                 + " TTFA=" + str(current_time_to_fail)
                                 + " CKPT=" + str(ckpt), 2)
                    progress += 1
                    ckpt[1] = progress
                else: # recovery state
                    current_time_to_fail -= self.restart_times[state]
                    if current_time_to_fail < 0: # failure in recovery state
                        self.debug_print("failure in recovery state", 2)
                        self.cnt_failures[0] += 1
                        self.cnt_failures[failure_level] += 1
                        self.cnt_failures[5] += 1 # failure count of recv state
                        self.time_recovery[state] += (current_time_to_fail
                            + self.restart_times[state])
                        # register failure node
                        rtc = node_info.set_failure_node()
                        if state == 1 and not rtc:
                            self.cnt_group_failure += 1
                            state = 2
                            self.debug_print("  LEVL 1 -> 2", 2)
                        progress_bk = progress
                        progress = self.rollback_to(ckpt, state)
                        if progress is None:
                            if self.L2ckpt_freq == 0:
                                progress = progress_bk
                            else:
                                progress = 0
                        self.debug_print("  FAIL: PROG=" + str(progress)
                            + " STAT=" + str(state)
                            + " FLVL=" + str(failure_level)
                            + " TTFA=" + str(current_time_to_fail)
                            + " CKPT=" + str(ckpt), 2)
                        break
                    # no failure in recovery state
                    self.time_recovery[state] += self.restart_times[state]

                    # initialize node state
                    node_info.init_failure_nodes()
                    self.debug_print("Initialize node state.", 2)
                    if node_info.get_n_spare_nodes() < 0:
                        flag_exit = True
                        exit_msg = "no spare node"
                        break

                    state = 0
                    self.debug_print("  SUCC: NEXT=" + str(progress)
                        + " STAT=" + str(state)
                        + " FLVL=" + str(failure_level)
                        + " TTFA=" + str(current_time_to_fail)
                        + " CKPT=" + str(ckpt), 2)
            self.elapsed_time += time_to_fail
            self.debug_print("=== elapsed_time: "
                + str(self.elapsed_time) + "=========", 2)

            if (i+1) % self.check_interval == 0:
                self.time_compute_act = self.interval * progress + surplus_time
                if self.time_compute_act < 0.0:
                    self.time_compute_act = 0.0
                eff_new = self.time_compute_act / self.elapsed_time
                eff_delta = abs(eff - eff_new)
                if self.eff_print:
                    prog_print = progress
                    if prog_print < 0:
                        prog_print = 0
                    if i < self.check_interval:
                        print("%8d, %10.8f, ----------, %10d"
                            % (self.cnt_failures[0], eff_new, prog_print))
                    else:
                        print("%8d, %10.8f, %6.4e, %10d"
                            % (self.cnt_failures[0], eff_new, eff_delta, prog_print))
                eff = eff_new
                if eff_delta < self.alpha:
                    self.cnt_check_ok += 1
                    if self.cnt_check_ok >= self.n_check_ok:
                        break
                else:
                    self.cnt_check_ok = 0

        self.debug_print(
            "failure count=%d (L1=%d, L2=%d, COMP=%d, CKPT=%d, RECV=%d)" %
                (self.cnt_failures[0], self.cnt_failures[1],
                 self.cnt_failures[2], self.cnt_failures[3],
                 self.cnt_failures[4], self.cnt_failures[5])
            )
        self.debug_print(
            "Checkpoint level up (L1 -> L2) count=%d" % self.cnt_group_failure
            )
        self.debug_print("n_spare_nodes=%d" % node_info.get_n_spare_nodes())

        # Delete NodeManagement object.
        del node_info

        return eff

    def rollback_to(self, ckpt, failure_level):
        """ Roll-back to the last checkpoint. """
        for i in range(len(ckpt)):
            if i >= failure_level and not ckpt[i] == None:
                return ckpt[i]

            ckpt[i] = None
        return None

    def next_failure(self, lambds):
        """ Return next failure time and checkpoint level. """
        lambd_sum = sum(lambds)
        tf = random.expovariate(lambd_sum)
        v = random.random()
        for level in range(1, len(lambds) + 1):
            v = v - lambds[level]/lambd_sum
            if v < 0:
                return tf, level

    def optimize(self, n_steps=5000, delta=[2, 2], move_mode=0,
                 Tmax=10.0, Tmin=0.05, log_interval=100):
        """
        Execute optimization using Simulated Annealing
        and return the optimized efficiency, interval and L2ckpt_freq.

        arguments:
            n_steps -- number of iterations
            delta -- percentage of movement in interval and L2ckpt_freq
            move_mode -- how to move interval and L2ckpt_freq
                0: move parameter is selected and increments by D or -D
                1: move parameter is selected and increments
                   by randint(1,D) or -randint(1,D)
                2: both parameter is increments by randint(-D,D)
                here, D = interval(or L2ckpt_freq) * delta / 100
            Tmax -- maximum temperature in Simulated Annealing
            Tmin -- minimum temperature in Simulated Annealing
            log_interval -- interval of log output
        """
        # parameter check
        if not self.check_params():
            return None, None, None
        if not self.check_opt_params(n_steps, delta, move_mode,
                                     Tmax, Tmin, log_interval):
            return None, None, None

        self.debug_print_opt("n_steps=%d" % n_steps)
        self.debug_print_opt("delta=%d, %d" % (delta[0], delta[1]))
        self.debug_print_opt("move_mode=%d" % move_mode)
        self.debug_print_opt("Tmax=%f" % Tmax)
        self.debug_print_opt("Tmin=%f" % Tmin)
        self.debug_print_opt("log_interval=%d" % log_interval)

        print_flag_org = self.print_flag
        self.print_flag = False
        self.set_init_state()
        efficiency = self.simulate()
        efficiency_best = efficiency
        interval_best = self.interval
        L2ckpt_freq_best = self.L2ckpt_freq
        T = Tmax
        cool = pow(10, math.log10(Tmin/Tmax) / n_steps)
        cnt = 0
        if log_interval > 0:
            print("  Temp.     Efficiency  interval  L2ckpt_freq")
        while T > (Tmin+1e-12):
            if log_interval > 0:
                if cnt % log_interval == 0:
                    print("%8.3f    %6f     %5d    %3d" %
                        (T, efficiency, self.interval, self.L2ckpt_freq))
            interval_bk = self.interval
            L2ckpt_freq_bk = self.L2ckpt_freq

            self.move_state(delta, move_mode)

            new_efficiency = self.simulate()

            # skip when error occured by invalid setteings.
            if new_efficiency == 0.0:
                if efficiency > 0.0:
                    self.interval = interval_bk
                    self.L2ckpt_freq = L2ckpt_freq_bk
                    cnt += 1
                    T = T * cool
                    continue

            # save best settings
            if (new_efficiency > efficiency_best):
                efficiency_best = new_efficiency
                interval_best = self.interval
                L2ckpt_freq_best = self.L2ckpt_freq

            p = pow(math.e, -abs(new_efficiency-efficiency)*100.0 / T)
            self.debug_print_opt(
                "T=%8.3f, efficiency:best=%f, cur=%f, new=%f, p=%g"
                % (T, efficiency_best, efficiency, new_efficiency, p)
                )
            if (new_efficiency > efficiency or random.random() < p):
                efficiency = new_efficiency
            else:
                self.interval = interval_bk
                self.L2ckpt_freq = L2ckpt_freq_bk
            cnt += 1
            T = T * cool

        if log_interval > 0:
            print("%8.3f    %6f     %5d    %3d" %
                (T, efficiency, self.interval, self.L2ckpt_freq))
        self.interval = interval_best
        self.L2ckpt_freq = L2ckpt_freq_best
        efficiency = self.simulate()
        self.print_flag = print_flag_org

        return efficiency, self.interval, self.L2ckpt_freq

    def optimize_simple(self, log_flag=True):
        """
        Execute optimization and
        return the optimized efficiency, interval and L2ckpt_freq.

        arguments:
            log_flag -- flag of log output
        """
        # parameter check
        if not self.check_params():
            return None, None, None

        print_flag_org = self.print_flag
        self.print_flag = False
        #self.set_init_state()
        efficiency = 0.0
        interval_best = self.interval
        L2ckpt_freq_best = self.L2ckpt_freq
        interval_bgn = 1000
        interval_end = 36000
        interval_step = 1000
        for L2ckpt_freq in [1, 2, 5, 10, 20, 100]:
            for interval in range(interval_bgn, interval_end+1, interval_step):
                self.interval = interval
                self.L2ckpt_freq = L2ckpt_freq
                new_efficiency = self.simulate()
                if (new_efficiency > efficiency):
                    efficiency = new_efficiency
                    interval_best = self.interval
                    L2ckpt_freq_best = self.L2ckpt_freq
                self.debug_print(" %6f   %6f     %5d    %3d" %
                    (efficiency, new_efficiency, interval, L2ckpt_freq))
        if log_flag:
            print(" Efficiency  interval  L2ckpt_freq")
            print(" %6f     %5d    %3d" %
                (efficiency, interval_best, L2ckpt_freq_best))

        if interval_best > 1000:
            interval_bgn = interval_best - 1000
            interval_end = interval_best + 1000
            interval_step = 100
        else:
            interval_bgn = 100
            interval_end = 2000
            interval_step = 100
        if L2ckpt_freq_best <= 10:
            L2_freq_bgn = L2ckpt_freq_best - 2
            L2_freq_end = L2ckpt_freq_best + 2
            L2_freq_step = 1
        elif L2ckpt_freq_best == 20:
            L2_freq_bgn = 10
            L2_freq_end = 20
            L2_freq_step = 2
        else:
            L2_freq_bgn = 50
            L2_freq_end = 100
            L2_freq_step = 5
        for L2ckpt_freq in range(L2_freq_bgn, L2_freq_end+1, L2_freq_step):
            for interval in range(interval_bgn, interval_end+1, interval_step):
                self.interval = interval
                self.L2ckpt_freq = L2ckpt_freq
                new_efficiency = self.simulate()
                if (new_efficiency > efficiency):
                    efficiency = new_efficiency
                    interval_best = self.interval
                    L2ckpt_freq_best = self.L2ckpt_freq
                self.debug_print(" %6f   %6f     %5d    %3d" %
                    (efficiency, new_efficiency, interval, L2ckpt_freq))
        if log_flag:
            print(" %6f     %5d    %3d" %
                (efficiency, interval_best, L2ckpt_freq_best))

        interval_bgn = interval_best - 100
        interval_end = interval_best + 100
        interval_step = 5
        if interval_bgn < 5:
            interval_bgn = 5
        L2_freq_bgn = L2ckpt_freq_best - 1
        L2_freq_end = L2ckpt_freq_best + 1
        L2_freq_step = 1
        if L2_freq_bgn < 1:
            L2_freq_bgn = 1
        for L2ckpt_freq in range(L2_freq_bgn, L2_freq_end+1, L2_freq_step):
            for interval in range(interval_bgn, interval_end+1, interval_step):
                self.interval = interval
                self.L2ckpt_freq = L2ckpt_freq
                new_efficiency = self.simulate()
                if (new_efficiency > efficiency):
                    efficiency = new_efficiency
                    interval_best = self.interval
                    L2ckpt_freq_best = self.L2ckpt_freq
                self.debug_print(" %6f   %6f     %5d    %3d" %
                    (efficiency, new_efficiency, interval, L2ckpt_freq))
        if log_flag:
            print(" %6f     %5d    %3d" %
                (efficiency, interval_best, L2ckpt_freq_best))

        self.interval = interval_best
        self.L2ckpt_freq = L2ckpt_freq_best
        efficiency = self.simulate()
        self.print_flag = print_flag_org

        return efficiency, self.interval, self.L2ckpt_freq

    def check_opt_params(self, n_steps, delta, move_mode,
                         Tmax, Tmin, log_interval):
        """ Check optimize parameters and return result(True/False). """
        if type(n_steps) is not int:
            self.error_print("n_steps is NOT integer!")
            return False
        if n_steps < 1:
            self.error_print("invalid n_steps!")
            return False

        if type(delta) is not list:
            self.error_print("invalid delta!")
            return False
        if len(delta) < 2:
            self.error_print("invalid delta!")
            return False
        for i in range(2):
            if type(delta[i]) is not int:
                self.error_print("delta contains non-integers!")
                return False
            if delta[i] < 0:
                self.error_print("invalid delta!")
                return False

        if type(move_mode) is not int:
            self.error_print("move_mode is NOT integer!")
            return False
        if move_mode < 0 or move_mode > 2:
            self.error_print("invalid move_mode!")
            return False

        if type(Tmax) is not float:
            if type(Tmax) is not int:
                self.error_print("Tmax is non-numeric value!")
                return False
            else:
                Tmax = float(Tmax)
        if type(Tmin) is not float:
            if type(Tmim) is not int:
                self.error_print("Tmin is non-numeric value!")
                return False
            else:
                Tmin = float(Tmin)
        if Tmax <= Tmin:
            self.error_print("invalid Tmax!")
            return False
        if Tmin <= 0.0:
            self.error_print("invalid Tmin!")
            return False

        if type(log_interval) is not int:
            self.error_print("log_interval is NOT integer!")
            return False
        if log_interval < 0:
            self.error_print("invalid log_interval!")
            return False
        return True

    def set_init_state(self):
        """ Set initial interval and L2ckpt_freq for optimization. """
        efficiency_best = 0.0
        interval_best = self.interval
        L2ckpt_freq_best = self.L2ckpt_freq
        for L2_freq in [1, 2, 5, 10]:
            self.L2ckpt_freq = L2_freq
            for interval in [1000, 2500, 5000, 8000, 12000, 24000]:
                self.interval = interval
                efficiency = self.simulate()
                if efficiency > efficiency_best:
                    efficiency_best = efficiency
                    L2ckpt_freq_best = L2_freq
                    interval_best = interval
        self.interval = interval_best
        self.L2ckpt_freq = L2ckpt_freq_best
        self.debug_print_opt("initial interval = %d, initial L2ckpt_freq = %d"
            % (self.interval, self.L2ckpt_freq))

    def move_state(self, delta, mode):
        """ Change interval or/and L2chpt_freq. """
        if mode == 0:
            idx = random.randint(0, 1)
            if idx == 0:
                d = int(math.ceil(self.interval * (delta[0]/100)))
                if random.random() > 0.5:
                    self.interval += d
                else:
                    self.interval -= d
                if self.interval < 1: self.interval = 1
            else:
                d = int(math.ceil(self.L2ckpt_freq * (delta[1]/100)))
                if random.random() > 0.5:
                    self.L2ckpt_freq += d
                else:
                    self.L2ckpt_freq -= d
                if self.L2ckpt_freq < 1: self.L2ckpt_freq = 1
        elif mode == 1:
            idx = random.randint(0, 1)
            if idx == 0:
                d = int(math.ceil(self.interval * (delta[0]/100)))
                if random.random() > 0.5:
                    self.interval += random.randint(1, delta[0])
                else:
                    self.interval -= random.randint(1, delta[0])
            else:
                d = int(math.ceil(self.L2ckpt_freq * (delta[1]/100)))
                if random.random() > 0.5:
                    self.L2ckpt_freq += random.randint(1, d)
                else:
                    self.L2ckpt_freq -= random.randint(1, d)
        elif mode == 2:
            d = int(math.ceil(self.interval * (delta[0]/100)))
            self.interval += random.randint(-d, d)
            d = int(math.ceil(self.L2ckpt_freq * (delta[1]/100)))
            self.L2ckpt_freq += random.randint(-d, d)
        else:
            idx = random.randint(0, 1)
            if idx == 0:
                if random.random() > 0.5:
                    self.interval += delta[0]
                else:
                    self.interval -= delta[0]
                if self.interval < 1: self.interval = 1
            else:
                if random.random() > 0.5:
                    self.L2ckpt_freq += delta[1]
                else:
                    self.L2ckpt_freq -= delta[1]
                if self.L2ckpt_freq < 1: self.L2ckpt_freq = 1

        if self.interval < 1: self.interval = 1
        if self.L2ckpt_freq < 1: self.L2ckpt_freq = 1

        self.debug_print_opt("interval=%5d, L2ckpt_freq=%3d"
            % (self.interval, self.L2ckpt_freq))

    def note_print(self, msg):
        """ Print information message. """
        if self.print_flag:
            print("[Note] %s" % msg)

    def warning_print(self, msg):
        """ Print warning message. """
        if self.print_flag:
            print("[Warning] %s" % msg)

    def error_print(self, msg):
        """ Print error message. """
        if self.print_flag:
            print("[Error] %s" % msg)

    def debug_print(self, msg, level=1):
        """ Print message for debug. """
        if self.debug_flag:
            if level <= self.debug_level:
                print("[Debug] %s" % msg)

    def debug_print_opt(self, msg):
        """ Print message for debug in optimazation. """
        if self.debug_flag_opt:
            print("[Debug] %s" % msg)


class NodeManagement():
    """ Manage states of nodes and node groups. """
    def __init__(self, n_nodes, n_spare_nodes,
                 n_nodes_in_group, disability_tolerance):
        self.n_nodes = n_nodes
        self.n_spare_nodes = n_spare_nodes
        self.n_nodes_in_group = n_nodes_in_group
        self.disability_tolerance = disability_tolerance
        self.group = []
        self.node = []
        self.failure_nodes = []
        node_no = 0
        group_no = 0
        while node_no < self.n_nodes:
            if (self.n_nodes - node_no) < self.n_nodes_in_group:
                self.n_nodes = node_no
                break
            self.group.append({})
            self.group[group_no]["n_broken"] = 0
            #self.group[group_no]["member"] = []
            for i in range(self.n_nodes_in_group):
                #self.group[group_no]["member"].append(node_no)
                self.node.append({})
                self.node[node_no]["state"] = True
                self.node[node_no]["group"] = group_no
                node_no += 1
            group_no += 1

    def get_n_nodes(self):
        return self.n_nodes

    def get_n_spare_nodes(self):
        return self.n_spare_nodes

    def get_n_nodes_in_group(self):
        return self.n_nodes_in_group

    def get_disability_tolerance(self):
        return self.disability_tolerance

    def init_failure_nodes(self):
        """ replace all broken nodes and initialize states """
        for i in range(len(self.group)):
            self.group[i]["n_broken"] = 0
        for i in range(len(self.failure_nodes)):
            node_no = self.failure_nodes[i]
            self.node[node_no]["state"] = True
        self.n_spare_nodes -= len(self.failure_nodes)
        self.failure_nodes = []

    def set_failure_node(self):
        if self.disability_tolerance == self.n_nodes_in_group:
            return True
        for i in range(1000000): # 1000000: to avoid endless loop
            failure_node_no = random.randint(0, self.n_nodes - 1)
            if self.node[failure_node_no]["state"]:
                self.node[failure_node_no]["state"] = False
                self.failure_nodes.append(failure_node_no)
                break
            if len(self.failure_nodes) >= self.n_nodes:
                break
        #group_no = int(failure_node_no / self.n_nodes_in_group)
        group_no = self.node[failure_node_no]["group"]
        self.group[group_no]["n_broken"] += 1
        if self.group[group_no]["n_broken"] > self.disability_tolerance:
            return False
        return True


if __name__  == "__main__":
    main()