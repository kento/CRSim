#!/bin/python
from argparse import ArgumentParser
from checkpoint_restart_simulator import *

"""
L1ckpt_overhead(int): 0, 1, 2, 4, 8, 16, 32 [7]
L2ckpt_latency(int): 0, 2, 4, 8, 16, 32, 64 [7]
ckptRestartTimes(list): same to L1ckpt_overhead
# failRates(list): 0, 1e1, ... 1e10 [11], 0, 1e1, ... 1e10 [11] #
MTBF(L1) 0, 10, 20, 40, 60, 120, 360, 900, 1440 [9]
MTBF(L2) 0, 60, 120, 360, 720, 1440 [6]
N(int): 1024 2048 4096 8192 16384 32768 65536 131072 [8]
# SN(int): 1 16 256 1024 [4] #
G(int): (group size) 1 2 4 8  [4]
g(int): 1 2 4 [3]
alpha(float): 0.1
check_interval(int): 
n_check_ok(int): 
n_failure_max(int): 
n_steps(int): 
log_interval(int): 
"""


# ./CRSim.py opt           -o 1 -l 2 -r 1 2 -f 600 6000 -n 100 -s 5000 -g 4 -t 2 -a 0.1 -e 1000 -c 1 -m 5000  -p 250 -v 100
# ./CRSim.py sim -i 1 -q 1 -o 1 -l 2 -r 1 2 -f 600 6000 -n 100 -s 5000 -g 4 -t 2 -a 0.1 -e 1000 -c 1 -m 5000 -v

def opt(args):
    failure_rates = [1/args.mtbf[0], 1/args.mtbf[1]]
    n_groups = int(args.nodes / args.group_size)
    print (failure_rates)
#   def optimize_cr(
#                    L1ckpt_overhead, L2ckpt_latency,
#                    ckptRestartTimes, failRates, N, SN, G, g, alpha,
#                    check_interval=1, n_check_ok=1, n_failure_max=500000,
#                    n_steps=5000, log_interval=100):
    result = optimize_cr(
        args.L1_overhead,
        args.L2_latency,
        args.recovery,
        failure_rates,
        args.nodes,
#        args.nodes * 10,
        args.spares,
        n_groups,
        args.group_tolerance,
        args.alpha,
        args.check_interval,
        args.check_contiguous,
        args.failure_max,
        args.steps,
        args.verbose)
    print("eff", "c_act", "c", "l1c", "l1r", "l2c", "l2r", "l1int", "l2freq")
    print(result)
    return



def sim(args):
#    def simulate_cr(
#                    interval, L2ckpt_freq, L1ckpt_overhead, L2ckpt_latency,
#                    ckptRestartTimes, failRates, N, SN, G, g, alpha,
#                    check_interval=1, n_check_ok=1, n_failure_max=500000,
#                    efficiency_log=False):
    failure_rates = [1/args.mtbf[0], 1/args.mtbf[1]]
    n_groups = int(args.nodes / args.group_size)
    result = simulate_cr(
        args.L1_interval,
        args.L2_frequency,
        args.L1_overhead,
        args.L2_latency,
        args.recovery,
        failure_rates,
        args.nodes,
        args.spares,
        n_groups,
        args.group_tolerance,
        args.alpha,
        args.check_interval,
        args.check_contiguous,
        args.failure_max,
        args.verbose)
    print(result)
    return

def parser():
    #    usage = '{} opt|sim -o L1_overhead  -l L2_latency -r L1_recovery L2_recovery -f L1_failure_rates L2_failure_rates  -n nodes -s spares -g groups -t gorup_tolerance -a alpha [-i check_interval] [-c check_contiguous] [-m failure_max] [-p steps] [-v log_interval]'.format(__file__)
    #    usage = '{} <positional args> [-h|--help]'.format(__file__)
    
    common = ArgumentParser(add_help=False)
    common.add_argument('-o', '--L1_overhead', help='L1 checkpoint overhead time', type=int, required=True)
    common.add_argument('-l', '--L2_latency', help='L2 checkpoint latency time', type=int, required=True)
    common.add_argument('-r', '--recovery', nargs='+', help='L1 and L2 recovery time (-r <L1 recovery tme> <L2 recovery time>)', type=int, required=True)
