from checkpoint_restart_simulator import *

def main():

    mode = 2

    # test of simulate_cr function
    if mode == 0:
        test_sim()
        test_sim_error()

    # test of optimize_cr function
    elif mode == 1:
        test_opt()
        test_opt_error()

    # for graph (sweeping interval and L2ckpt_freq)
    #   test.py > graph.csv
    #   create_graph.py graph.csv
    elif mode == 2:
        settings = 0
        if settings == 0:
            interval = 100
            L2ckpt_freq = 1
            L1ckpt_overhead = 10
            L2ckpt_latency = 100
            ckptRestartTimes = [10, 100]
            N = 1000
            #N = 8
            SN = 1000000
            G = 4
            #G = 1
            g = 1
            #g = 2
            #g = 3
        elif settings == 1:
            interval = 2000
            L2ckpt_freq = 4
            L1ckpt_overhead = 200
            L2ckpt_latency = 6000
            ckptRestartTimes = [200, 6000]
            N = 1000
            SN = 1000000
            G = 4
            g = 1
        else: # base settings for test
            interval = 3000
            L2ckpt_freq = 20
            L1ckpt_overhead = 100
            L2ckpt_latency = 2000
            ckptRestartTimes = [100, 2000]
            N = 1000
            SN = 1000000
            G = 4
            g = 1

        #failRates = [1e-04, 1e-05]
        failRates = [1e-05, 1e-06]
        #failRates = [1e-06, 1e-07]

        alpha = 1e-4
        chk_interval = 1000
        n_check_ok = 1

        CheckpointRestartSimulator.print_flag = False
        ef = {}
        ef_max = 0.0
        p1 = 0
        p2 = 0
        header = " "
        precise = False
        if precise:
            int_list = [
                100, 200, 300, 400, 500, 600, 700, 800, 900,
                ]
            interval_end = 36000
            interval_stp = 500
            for i in range(1000, interval_end+1, interval_stp):
                int_list.append(i)
            L2_list = [1,2,3,4,5,6,7,8,9]
            for i in range(10, 20, 2):
                L2_list.append(i)
            for i in range(20, 101, 5):
                L2_list.append(i)
        else:
            int_list = [
                100, 200, 300, 400, 500, 600, 700, 800, 900,
                1000, 1500, 2000, 2500, 3000, 5000, 7500,
                10000, 15000, 20000, 25000, 30000, 36000
                ]
            L2_list = [1,2,3,4,5,6,7,8,9,10,15,20,30,40,50,60,70,80,90,100]
        for interval in int_list:
            header = header + ", %d" % interval
        print(header)
        for L2ckpt_freq in L2_list:
            #L2ckpt_freq = i + 1
            ef[L2ckpt_freq] = {}
            results = "%d" % L2ckpt_freq
            for interval in int_list:
                rtn_vals = simulate_cr(interval, L2ckpt_freq, L1ckpt_overhead,
                    L2ckpt_latency, ckptRestartTimes, failRates,
                    N, SN, G, g, alpha, chk_interval)
                results = results + ", %f" % rtn_vals[0]
                ef[L2ckpt_freq][interval] = rtn_vals[0]
                if ef[L2ckpt_freq][interval] > ef_max:
                    ef_max = ef[L2ckpt_freq][interval]
                    p1 = interval
                    p2 = L2ckpt_freq
            print(results)
        print("max_ef=%f, int=%d, L2_freq=%d" % (ef_max, p1, p2))
        CheckpointRestartSimulator.print_flag = True

