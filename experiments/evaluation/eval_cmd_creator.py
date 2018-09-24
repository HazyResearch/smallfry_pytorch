import argh
import pathlib
import glob
import os
import evaluate

'''
CORE LAUNCH METHODS: launch and qsub_launch
'''
#globally stores a launch
log = []
#evaluate cmd creator launch path
launch_path = str(pathlib.PurePath(evaluate.get_launch_path(), 'eval'))
qsub_log_path = str(pathlib.PurePath(evaluate.get_qsub_log_path(), 'eval'))

def launch(params):
    s = 'python3.6 /proj/smallfry/git/smallfry/experiments/evaluation/evaluate.py eval-embeddings %s  %s %s --seed %s' % params
    return s

def qsub_launch(params):
    return 'qsub -V -b y -wd %s %s ' % (qsub_log_path, launch(params))

'''
HELPER METHODS FOR COMMON SWEEP STYLES (and logging)
'''
def log_launch(name):
    log_launch_path = str(pathlib.PurePath( launch_path, name ))
    with open(log_launch_path, 'w+') as llp:
        llp.write('\n'.join(log))

def forall_in_rungroup(evaltype, rungroup, seeds, params=None, qsub=True):
    '''a subroutine for complete 'sweeps' of params'''
    l = qsub_launch if qsub else launch
    for seed in seeds:
        rungroup_qry = evaluate.get_base_outputdir()+'/*'
        rungroup_found = False
        for rg in glob.glob(rungroup_qry):
            if os.path.basename(rg) == rungroup:    
            #speical params not support yet TODO
                rungroup_found = True
                rungroup_wildcard = rg +'/*'
                for emb in glob.glob(rungroup_wildcard):
                    cmd = l((emb,
                            evaltype,
                            '/',
                            seed))
                    log.append(cmd)
        assert rungroup_found, "rungroup requested in eval cmd creator not found"

def forall_in_rungroup_with_seed(evaltype, rungroup, seeds, params=None, qsub=True):
    '''a subroutine for complete 'sweeps' of params'''
    l = qsub_launch if qsub else launch
    for seed in seeds:
        rungroup_qry = evaluate.get_base_outputdir()+'/*'
        rungroup_found = False
        for rg in glob.glob(rungroup_qry):
            if os.path.basename(rg) == rungroup:    
            #speical params not support yet TODO
                rungroup_found = True
                rungroup_wildcard = rg +'/*'
                for emb in glob.glob(rungroup_wildcard):
                    if not( 'seed=%s' % seed in emb): continue #only match up correct seeds
                    cmd = l((emb,
                            evaltype,
                            '/',
                            seed))
                    log.append(cmd)
        assert rungroup_found, "rungroup requested in eval cmd creator not found"

'''
LAUNCH ROUTINES BELOW THIS LINE =========================
'''
def launch_dca_fronorm_eval(name):
    #date of code Sept 21, 2018
    rungroups = ['2018-09-21-experiment1-dca-hp-tune','2018-09-20-experiment1-dca-hp-tune']
    evaltypes = ['sythetics']
    global qsub_log_path
    for rungroup in rungroups:
        qsub_log_path = evaluate.prep_qsub_log_dir(qsub_log_path, name, rungroup)
        params = dict()
        for evaltype in evaltypes:
            seeds = [20]
            forall_in_rungroup(evaltype, rungroup, seeds)
        log_launch(evaluate.get_log_name(name, rungroup))

def launch_experiment1_dca_fronorm_eval(name):
    #date of code Sept 22, 2018
    rungroup = '2018-09-20-experiment1-dca-hp-tune'
    evaltypes = ['synthetics']
    global qsub_log_path
    qsub_log_path = evaluate.prep_qsub_log_dir(qsub_log_path, name, rungroup)
    params = dict()
    for evaltype in evaltypes:
        seeds = [20]
        forall_in_rungroup(evaltype, rungroup, seeds)
    log_launch(evaluate.get_log_name(name, rungroup)) 

def launch_experiment1_final_testrun(name):
    #date of code Sept 17, 2018
    rungroup = '2018-09-20-experiment1-final-testrun'
    evaltypes = ['synthetics','intrinsics','QA']
    global qsub_log_path
    qsub_log_path = evaluate.prep_qsub_log_dir(qsub_log_path, name, rungroup)
    params = dict()
    for evaltype in evaltypes:
        seeds = [20]
        forall_in_rungroup(evaltype, rungroup, seeds)
    log_launch(evaluate.get_log_name(name, rungroup))

def launch_testrun4(name):
    #date of code Sept 17, 2018
    rungroup = '2018-09-18-test-run-4'
    evaltypes = ['synthetics','intrinsics','QA']
    global qsub_log_path
    qsub_log_path = evaluate.prep_qsub_log_dir(qsub_log_path, name, rungroup)
    params = dict()
    for evaltype in evaltypes:
        seeds = [20]
        forall_in_rungroup(evaltype, rungroup, seeds)
    log_launch(evaluate.get_log_name(name, rungroup))

def launch_debug_dca_loss(name):
    #date of code Sept 17, 2018
    rungroup = '2018-09-18-debug-dca-loss'
    evaltypes = ['synthetics']
    global qsub_log_path
    qsub_log_path = evaluate.prep_qsub_log_dir(qsub_log_path, name, rungroup)
    params = dict()
    for evaltype in evaltypes:
        seeds = [20]
        forall_in_rungroup(evaltype, rungroup, seeds)
    log_launch(evaluate.get_log_name(name, rungroup))

def launch3_testrun(name):
    #date of code Sept 17, 2018
    rungroup = '2018-09-17-official-test-run-lite-2'
    evaltypes = ['QA']
    global qsub_log_path
    qsub_log_path = evaluate.prep_qsub_log_dir(qsub_log_path, name, rungroup)
    params = dict()
    for evaltype in evaltypes:
        seeds = [20]
        forall_in_rungroup(evaltype, rungroup, seeds, qsub=False)
    log_launch(evaluate.get_log_name(name, rungroup))

def launch2_official_qsub(name):
    #date of code Sept 17, 2018
    rungroup = '2018-09-17-official-test-run-lite-2'
    evaltypes = ['intrinsics','synthetics','QA']
    global qsub_log_path
    qsub_log_path = evaluate.prep_qsub_log_dir(qsub_log_path, name, rungroup)
    params = dict()
    for evaltype in evaltypes:
        seeds = [20]
        forall_in_rungroup(evaltype, rungroup, seeds)
    log_launch(evaluate.get_log_name(name, rungroup))

def launch1_demo_qsub(name):
    #date of code Sept 17, 2018
    rungroup = '2018-09-16-sweep-6297-test-2'
    evaltypes = ['QA']
    params = dict()
    for evaltype in evaltypes:
        seeds = [6297]
        forall_in_rungroup(evaltype, rungroup, seeds)
    log_launch(evaluate.get_log_name(name, rungroup))

def launch1_demo(name):
    #date of code Sept 16, 2018
    rungroup = '2018-09-16-sweep-6297-test-2'
    evaltypes = ['QA']
    params = dict()
    for evaltype in evaltypes:
        seeds = [6297]
        forall_in_rungroup(evaltype, rungroup, seeds, qsub=False)
    log_launch(get_log_name(name, rungroup))


#IMPORTANT!! this line determines which cmd will be run
cmd = [launch_experiment1_dca_fronorm_eval]

parser = argh.ArghParser()
parser.add_commands(cmd)

if __name__ == '__main__':
    parser.dispatch()