#    common.add_argument('-f', '--failure_rates', nargs='+', help='L1 and L2 failure rates (-f <L1 failure rates> <L2 failure rates>)', type=float, required=True)
    common.add_argument('-f', '--mtbf', nargs='+', help='L1 and L2 MTBF (-f <L1 MTBF> <L2 MTBF>)', type=float, required=True)
    common.add_argument('-n', '--nodes', help='The number of nodes to use', type=int, required=True)
    common.add_argument('-s', '--spares', help='The number of spares nodes to use', type=int, required=True, default=math.inf)
    common.add_argument('-g', '--group_size', help='The size of L1 checkpointing group', type=int, required=True)
    common.add_argument('-t', '--group_tolerance', help='The number of failure nodes a group where the application can recover from L1 checkpoint. For example, in XOR, the application still can recovery with one failed node with in an XOR group. Please specify 1 for this option ', type=int, required=True)
    common.add_argument('-a', '--alpha', help='threshold value to finish simulation', type=float, required=True)
    ##### Optional arguments #####
    common.add_argument('-e', '--check_interval', help='Interval of checking amount of change in efficiency', type=int, required=False)
    common.add_argument('-c', '--check_contiguous', help='The number of continuous ok at checking efficiency', type=int, required=False)
    common.add_argument('-m', '--failure_max', help='Maximum failure occurrence limit', type=int, required=False)


    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_sim = subparsers.add_parser('sim', parents=[common])
    parser_sim.add_argument('-i', '--L1_interval', help='L1 checkpoint in unit time', type=int, required=True)
    parser_sim.add_argument('-q', '--L2_frequency', help='L2 frequency. For example, if this value is X, it performs an L2 checkpoint for every <X> L1 checkponts', type=int, required=True)
    parser_sim.add_argument('-v', '--verbose', help='output efficiency', action="store_true", required=False)
    parser_sim.set_defaults(handler=sim)
    
    parser_opt = subparsers.add_parser('opt', parents=[common])
    parser_opt.add_argument('-p', '--steps', help='Maximum number of iterations in optimazation', type=int, required=False)
    parser_opt.add_argument('-v', '--verbose', help='interval of log output', type=int, required=False)
    
    parser_opt.set_defaults(handler=opt)
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
    return args

def parsera():
    usage = '{} opt|sim -o L1_overhead  -l L2_latency -r L1_recovery L2_recovery -f L1_failure_rates L2_failure_rates  -n nodes -s spares -g groups -t gorup_tolerance -a alpha [-i check_interval] [-c check_contiguous] [-m failure_max] [-p steps] [-v log_interval]'\
            .format(__file__)
    parser = ArgumentParser(usage=usage, add_help=False)

    subparsers = parser.add_subparsers()

    parser_opt = subparsers.add_parser('opt', help='see `opt -h`', parents=[parser])

    parser_opt.add_argument('-o', '--L1_overhead', help='L1 checkpoint overhead time', type=int, required=True)
    parser_opt.add_argument('-l', '--L2_latency', help='L2 checkpoint latency time', type=int, required=True)
    parser_opt.add_argument('-r', '--recovery', nargs='+', help='L1 and L2 recovery time (-r <L1 recovery tme> <L2 recovery time>)', type=int, required=True)