def test_sim():
    params = {}
    params["interval"] = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 20, 30, 40, 50, 60, 70, 80, 90,
        100, 200, 300, 400, 500, 600, 700, 800, 900,
        1000, 2000, 3600, 7200,
        10000, 18000, 36000
        ]
    params["L2ckpt_freq"] = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 20, 30, 40, 50, 60, 70, 80, 90,
        100
        ]
    params["L1ckpt_overhead"] = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 20, 30, 40, 50, 60, 70, 80, 90,
        100, 200, 300, 400, 500, 600, 700, 800, 900,
        1000, 1800, 3600
        ]
    params["L2ckpt_latency"] = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 20, 30, 40, 50, 60, 70, 80, 90,
        100, 200, 300, 400, 500, 600, 700, 800, 900,
        1000, 2000, 3600, 7200,
        10000, 18000, 36000
        ]
    params["L1ckpt_restrat"] = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 20, 30, 40, 50, 60, 70, 80, 90,
        100, 200, 300, 400, 500, 600, 700, 800, 900,
        1000, 1800, 3600
        ]
    params["L2ckpt_restrat"] = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 20, 30, 40, 50, 60, 70, 80, 90,
        100, 200, 300, 400, 500, 600, 700, 800, 900,
        1000, 2000, 3600, 7200,
        10000, 18000, 36000
        ]
    params["L1failRate"] = [
        0.0, 0.0, 1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1
        ]
    params["L2failRate"] = [
        0.0, 1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1
        ]
    params["N"] = [
        1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 20, 50,
        100, 200, 500,
        1000, 2000, 5000,
        10000, 20000, 50000,
        100000, 200000, 500000,
        1000000
        ]
    params["SN"] = [
        10, 10000, 1000000
        ]
    params["G"] = [
        1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 20, 50,
        100, 200, 500,
        1000, 2000, 5000,
        10000, 20000, 50000,
        100000, 200000, 500000,
        1000000
        ]
    params["g"] = [
        1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 20, 50,
        100, 200, 500,
        1000, 2000, 5000,
        10000, 20000, 50000,
        100000, 200000, 500000,
        1000000
        ]
    params["alpha"] = [
        1.0, 0.1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9
        ]
    params["check_interval"] = [
        1, 100, 1000
        ]
    params["n_check_ok"] = [
        1, 2, 3
        ]
    params["n_failure_max"] = [
        10, 50000
        ]
    params["efficiency_log"] = [
        False
        ]
    params["detail_flow"] = [
        0
        ]
    keys = [
        "detail_flow",
        "interval", "L2ckpt_freq", "L1ckpt_overhead", "L2ckpt_latency",
        "L1ckpt_restrat", "L2ckpt_restrat", "L1failRate", "L2failRate",
        "N", "G", "g", "alpha",
        "SN", "check_interval", "n_check_ok", "n_failure_max", "efficiency_log"
        ]

    # set debug print flag
    CheckpointRestartSimulator.debug_flag = True
    test_no_base = 10000
    for key in keys:
        CheckpointRestartSimulator.debug_level = 1
        interval = 3000
        L2ckpt_freq = 20
        L1ckpt_overhead = 100
        L2ckpt_latency = 2000
        ckptRestartTimes = [100, 2000]
        failRates = [1e-5, 1e-6]
        N = 1000
        SN = 1000000
        G = 4
        g = 1
        alpha = 1e-3
        chk_interval = 1000
        n_check_ok = 1
        n_failure_max = 500000
        efficiency_log = True
        for i in range(len(params[key])):
            print("=========================")
            if key == "interval":
                interval = params["interval"][i]
                test_no = test_no_base + i
                print("[Test%05d] interval = %s" % (test_no, str(interval)))
                if i == 0:
                    L2ckpt_freq = 0
                else:
                    L2ckpt_freq = 20
            elif key == "L2ckpt_freq":
                L2ckpt_freq = params["L2ckpt_freq"][i]
                test_no = test_no_base + i
                print("[Test%05d] L2ckpt_freq = %s" % (test_no, str(L2ckpt_freq)))
            elif key == "L1ckpt_overhead":
                L1ckpt_overhead = params["L1ckpt_overhead"][i]
                test_no = test_no_base + i
                print("[Test%05d] L1ckpt_overhead = %s" % (test_no, str(L1ckpt_overhead)))
            elif key == "L2ckpt_latency":
                L2ckpt_latency = params["L2ckpt_latency"][i]
                test_no = test_no_base + i
                print("[Test%05d] L2ckpt_latency = %s" % (test_no, str(L2ckpt_latency)))
            elif key == "L1ckpt_restrat":
                ckptRestartTimes[0] = params["L1ckpt_restrat"][i]
                test_no = test_no_base + i
                print("[Test%05d] L1ckpt_restrat = %s" % (test_no, str(ckptRestartTimes[0])))
            elif key == "L2ckpt_restrat":
                ckptRestartTimes[1] = params["L2ckpt_restrat"][i]
                test_no = test_no_base + i
                print("[Test%05d] L2ckpt_restrat = %s" % (test_no, str(ckptRestartTimes[1])))
            elif key == "L1failRate":
                failRates[0] = params["L1failRate"][i]
                test_no = test_no_base + i
                print("[Test%05d] L1failRate = %s" % (test_no, str(failRates[0])))
                if i == 0:
                    failRates[1] = 0.0
                else:
                    failRates[1] = 1e-6
            elif key == "L2failRate":
                failRates[1] = params["L2failRate"][i]
                test_no = test_no_base + i
                print("[Test%05d] L2failRate = %s" % (test_no, str(failRates[1])))
            elif key == "N":
                N = params["N"][i]
                test_no = test_no_base + i
                print("[Test%05d] N = %s" % (test_no, str(N)))
                if N < 4:
                    G = N
                else:
                    G = 4
            elif key == "SN":
                SN = params["SN"][i]
                test_no = test_no_base + i
                print("[Test%05d] SN = %s" % (test_no, str(SN)))
            elif key == "G":
                N = 1000000
                G = params["G"][i]
                test_no = test_no_base + i
                print("[Test%05d] G = %s" % (test_no, str(G)))
            elif key == "g":
                g = params["g"][i]
                test_no = test_no_base + i
                print("[Test%05d] g = %s" % (test_no, str(g)))
                N = 1000000
                G = 1000000
                if g > 1000000:
                    G = g + 1
                    N = G
            elif key == "alpha":
                alpha = params["alpha"][i]
                test_no = test_no_base + i
                print("[Test%05d] alpha = %s" % (test_no, str(alpha)))
                n_check_ok = 2
                if i == 4:
                    chk_interval = 100
                    n_check_ok = 3
                elif i > 4:
                    chk_interval = 1
                    if i > 6:
                        n_check_ok = 1
            elif key == "check_interval":
                chk_interval = params["check_interval"][i]
                test_no = test_no_base + i
                print("[Test%05d] check_interval = %s" % (test_no, str(chk_interval)))
            elif key == "n_check_ok":
                n_check_ok = params["n_check_ok"][i]
                test_no = test_no_base + i
                print("[Test%05d] n_check_ok = %s" % (test_no, str(n_check_ok)))
            elif key == "n_failure_max":
                n_failure_max = params["n_failure_max"][i]
                test_no = test_no_base + i
                print("[Test%05d] n_failure_max = %s" % (test_no, str(n_failure_max)))
            elif key == "efficiency_log":
                efficiency_log = params["efficiency_log"][i]
                test_no = test_no_base + i
                print("[Test%05d] efficiency_log = %s" % (test_no, str(efficiency_log)))
            elif key == "detail_flow":
                test_no = test_no_base + i
                print("[Test%05d] detail flow check" % test_no)
                CheckpointRestartSimulator.debug_level = 2
                L1ckpt_overhead = 500
                ckptRestartTimes[0] = 500
                failRates = [1e-4, 1e-5]
                N = 8
                chk_interval = 20

            rtn_vals = simulate_cr(interval, L2ckpt_freq, L1ckpt_overhead,
                L2ckpt_latency, ckptRestartTimes, failRates, N, SN, G, g, alpha,
                check_interval=chk_interval, n_check_ok=n_check_ok,
                n_failure_max=n_failure_max, efficiency_log=efficiency_log)

            print("efficiency               = %f" % rtn_vals[0])
            print("actual computation time  = %f" % rtn_vals[1])
            print("total compute state time = %f" % rtn_vals[2])
            print("total L1 overhead time   = %f" % rtn_vals[3])
            print("total L1 recovery time   = %f" % rtn_vals[4])
            print("total L2 overhead time   = %f" % rtn_vals[5])
            print("total L2 recovery time   = %f" % rtn_vals[6])
            print("whole elapsed time       = %f" %
                (rtn_vals[2] + rtn_vals[3] + rtn_vals[4] + rtn_vals[6]))
        test_no_base += 100
    CheckpointRestartSimulator.debug_flag = False
    CheckpointRestartSimulator.debug_level = 1

