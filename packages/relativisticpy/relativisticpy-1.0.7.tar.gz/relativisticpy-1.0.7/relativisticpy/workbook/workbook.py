from cmath import exp
import re
import sympy as smp
from jsonmathpy.compute import MathJSONInterpreter
from jsonmathpy.mathify import Mathify
from relativisticpy.base_tensor.data_structure import TensorObject
from relativisticpy.base_tensor.gr_tensor import GrTensor
from relativisticpy.tensors.metric import Metric
from relativisticpy.tensors.metric import MetricWork
from relativisticpy.tensors.riemann import Riemann
from relativisticpy.tensors.derivative import Derivative


class Workbook:

    """ Cache for storing values accessed by string keys """
    def __init__(self):
        self.cache = {
            "Schwarzschild" : "[[-(1 - (G)/(r)),0,0,0],[0,1/(1 - (G)/(r)),0,0],[0,0,r**2,0],[0,0,0,r**2*sin(theta)**2]]",
            "SchildGeneral" : "[[-F(r),0,0,0],[0,1/(F(r)),0,0],[0,0,r**2,0],[0,0,0,r**2*sin(theta)**2]]",
            "AntiDeSitter" : "[[-(k**2*r**2 + 1),0,0,0],[0,1/(k**2*r**2 + 1),0,0],[0,0,r**2,0],[0,0,0,r**2*sin(theta)**2]]",
            "PolarCoordinates" : "[[-1,0,0,0],[0,1,0,0],[0,0,r**2,0],[0,0,0,r**2*sin(theta)**2]]",
            "Minkowski" : "[[-1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]",
            "WeylLewisPapapetrou": "[[-1,0,0,0],[0,1,0,0],[0,0,r**2,0],[0,0,0,r**2*sin(theta)**2]]",
            "ReissnerNordström" : "[[-(1 - (G)/(r) + (Q**2)/(r**2)),0,0,0],[0,1/(1 - (G)/(r) + (Q**2)/(r**2)),0,0],[0,0,r**2,0],[0,0,0,r**2*sin(theta)**2]]"
        }

    def get_operations_with_latest_cache(self):
        return {
                    # Build Objects
                    "BUILD_INT"         : self.build_int,
                    "BUILD_FLOAT"       : self.build_float,
                    "BUILD_TENSOR"      : self.tensor,
                    "BUILD_MINUS"       : self.minus,
                    "BUILD_VARIABLE"    : self.variable,

                    # Simple Operations
                    "ADD"               : self.add,
                    "MULTIPLY"          : self.multiply,
                    "SUBTRACTION"       : self.subtract,
                    "DIVISION"          : self.divide,
                    "POWER"             : self.power,

                    # Simpy Operations
                    "DIFFERENTIAL"      : self.differentiate,
                    "INTEGRAL"          : self.integrate,
                    "SIMPLIFY"          : self.simplify,
                    "ARRAY"             : self.array,
                    "SOLVE"             : self.solve,
                    "SERIES"            : self.series,
                    "LIMIT"             : self.limit,
                    "EXPAND"            : self.expand,
                    "EXP"               : self.exp,
                    "CONSTANT"          : self.constant,
                    "NUMERICAL"         : self.numerical,

                    # Trigonometry Functions
                    "SIN"               : self.sin,
                    "COS"               : self.cos,
                    "TAN"               : self.tan,
                    "ASIN"              : self.asin,
                    "ACOS"              : self.acos,
                    "ATAN"              : self.atan,

                    # Hyperbolic Functions 
                    "SINH"               : self.sinh,
                    "COSH"               : self.cosh,
                    "TANH"               : self.tanh,
                    "ASINH"              : self.asinh,
                    "ACOSH"              : self.acosh,
                    "ATANH"              : self.atanh,
                }

    def expr(self, expression):
        if bool(re.match('([a-zA-Z]+)(\=)', expression.replace(' ',''))):
            self.cache_equation(expression)
        else:
            ans = MathJSONInterpreter(self.get_operations_with_latest_cache()).interpret(Mathify(expression)())
            if isinstance(ans, (Metric, MetricWork, GrTensor, Riemann, TensorObject)):
                return ans.get_specified_components()
            else:
                return ans

    def cache_equation(self, equation : str):
        """ Add a equation to the cache """
        key, value = equation.replace(' ','').split('=')
        if key == 'Metric' or key == 'Basis':
            self.cache[key] = value
        else:
            self.cache[key] = self.expr(value)

    def cache_value(self, key, value):
        """ Add a value to the cache """
        self.cache[key] = self.expr(value)

    def get_cached_value(self, key):
        """ Get a value from the cache by key """
        return self.cache.get(key)

    def key_exists(self, key):
        """ Get boolean determining whether key exists """
        return bool(self.get_cached_value(key))

    def clear_cache(self, clear_item = None):
        """ Clear the cache """

        if clear_item == None:
            self.cache.clear()
        elif self.key_exists(clear_item):
            del self.cache[clear_item]
        

    def add(self, *args):
        return args[0] + args[1]

    def subtract(self, *args):
        return args[0] - args[1]

    def multiply(self, *args):
        return args[0] * args[1]

    def power(self, *args):
        return args[0] ** args[1]

    def divide(self, *args):
        return args[0] / args[1]

    def build_int(self, *args):
        return int(''.join(args))

    def build_float(self, *args):
        return float(''.join(args))

    def array(self, *args):
        return smp.MutableDenseNDimArray(list(args))

    def differentiate(self, *args):
        expr = args[0]
        wrt = MathJSONInterpreter(self.get_operations_with_latest_cache()).interpret(args[1][0])
        return smp.diff(expr, wrt)

    def integrate(self, *args):
        expr = args[0]
        wrt = MathJSONInterpreter(self.get_operations_with_latest_cache()).interpret(args[1][0])
        return smp.integrate(expr, wrt)

    def simplify(self, *args):
        expr = args
        return smp.simplify(expr[0])

    def solve(self, *args):
        expr = args
        return smp.solve(expr[0])

    def numerical(self, *args):
        wrt = MathJSONInterpreter(self.get_operations_with_latest_cache()).interpret(args[1][0])
        return smp.N(args[0], wrt)

    def tensor(self, *args):
        tensor_string_representation = ''.join(args)
        tensor_name = re.match('([a-zA-Z]+)', tensor_string_representation).group()
        tesnor_indices = tensor_string_representation.replace(tensor_name, '')

        if self.key_exists('Metric') and self.key_exists('Basis'):
            self.METRIC  =  Metric(self.get_cached_value('Metric'), "_{a}_{b}", self.get_cached_value('Basis'))
        else:
            raise ValueError('No Metric has been defined')
        if tensor_name == 'G':
            return MetricWork(self.METRIC, tesnor_indices)
        elif tensor_name == 'd':
            return Derivative(self.METRIC.components, tesnor_indices, self.METRIC.basis)
        elif tensor_name == "R":
            return Riemann(self.METRIC, tesnor_indices)

    def minus(self, *args):
        a = args[0]
        return -a

    def series(self, *args):
        expr = args[0]
        if len(args[1]) == 2:
            point = MathJSONInterpreter(self.get_operations_with_latest_cache()).interpret(args[1][0])
            n = MathJSONInterpreter(self.get_operations_with_latest_cache()).interpret(args[1][1])
            return smp.series(expr, x0 = point, n = n)
        elif len(args[1]) == 1:
            point = MathJSONInterpreter(self.get_operations_with_latest_cache()).interpret(args[1][0])
            return smp.series(expr, x0 = point, n = 5)
        else:
            return smp.series(expr, x0 = 0, n = 5)

    def limit(self, *args):
        expr = args[0]
        x0 = MathJSONInterpreter(self.get_operations_with_latest_cache()).interpret(args[1][0])
        x1 = MathJSONInterpreter(self.get_operations_with_latest_cache()).interpret(args[1][1])
        return smp.limit(expr, x0, x1)

    def expand(self, *args):
        return smp.expand(args[0])

    def exp(self, *args):
        return smp.exp(args[0])

    def constant(self, *args):
        if args[0] == 'pi':
            return smp.pi
        if args[0] == 'e':
            return smp.E

    def variable(self, *args):
        a = ''.join(args)
        if self.key_exists(a):
            if isinstance(self.get_cached_value(a), (smp.Basic, smp.MutableDenseNDimArray)):
                return self.get_cached_value(a)
            else:
                return MathJSONInterpreter(self.get_operations_with_latest_cache()).interpret(Mathify(self.get_cached_value(a))())
        else:
            return smp.symbols('{}'.format(a))
    
    def sin(self, *args):
        return smp.sin(args[0])

    def cos(self, *args):
        return smp.cos(args[0])

    def tan(self, *args):
        return smp.tan(args[0])

    def asin(self, *args):
        return smp.asin(args[0])

    def acos(self, *args):
        return smp.acos(args[0])

    def atan(self, *args):
        return smp.atan(args[0])

    def sinh(self, *args):
        return smp.sinh(args[0])

    def cosh(self, *args):
        return smp.cosh(args[0])

    def tanh(self, *args):
        return smp.tanh(args[0])

    def asinh(self, *args):
        return smp.asinh(args[0])

    def acosh(self, *args):
        return smp.acosh(args[0])

    def atanh(self, *args):
        return smp.atanh(args[0])




