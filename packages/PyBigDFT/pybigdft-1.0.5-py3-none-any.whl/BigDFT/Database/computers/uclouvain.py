
import math, yaml, logging
from BigDFT.RemoteRunnerUtils import CallableAttrDict
from BigDFT.URL import URL

# create and link logger
module_logger = logging.getLogger(__name__)
# some long string that won't be accidentally entered
filler = 'mannscript_defaultvalue'
mann_spec = f"""
name: {filler}
time: {filler}
mpi: {filler}
nodes: {filler}
omp: {filler}
# project: {filler}
memory: 3500
partition: Def
sourcepath: {filler}
modules:
   - intel/2021b
   - python/anaconda3
submitter: sbatch
max_per_node: 128
omp_thread_limit: -1  # set to OMP threading limit
extra_lines: []
mpi_command_line: ''
check_resources: False
"""


def safe_divide(a, b):
    """
    always-fit division. Rounds up after division, always returns >= 1
    """
    r = math.ceil(a / b)
    return max(r, 1)


class ScriptPrologue(CallableAttrDict):
    def __str__(self):

        if self.nodes == filler:
            nodes = safe_divide(self.mpi, self.max_per_node)
        else:
            nodes = self.nodes
        # omp = self.omp
        self.tpn = safe_divide(self.mpi, nodes)

        lims = {'standard': (4, None),
                'mono': (1, 1),
                'short': (32, 512),
                'csp': (32, 1024)}

        # TODO check actual values of limits
        if self.partition in lims and self.check_resources:
            nodemin = lims[self.partition][0]
            nodemax = lims[self.partition][1]

            processes = nodes * self.mpi

            if processes < nodemin:
                raise ValueError(f'{processes} processes is too low for '
                                 f'queue {self.partition} (min {nodemin})')

            if nodemax and processes > nodemax:
                raise ValueError(f'{processes} processes is too high for '
                                 f'queue {self.partition} (max {nodemax})')

        shebang = "#!/bin/bash"
        pragma = "#SBATCH"
        options = [('--job-name=', self.name),
                   ('--time=', self.time),
                   ('', ''),
                   ('--ntasks=', self.mpi),
                   ('--ntasks-per-node=', self.tpn),
                   ('--nodes=', self.nodes),
                   ('--cpus-per-task=', self.omp),
                   ('--mem-per-cpu=', self.memory),
                   ('--output=',f'{self.name}-stdout'),]
        prologue = '\n'.join([shebang] +
                             [f'{pragma} {opt}{str(val)}'
                              for opt,val in options])
        return prologue + '\n'


class MannScript(CallableAttrDict):

    def __str__(self):
        prologue = ScriptPrologue(self)

        # these parameters can be ignored, and filled automatically
        # for validation
        self.can_be_default = ['nodes',
                               'sourcepath']

        if self.sourcepath == filler:
            sourcepath = '/home/ucl/modl/$USER/files/bigdft-suite/build/bigdft/bigdftvars.sh'
        else:
            sourcepath = self.sourcepath

        text = '\n \n'.join(['module load ' + str(mod) for mod in self.modules])
        text += f'\n\nexport OMP_NUM_THREADS={self.omp}'

        text += f"""
\nsource {sourcepath}
export BIGDFT_MPIRUN='mpirun'
export FUTILE_PROFILING_DEPTH=0
"""
        for line in self.extra_lines:
            text += line
        return '\n'.join([prologue(), text])

    @property
    def missing(self):
        """
        return non-updated arguments
        """
        self.__str__()
        missing = [k for k, v in self.items() if v == str(filler) and k not in self.can_be_default]
        module_logger.debug(f'missing arguments: {missing}')
        return missing

    @property
    def valid(self):
        valid = len(self.missing) == 0
        module_logger.debug(f'checking if script is valid: {valid}')
        return valid


submission_script = MannScript(yaml.load(mann_spec, Loader=yaml.Loader))
url = URL()