def test_sim_error():
    params = {}
    params["interval"] = [
        -1, "a"
        ]
    params["L2ckpt_freq"] = [
        -1, "a", 1, 1
        ]
    params["L1ckpt_overhead"] = [
        -1, "a"
        ]
    params["L2ckpt_latency"] = [
        -1, "a"
        ]
    params["L1ckpt_restrat"] = [
        -1, "a"
        ]
    params["L2ckpt_restrat"] = [
        -1, "a", 100, 100
        ]
    params["L1failRate"] = [
        -1, "a"
        ]
    params["L2failRate"] = [
        -1, "a", 1e-5, 1e-5
        ]
    params["N"] = [
        0, "a"
        ]
    params["SN"] = [
        -1, "a"
        ]
    params["G"] = [
        0, "a", 1001
        ]
    params["g"] = [
        0, "a", 5
        ]
    params["alpha"] = [
        1.01, 0.0, "a"
        ]
    params["check_interval"] = [
        0, "a"
        ]
    params["n_check_ok"] = [
        0, "a"
        ]
    params["n_failure_max"] = [
        0, "a"
        ]
    params["efficiency_log"] = [
        0
        ]
    keys = [
        "interval", "L2ckpt_freq", "L1ckpt_overhead", "L2ckpt_latency",
        "L1ckpt_restrat", "L2ckpt_restrat", "L1failRate", "L2failRate",
        "N", "G", "g", "alpha",
        "SN", "check_interval", "n_check_ok","n_failure_max", "efficiency_log"
        ]

    test_no_base = 20000
    for key in keys:
        interval = 3000
        L2ckpt_freq = 20
        L1ckpt_overhead = 100
        L2ckpt_latency = 2000
        ckptRestartTimes = [100, 2000]
        failRates = [1e-5, 1e-6]
        N = 1000
        SN = 1000000
        G = 4
        g = 1
        alpha = 1e-3
        chk_interval = 1000
        n_check_ok = 1
        n_failure_max = 500000
        efficiency_log = False
        for i in range(len(params[key])):
            print("=========================")
            if key == "interval":
                interval = params["interval"][i]
                test_no = test_no_base + i
                print("[Test%05d] interval = %s" % (test_no, str(interval)))
            elif key == "L2ckpt_freq":
                if i == 2:
                    interval = 200
                if i == 3:
                    interval = 0
                L2ckpt_freq = params["L2ckpt_freq"][i]
                test_no = test_no_base + i
                print("[Test%05d] L2ckpt_freq = %s" % (test_no, str(L2ckpt_freq)))
            elif key == "L1ckpt_overhead":
                L1ckpt_overhead = params["L1ckpt_overhead"][i]
                test_no = test_no_base + i
                print("[Test%05d] L1ckpt_overhead = %s" % (test_no, str(L1ckpt_overhead)))
            elif key == "L2ckpt_latency":
                L2ckpt_latency = params["L2ckpt_latency"][i]
                test_no = test_no_base + i
                print("[Test%05d] L2ckpt_latency = %s" % (test_no, str(L2ckpt_latency)))
            elif key == "L1ckpt_restrat":
                ckptRestartTimes[0] = params["L1ckpt_restrat"][i]
                test_no = test_no_base + i
                print("[Test%05d] L1ckpt_restrat = %s" % (test_no, str(ckptRestartTimes[0])))
            elif key == "L2ckpt_restrat":
                test_no = test_no_base + i
                if i == 2:
                    ckptRestartTimes = [100]
                elif i == 3:
                    ckptRestartTimes = 100
                else:
                    ckptRestartTimes[1] = params["L2ckpt_restrat"][i]
                print("[Test%05d] L2ckpt_restrat = %s" % (test_no, str(params["L2ckpt_restrat"][i])))
            elif key == "L1failRate":
                failRates[0] = params["L1failRate"][i]
                test_no = test_no_base + i
                print("[Test%05d] L1failRate = %s" % (test_no, str(failRates[0])))
            elif key == "L2failRate":
                test_no = test_no_base + i
                if i == 2:
                    failRates = [1e-5]
                elif i == 3:
                    failRates = 1e-5
                else:
                    failRates[1] = params["L2failRate"][i]
                print("[Test%05d] L2failRate = %s" % (test_no, str(params["L2failRate"][i])))
            elif key == "N":
                N = params["N"][i]
                test_no = test_no_base + i
                print("[Test%05d] N = %s" % (test_no, str(N)))
            elif key == "SN":
                SN = params["SN"][i]
                test_no = test_no_base + i
                print("[Test%05d] SN = %s" % (test_no, str(SN)))
            elif key == "G":
                G = params["G"][i]
                test_no = test_no_base + i
                print("[Test%05d] G = %s" % (test_no, str(G)))
            elif key == "g":
                g = params["g"][i]
                test_no = test_no_base + i
                print("[Test%05d] g = %s" % (test_no, str(g)))
            elif key == "alpha":
                alpha = params["alpha"][i]
                test_no = test_no_base + i
                print("[Test%05d] alpha = %s" % (test_no, str(alpha)))
            elif key == "check_interval":
                chk_interval = params["check_interval"][i]
                test_no = test_no_base + i
                print("[Test%05d] check_interval = %s" % (test_no, str(chk_interval)))
            elif key == "check_interval":
                n_check_ok = params["n_check_ok"][i]
                test_no = test_no_base + i
                print("[Test%05d] n_check_ok = %s" % (test_no, str(n_check_ok)))
            elif key == "n_check_ok":
                n_check_ok = params["n_check_ok"][i]
                test_no = test_no_base + i
                print("[Test%05d] n_check_ok = %s" % (test_no, str(n_check_ok)))
            elif key == "n_failure_max":
                n_failure_max = params["n_failure_max"][i]
                test_no = test_no_base + i
                print("[Test%05d] n_failure_max = %s" % (test_no, str(n_failure_max)))
            elif key == "efficiency_log":
                efficiency_log = params["efficiency_log"][i]
                test_no = test_no_base + i
                print("[Test%05d] efficiency_log = %s" % (test_no, str(efficiency_log)))

            rtn_vals = simulate_cr(interval, L2ckpt_freq, L1ckpt_overhead,
                L2ckpt_latency, ckptRestartTimes, failRates, N, SN, G, g, alpha,
                check_interval=chk_interval, n_check_ok=n_check_ok,
                n_failure_max=n_failure_max, efficiency_log=efficiency_log)

            print("efficiency               = %f" % rtn_vals[0])
            print("actual computation time  = %f" % rtn_vals[1])
            print("total compute state time = %f" % rtn_vals[2])
            print("total L1 overhead time   = %f" % rtn_vals[3])
            print("total L1 recovery time   = %f" % rtn_vals[4])
            print("total L2 overhead time   = %f" % rtn_vals[5])
            print("total L2 recovery time   = %f" % rtn_vals[6])
            print("whole elapsed time       = %f" %
                (rtn_vals[2] + rtn_vals[3] + rtn_vals[4] + rtn_vals[6]))
        test_no_base += 10