#    parser_opt.add_argument('-f', '--failure_rates', nargs='+', help='L1 and L2 failure rates (-f <L1 failure rates> <L2 failure rates>)', type=float, required=True)
    parser_opt.add_argument('-f', '--mtbf', nargs='+', help='L1 and L2 MTBF (-f <L1 MTBF> <L2 MTBF>)', type=float, required=True)
    parser_opt.add_argument('-n', '--nodes', help='The number of nodes to use', type=int, required=True)
    parser_opt.add_argument('-s', '--spares', help='The number of spares nodes to use', type=int, required=True, default=math.inf)
    parser_opt.add_argument('-g', '--group_size', help='The size of L1 checkpointing group', type=int, required=True)
    parser_opt.add_argument('-t', '--group_tolerance', help='The number of failure nodes a group where the application can recover from L1 checkpoint. For example, in XOR, the application still can recovery with one failed node with in an XOR group. Please specify 1 for this option ', type=int, required=True)
    parser_opt.add_argument('-a', '--alpha', help='threshold value to finish simulation', type=float, required=True)
    ##### Optional arguments #####
    parser_opt.add_argument('-i', '--check_interval', help='Interval of checking amount of change in efficiency', type=int, required=False)
    parser_opt.add_argument('-c', '--check_contiguous', help='The number of continuous ok at checking efficiency', type=int, required=False)
    parser_opt.add_argument('-m', '--failure_max', help='Maximum failure occurrence limit', type=int, required=False)
    parser_opt.add_argument('-p', '--steps', help='Maximum number of iterations in optimazation', type=int, required=False)
    parser_opt.add_argument('-v', '--log_interval', help='interval of log output', type=int, required=False)
    parser_opt.set_defaults(handler=opt)
    
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
    return args

def parser_old():
    usage = '{} -o L1_overhead  -l L2_latency -r L1_recovery L2_recovery -f L1_failure_rates L2_failure_rates  -n nodes -s spares -g groups -t gorup_tolerance -a alpha [-i check_interval] [-c check_contiguous] [-m failure_max] [-p steps] [-v log_interval]'\
            .format(__file__)
    parser = ArgumentParser(usage=usage)
    parser.add_argument('-o', '--L1_overhead', help='L1 checkpoint overhead time', type=int, required=True)
    parser.add_argument('-l', '--L2_latency', help='L2 checkpoint latency time', type=int, required=True)
    parser.add_argument('-r', '--recovery', nargs='+', help='L1 and L2 recovery time (-r <L1 recovery tme> <L2 recovery time>)', type=int, required=True)
#    parser.add_argument('-f', '--failure_rates', nargs='+', help='L1 and L2 failure rates (-f <L1 failure rates> <L2 failure rates>)', type=float, required=True)
    parser.add_argument('-f', '--mtbf', nargs='+', help='L1 and L2 MTBF (-f <L1 MTBF> <L2 MTBF>)', type=float, required=True)
    parser.add_argument('-n', '--nodes', help='The number of nodes to use', type=int, required=True)
    parser.add_argument('-s', '--spares', help='The number of spares nodes to use', type=int, required=True, default=math.inf)
    parser.add_argument('-g', '--group_size', help='The size of L1 checkpointing group', type=int, required=True)
    parser.add_argument('-t', '--group_tolerance', help='The number of failure nodes a group where the application can recover from L1 checkpoint. For example, in XOR, the application still can recovery with one failed node with in an XOR group. Please specify 1 for this option ', type=int, required=True)
    parser.add_argument('-a', '--alpha', help='threshold value to finish simulation', type=float, required=True)
    ##### Optional arguments #####
    parser.add_argument('-i', '--check_interval', help='Interval of checking amount of change in efficiency', type=int, required=False)
    parser.add_argument('-c', '--check_contiguous', help='The number of continuous ok at checking efficiency', type=int, required=False)
    parser.add_argument('-m', '--failure_max', help='Maximum failure occurrence limit', type=int, required=False)
    parser.add_argument('-p', '--steps', help='Maximum number of iterations in optimazation', type=int, required=False)
    parser.add_argument('-v', '--log_interval', help='interval of log output', type=int, required=False)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parser()



