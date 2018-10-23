import ast
from rbfopt import RbfoptSettings


def register_problem_options(parser):
    algset = parser.add_argument_group('Problem settings')
    algset.add_argument('--objective_n', '--objectiveN', action='store', dest='objective_n',
                        metavar='OBJECTIVE_N', type=int, default=1, help='number of objectives')
    algset.add_argument('--param_list', '--param', required=True, action='store', dest='param_list',
                        metavar='PARAM_LIST', type=str, help='list of parameters for initialization')


def register_rbfopt_options(parser):
    """Add options to the command line parser.

    Register all the options for the optimization algorithm.

    Parameters
    ----------
    parser : argparse.ArgumentParser
        The parser.

    See also
    --------   
    :class:`rbfopt_settings.RbfoptSettings` for a detailed description of
    all the command line options.
    """
    # Algorithmic settings
    algset = parser.add_argument_group('Algorithmic settings')
    # Get default values from here
    default = RbfoptSettings()
    docstring = default.__doc__
    param_docstring = docstring[docstring.find('Parameters'):
                                docstring.find('Attributes')].split(' : ')
    param_name = [val.split(' ')[-1].strip() for val in param_docstring[:-1]]
    param_type = [val.split('\n')[0].strip() for val in param_docstring[1:]]
    param_help = [' '.join(line.strip() for line in val.split('\n')[1:-2])
                  for val in param_docstring[1:]]
    # We extract the default from the docstring in case it is
    # necessary, but we use the actual default from the object above.
    # param_default = [val.split(' ')[-1].rstrip('.').strip('\'') for val in param_help]
    for i in range(len(param_name)):
        if (param_type[i] == 'float'):
            type_fun = float
        elif (param_type[i] == 'int'):
            type_fun = int
        elif (param_type[i] == 'bool'):
            type_fun = ast.literal_eval
        else:
            type_fun = str
        algset.add_argument('--' + param_name[i], action='store',
                            dest=param_name[i],
                            type=type_fun,
                            help=param_help[i],
                            default=getattr(default, param_name[i]))
    algset.add_argument('--addNodes', action='store_true',
                        help='add the points from the addPointsFile and addValuesFile to the model')
    algset.add_argument('--path', action='store', type=str,
                        help='path for files, default is script directory')
    algset.add_argument('--addPointsFile', action='store',
                        type=str, help='file name for points to add to the model')
    algset.add_argument('--addValuesFile', action='store', type=str,
                        help='file name for objective values to add to the model')
    algset.add_argument('--log', '-o', action='store', metavar='LOG_FILE_NAME',
                        type=str, dest='output_stream', help='Name of log file for output redirection')