def test_opt():
    params = {}
    params["L1ckpt_overhead"] = [
        0, 100, 3600
        ]
    params["L2ckpt_latency"] = [
        0, 1000, 36000
        ]
    params["L1ckpt_restrat"] = [
        0, 100, 3600
        ]
    params["L2ckpt_restrat"] = [
        0, 1000, 36000
        ]
    params["L1failRate"] = [
        0.0, 1e-10, 1e-6
        ]
    params["L2failRate"] = [
        0.0, 1e-10, 1e-6
        ]
    params["N"] = [
        1, 1000, 1000000
        ]
    params["SN"] = [
        10000, 1000000
        ]
    params["G"] = [
        1, 1000, 1000000
       ]
    params["g"] = [
        1, 1000, 1000000
       ]
    params["alpha"] = [
        1e-2, 1e-5, 1e-7
        ]
    params["n_steps"] = [
        100, 5000
        ]
    params["log_interval"] = [
        0, 25
        ]
    keys = [
        "L1ckpt_overhead", "L2ckpt_latency",
        "L1ckpt_restrat", "L2ckpt_restrat", "L1failRate", "L2failRate",
        "N", "SN", "G", "g", "alpha", "n_steps", "log_interval"
        ]

    test_no_base = 30000
    for key in keys:
        CheckpointRestartSimulator.debug_flag_opt = True # set debug print flag
        L1ckpt_overhead = 100
        L2ckpt_latency = 2000
        ckptRestartTimes = [100, 2000]
        failRates = [1e-05, 1e-06]
        N = 1000
        SN = 1000000
        G = 4
        g = 1
        alpha = 1e-3
        check_interval = 1000
        n_check_ok = 1
        n_steps = 250
        log_interval = 50
        for i in range(len(params[key])):
            print("=========================")
            if key == "L1ckpt_overhead":
                L1ckpt_overhead = params["L1ckpt_overhead"][i]
                test_no = test_no_base + i
                print("[Test%05d] L1ckpt_overhead = %s" % (test_no, str(L1ckpt_overhead)))
            elif key == "L2ckpt_latency":
                L2ckpt_latency = params["L2ckpt_latency"][i]
                test_no = test_no_base + i
                print("[Test%05d] L2ckpt_latency = %s" % (test_no, str(L2ckpt_latency)))
            elif key == "L1ckpt_restrat":
                ckptRestartTimes[0] = params["L1ckpt_restrat"][i]
                test_no = test_no_base + i
                print("[Test%05d] L1ckpt_restrat = %s" % (test_no, str(ckptRestartTimes[0])))
            elif key == "L2ckpt_restrat":
                ckptRestartTimes[1] = params["L2ckpt_restrat"][i]
                test_no = test_no_base + i
                print("[Test%05d] L2ckpt_restrat = %s" % (test_no, str(ckptRestartTimes[1])))
            elif key == "L1failRate":
                failRates[0] = params["L1failRate"][i]
                test_no = test_no_base + i
                print("[Test%05d] L1failRate = %s" % (test_no, str(failRates[0])))
            elif key == "L2failRate":
                failRates[1] = params["L2failRate"][i]
                test_no = test_no_base + i
                print("[Test%05d] L2failRate = %s" % (test_no, str(failRates[1])))
            elif key == "N":
                N = params["N"][i]
                test_no = test_no_base + i
                print("[Test%05d] N = %s" % (test_no, str(N)))
                if N < 4:
                    G = N
                else:
                    G = 4
            elif key == "SN":
                SN = params["SN"][i]
                test_no = test_no_base + i
                print("[Test%05d] SN = %s" % (test_no, str(SN)))
            elif key == "G":
                N = 1000000
                G = params["G"][i]
                test_no = test_no_base + i
                print("[Test%05d] G = %s" % (test_no, str(G)))
            elif key == "g":
                g = params["g"][i]
                test_no = test_no_base + i
                print("[Test%05d] g = %s" % (test_no, str(g)))
                N = 1000000
                G = 1000000
                if g > 1000000:
                    G = g + 1
                    N = G
            elif key == "alpha":
                alpha = params["alpha"][i]
                test_no = test_no_base + i
                print("[Test%05d] alpha = %s" % (test_no, str(alpha)))
                n_check_ok = 2
                if i > 0:
                    n_steps = 50
                    check_interval = 1
                    n_check_ok = 1
            elif key == "n_steps":
                if i == 1:
                    CheckpointRestartSimulator.debug_flag_opt = False
                n_steps = params["n_steps"][i]
                test_no = test_no_base + i
                print("[Test%05d] n_steps = %s" % (test_no, str(n_steps)))
            elif key == "log_interval":
                log_interval = params["log_interval"][i]
                test_no = test_no_base + i
                print("[Test%05d] log_interval = %s" % (test_no, str(log_interval)))

            rtn_vals = optimize_cr(L1ckpt_overhead,
                L2ckpt_latency, ckptRestartTimes, failRates, N, SN, G, g, alpha,
                check_interval, n_check_ok, n_steps=n_steps,
                log_interval=log_interval)

            print("interval = %d  L2ckpt_freq = %d" % (rtn_vals[7], rtn_vals[8]))
            print("efficiency               = %f" % rtn_vals[0])
            print("actual computation time  = %f" % rtn_vals[1])
            print("total compute state time = %f" % rtn_vals[2])
            print("total L1 overhead time   = %f" % rtn_vals[3])
            print("total L1 recovery time   = %f" % rtn_vals[4])
            print("total L2 overhead time   = %f" % rtn_vals[5])
            print("total L2 recovery time   = %f" % rtn_vals[6])
            print("whole elapsed time       = %f" %
                (rtn_vals[2] + rtn_vals[3] + rtn_vals[4] + rtn_vals[6]))
        test_no_base += 10
    CheckpointRestartSimulator.debug_flag_opt = False

