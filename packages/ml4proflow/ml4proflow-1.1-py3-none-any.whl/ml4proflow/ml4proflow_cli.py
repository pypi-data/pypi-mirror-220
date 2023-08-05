#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import sys
from typing import Any
from time import perf_counter, time
from ml4proflow import modules


sys.setrecursionlimit(20000)


def load_json(f: str) -> dict[Any, Any]:
    with open(f) as jf:
        return json.load(jf)


def run_n_times(dfg: modules.DataFlowGraph, runs: int) -> None:
    for i in range(runs):
        dfg.execute_once()


def main(arguments: list[str] = sys.argv[1:]) -> None:
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--record-times', action='store_true')
    parser.add_argument('--graph-desc')
    parser.add_argument('--profile-json-parse')
    parser.add_argument('--profile-dfg-create', action='store_true')
    parser.add_argument('--profile-process-n-times', type=int)
    parser.add_argument('--process-until-exception')
    parser.add_argument('--process-n-times', type=int)
    parser.add_argument('--process-n-seconds', type=int)
    parser.add_argument('--abort-on-more-threads', action='store_true')
    args = parser.parse_args(arguments)
    if args.record_times:
        print("python_init_done:%s:%s" % (time(), perf_counter()))
    if args.profile_json_parse:
        import cProfile
        cProfile.run('load_json("%s")' % args.profile_json_parse)
    if args.graph_desc:
        dfg_desc = load_json(args.graph_desc)
    else:
        print('TODO')
        return
    if args.record_times:
        print("python_json_done:%s:%s" % (time(), perf_counter()))
    if args.profile_dfg_create:
        import cProfile
        cmd = 'modules.DataFlowGraph(modules.DataFlowManager(), dfg_desc)'
        cProfile.runctx(cmd, globals(), locals())
    dfm = modules.DataFlowManager()
    dfg = modules.DataFlowGraph(dfm, dfg_desc)
    if args.abort_on_more_threads:
        import multiprocessing
        if len(multiprocessing.active_children()) > multiprocessing.cpu_count():
            print('python_skip:%s:%s' % (len(multiprocessing.active_children()),
                                         multiprocessing.cpu_count()))
    if args.record_times:
        print("python_dfg_create_done:%s:%s" % (time(), perf_counter()))
    if args.profile_process_n_times:
        import cProfile
        cProfile.runctx('run_n_times(dfg, args.profile_process_n_times)',
                        globals(), locals())
    if args.process_n_times:
        run_n_times(dfg, args.process_n_times)
    if args.process_n_seconds:
        start_time = time()
        run_counter = 0
        while time()-start_time <= args.process_n_seconds:
            dfg.execute_once()
            run_counter += 1
    if args.record_times:
        print("python_process_done:%s:%s" % (time(), perf_counter()))
    dfg.on_shutdowning()
    if args.record_times:
        print("python_want_shutdown_done:%s:%s" % (time(), perf_counter()))
    dfg.on_shutdowned()
    if args.record_times:
        print("python_shutdown_done:%s:%s" % (time(), perf_counter()))
    if args.process_n_seconds:
        print("python_runs:%s" % run_counter)


if __name__ == '__main__':
    main(sys.argv[1:])
