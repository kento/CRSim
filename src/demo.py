from checkpoint_restart_simulator import *

def main():

    mode = 0
    settings = 0

    if settings == 0:
        interval = 100
        L2ckpt_freq = 1
        L1ckpt_overhead = 10
        L2ckpt_latency = 100
        ckptRestartTimes = [10, 100]
        N = 1000
        SN = 1000000
        G = 4
        #G = 1
        g = 2
        #g = 2
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
    else:
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
    n_check_ok = 2

    # simulation
    if mode == 0:
        #CheckpointRestartSimulator.debug_flag = True
        print("*** Simulation Start ***")
        rtn_vals = simulate_cr(interval, L2ckpt_freq, L1ckpt_overhead,
            L2ckpt_latency, ckptRestartTimes, failRates, N, SN, G, g, alpha,
            check_interval=chk_interval, n_check_ok=n_check_ok,
            efficiency_log=True)

        print("efficiency               = %f" % rtn_vals[0])
        print("actual computation time  = %f" % rtn_vals[1])
        print("total compute state time = %f" % rtn_vals[2])
        print("total L1 overhead time   = %f" % rtn_vals[3])
        print("total L1 recovery time   = %f" % rtn_vals[4])
        print("total L2 overhead time   = %f" % rtn_vals[5])
        print("total L2 recovery time   = %f" % rtn_vals[6])
        print("*** Simulation Complete ***")

    # optimization
    else:
        #CheckpointRestartSimulator.debug_flag_opt = True
        print("*** Optimization Start ***")
        rtn_vals = optimize_cr(L1ckpt_overhead, L2ckpt_latency,
            ckptRestartTimes, failRates, N, SN, G, g, alpha,
            check_interval=chk_interval, n_check_ok=n_check_ok,
            n_steps=1000, log_interval=100)

        print("\ninterval = %d  L2ckpt_freq = %d" % (rtn_vals[7], rtn_vals[8]))
        print("efficiency               = %f" % rtn_vals[0])
        print("actual computation time  = %f" % rtn_vals[1])
        print("total compute state time = %f" % rtn_vals[2])
        print("total L1 overhead time   = %f" % rtn_vals[3])
        print("total L1 recovery time   = %f" % rtn_vals[4])
        print("total L2 overhead time   = %f" % rtn_vals[5])
        print("total L2 recovery time   = %f" % rtn_vals[6])
        print("*** Optimization Complete ***")

if __name__  == "__main__":
    main()