def test_opt_error():
    params = {}
    params["L1ckpt_overhead"] = [
        -1, "a"
        ]
    params["L2ckpt_latency"] = [
        -1, "a"
        ]
    params["L1ckpt_restrat"] = [
        -1, "a"
        ]
    params["L2ckpt_restrat"] = [
        -1, "a", 100, 100
        ]
    params["L1failRate"] = [
        -1, "a"
        ]
    params["L2failRate"] = [
        -1, "a", 1e-5, 1e-5
        ]
    params["N"] = [
        0, "a"
        ]
    params["SN"] = [
        -1, "a"
        ]
    params["G"] = [
        0, "a", 1001
        ]
    params["g"] = [
        0, "a", 5
        ]
    params["alpha"] = [
        1.01, 0.0, "a"
        ]
    params["check_interval"] = [
        0, "a"
        ]
    params["n_check_ok"] = [
        0, "a"
        ]
    params["n_failure_max"] = [
        0, "a"
        ]
    params["n_steps"] = [
        0, "a"
        ]
    params["log_interval"] = [
        -1, "a"
        ]
    keys = [
        "L1ckpt_overhead", "L2ckpt_latency",
        "L1ckpt_restrat", "L2ckpt_restrat", "L1failRate", "L2failRate",
        "N", "SN", "G", "g", "alpha", "check_interval", "n_check_ok",
        "n_failure_max", "n_steps", "log_interval"
        ]

    test_no_base = 40000
    for key in keys:
        L1ckpt_overhead = 100
        L2ckpt_latency = 2000
        ckptRestartTimes = [100, 2000]
        failRates = [1e-5, 1e-6]
        N = 1000
        SN = 1000000
        G = 4
        g = 1
        alpha = 1e-3
        chk_interval = 1000
        n_check_ok = 1
        n_failure_max = 500000
        efficiency_log = False
        n_steps = 1000
        log_interval = 100
        for i in range(len(params[key])):
            print("=========================")
            if key == "L1ckpt_overhead":
                L1ckpt_overhead = params["L1ckpt_overhead"][i]
                test_no = test_no_base + i
                print("[Test%05d] L1ckpt_overhead = %s" % (test_no, str(L1ckpt_overhead)))
            elif key == "L2ckpt_latency":
                L2ckpt_latency = params["L2ckpt_latency"][i]
                test_no = test_no_base + i
                print("[Test%05d] L2ckpt_latency = %s" % (test_no, str(L2ckpt_latency)))
            elif key == "L1ckpt_restrat":
                ckptRestartTimes[0] = params["L1ckpt_restrat"][i]
                test_no = test_no_base + i
                print("[Test%05d] L1ckpt_restrat = %s" % (test_no, str(ckptRestartTimes[0])))
            elif key == "L2ckpt_restrat":
                test_no = test_no_base + i
                if i == 2:
                    ckptRestartTimes = [100]
                elif i == 3:
                    ckptRestartTimes = 100
                else:
                    ckptRestartTimes[1] = params["L2ckpt_restrat"][i]
                print("[Test%05d] L2ckpt_restrat = %s" % (test_no, str(params["L2ckpt_restrat"][i])))
            elif key == "L1failRate":
                failRates[0] = params["L1failRate"][i]
                test_no = test_no_base + i
                print("[Test%05d] L1failRate = %s" % (test_no, str(failRates[0])))
            elif key == "L2failRate":
                test_no = test_no_base + i
                if i == 2:
                    failRates = [1e-5]
                elif i == 3:
                    failRates = 1e-5
                else:
                    failRates[1] = params["L2failRate"][i]
                print("[Test%05d] L2failRate = %s" % (test_no, str(params["L2failRate"][i])))
            elif key == "N":
                N = params["N"][i]
                test_no = test_no_base + i
                print("[Test%05d] N = %s" % (test_no, str(N)))
            elif key == "SN":
                SN = params["SN"][i]
                test_no = test_no_base + i
                print("[Test%05d] SN = %s" % (test_no, str(SN)))
            elif key == "G":
                G = params["G"][i]
                test_no = test_no_base + i
                print("[Test%05d] G = %s" % (test_no, str(G)))
            elif key == "g":
                g = params["g"][i]
                test_no = test_no_base + i
                print("[Test%05d] g = %s" % (test_no, str(g)))
            elif key == "alpha":
                alpha = params["alpha"][i]
                test_no = test_no_base + i
                print("[Test%05d] alpha = %s" % (test_no, str(alpha)))
            elif key == "check_interval":
                chk_interval = params["check_interval"][i]
                test_no = test_no_base + i
                print("[Test%05d] check_interval = %s" % (test_no, str(chk_interval)))
            elif key == "check_interval":
                n_check_ok = params["n_check_ok"][i]
                test_no = test_no_base + i
                print("[Test%05d] n_check_ok = %s" % (test_no, str(n_check_ok)))
            elif key == "n_check_ok":
                n_check_ok = params["n_check_ok"][i]
                test_no = test_no_base + i
                print("[Test%05d] n_check_ok = %s" % (test_no, str(n_check_ok)))
            elif key == "n_failure_max":
                n_failure_max = params["n_failure_max"][i]
                test_no = test_no_base + i
                print("[Test%05d] n_failure_max = %s" % (test_no, str(n_failure_max)))
            elif key == "n_steps":
                n_steps = params["n_steps"][i]
                test_no = test_no_base + i
                print("[Test%05d] n_steps = %s" % (test_no, str(n_steps)))
            elif key == "log_interval":
                log_interval = params["log_interval"][i]
                test_no = test_no_base + i
                print("[Test%05d] log_interval = %s" % (test_no, str(log_interval)))

            rtn_vals = optimize_cr(L1ckpt_overhead, L2ckpt_latency,
                ckptRestartTimes, failRates, N, SN, G, g, alpha,
                check_interval=chk_interval, n_check_ok=n_check_ok,
                n_failure_max=n_failure_max, n_steps=n_steps,
                log_interval=log_interval)

            print("interval = %d  L2ckpt_freq = %d" % (rtn_vals[7], rtn_vals[8]))
            print("efficiency               = %f" % rtn_vals[0])
            print("actual computation time  = %f" % rtn_vals[1])
            print("total compute state time = %f" % rtn_vals[2])
            print("total L1 overhead time   = %f" % rtn_vals[3])
            print("total L1 recovery time   = %f" % rtn_vals[4])
            print("total L2 overhead time   = %f" % rtn_vals[5])
            print("total L2 recovery time   = %f" % rtn_vals[6])
            print("whole elapsed time       = %f" %
                (rtn_vals[2] + rtn_vals[3] + rtn_vals[4] + rtn_vals[6]))
        test_no_base += 10

if __name__  == "__main__":
    main()