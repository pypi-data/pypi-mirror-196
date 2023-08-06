#
#     This file is part of rockit.
#
#     rockit -- Rapid Optimal Control Kit
#     Copyright (C) 2019 MECO, KU Leuven. All rights reserved.
#
#     Rockit is free software; you can redistribute it and/or
#     modify it under the terms of the GNU Lesser General Public
#     License as published by the Free Software Foundation; either
#     version 3 of the License, or (at your option) any later version.
#
#     Rockit is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#     Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public
#     License along with CasADi; if not, write to the Free Software
#     Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
#

from ...freetime import FreeTime
from ...casadi_helpers import prepare_build_dir
from ..method import ExternalMethod, linear_coeffs, check_Js
from ...solution import OcpSolution
from ...sampling_method import SamplingMethod

import numpy as np
from casadi import external, vec, CodeGenerator, SX, Sparsity, MX, vcat, veccat, symvar, substitute, densify, sparsify, DM, Opti, is_linear, vertcat, depends_on, jacobian, linear_coeff, quadratic_coeff, mtimes, pinv, evalf, Function, vvcat, inf, sum1, sum2, diag, solve, fmin, fmax
import casadi
import casadi as cs
from ...casadi_helpers import DM2numpy, reshape_number
from collections import OrderedDict

import subprocess
import os
from ctypes import *
import glob
import shutil
import platform
import hashlib
import fatrop.fatropy as fatropy

def get_terms(e):
    def get_terms_internal(e):
        if e.op()==cs.OP_ADD:
            for i in range(e.n_dep()):
                for t in get_terms_internal(e.dep(i)):
                    yield t
        else:
            yield e
    return list(get_terms_internal(e))


def visit(e,parents=None):
    if parents is None:
        parents = []
    yield (e,parents)
    for i in range(e.n_dep()):
        for t in visit(e.dep(i),parents=[e]+parents):
            yield t

"""
conda install -c conda-forge make cmake
"""

external_dir = os.path.join(os.path.dirname(__file__),"external")

if not os.path.exists(external_dir):
    raise Exception("FATROP source not found")

def run_build(cwd=None):
    subprocess.run(["bash","build.sh"],cwd=cwd)

INF = inf



stats_fields = [('stop_crit',c_int),('conv_grad',c_int),('conv_con',c_int),('n_outer_iter',c_int),('n_inner_iter',c_int),('runtime',c_double)]

class StatsStruct(Structure):
    _fields_ = stats_fields


def format_float(e):
    return "%0.18f" % e

def strlist(a):
    elems = []
    for e in a:
        if isinstance(e,str):
            elems.append('"'+e+'"')
        elif isinstance(e,float):
            elems.append(format_float(e))
        else:
            elems.append(str(e))
    return ",".join(elems)
    
def check_Js(J):
    """
    Checks if J, a pre-multiplier for slacks, is of legitimate structure
    Empty rows are allowed
    """
    try:
        J = evalf(J)
    except:
        raise Exception("Slack error")
    assert np.all(np.array(J.nonzeros())==1), "All nonzeros must be 1"
    # Check if slice of permutation of unit matrix
    assert np.all(np.array(sum2(J))<=1), "Each constraint can only depend on one slack at most"
    assert np.all(np.array(sum1(J))<=1), "Each constraint must depend on a unique slack, if any"

def fill_in(var, expr,value, array, k):
    value = evalf(value)
    J, r = linear_coeffs(var,expr)
    J = evalf(J)
    r = evalf(r)
    assert r.is_zero()
    check_Js(J)
    expr = reshape_number(var, expr)
    if J.sparsity().get_col():
        array[J.sparsity().get_col(), k] = value[J.row()]
def fill_in_array(var, expr, value, array):
    value = evalf(value)
    J, r = linear_coeffs(var[:,0],expr)
    J = evalf(J)
    r = evalf(r)
    assert r.is_zero()
    check_Js(J)
    expr = reshape_number(var, expr)
    if J.sparsity().get_col():
        array[J.sparsity().get_col(), :] = value[J.row(), :]
def get_offsets(var, expr):
    J, r = linear_coeffs(var,expr)
    J = evalf(J)
    r = evalf(r)
    assert r.is_zero()
    check_Js(J)
    expr = reshape_number(var, expr)
    return (J.row(), J.sparsity().get_col())

def mark(slack, Js):
    assert np.all(np.array(slack[Js.sparsity().get_col()])==0)
    slack[Js.sparsity().get_col()] = 1

def export_expr(m):
    if isinstance(m,list):
        if len(m)==0:
            return MX(0, 1)
        else:
            return vcat(m)
    return m

def export_num(m):
    res=np.array(evalf(export_expr(m)))
    if np.any(res==-inf) or np.any(res==inf):
        print("WARNING: Double-sided constraints are much preferred. Replaced inf with %f." % INF)
    res[res==-inf] = -INF
    res[res==inf] = INF
    return res

def export_num_vec(m):
    return np.array(evalf(export_expr(m))).reshape(-1)

def export(m):
    return (export_expr(m),False)

def export_vec(m):
    return (export_expr(m),True)

class MyCodeGenerator:
    def __init__(self,name):
        self.added_shorthands = set()
        self.add_includes = []
        self.prefix = ""
        self.auxiliaries = ""
        self.body = ""
        self.name = name

    def add_include(self,h):
        self.add_includes.append(h)

    def shorthand(self,name):
        self.added_shorthands.add(name)
        return self.prefix + name

    def add_dependency(self, f):
        name = f.codegen_name(self, False)
        fname = self.prefix + name
        stack_counter = self.shorthand(name + "_unused_stack_counter")
        stack = self.shorthand(name + "_unused_stack")
        mem_counter = self.shorthand(name + "_mem_counter")
        mem_array = self.shorthand(name + "_mem")
        alloc_mem = self.shorthand(name + "_alloc_mem")
        init_mem = self.shorthand(name + "_init_mem")
        work = self.shorthand(name+"_work")

        self.auxiliaries += f"#include <iostream>\n"
        self.auxiliaries += f"static int {mem_counter} = 0;\n"
        self.auxiliaries += f"static int {stack_counter } = -1;\n"
        self.auxiliaries += f"static int {stack}[CASADI_MAX_NUM_THREADS];\n"
        # self.auxiliaries += f"static {f.codegen_mem_type()} *{mem_array}[CASADI_MAX_NUM_THREADS];\n\n"

        # f.codegen_declarations(self)

        f.codegen(self, fname)

        def encode_sp(sp,i):
            r = f"case {i}:\n"
            r+= "{"
            spc = sp.compress()
            r+= f"static casadi_int sp[{len(spc)}] = {{{strlist(spc)}}}; return sp;"
            r+= "}"
            return r

        def encode_name(n,i):
            return f"case {i}: return \"{n}\";\n"

        newline = "\n"

        self.body += f"""

            casadi_int {fname}_n_in(void) {{
                return {f.n_in()};
            }}

            casadi_int {fname}_n_out(void) {{
                return {f.n_out()};
            }}

            const casadi_int* {fname}_sparsity_in(casadi_int i) {{
                switch (i) {{
                {newline.join(encode_sp(f.sparsity_in(i), i) for i in range(f.n_in()))}
                default: return 0;
                }}
            }}

            const casadi_int* {fname}_sparsity_out(casadi_int i) {{
                switch (i) {{
                {newline.join(encode_sp(f.sparsity_out(i), i) for i in range(f.n_out()))}
                default: return 0;
                }}
            }}

            const char* {fname}_name_in(casadi_int i) {{
                switch (i) {{
                {newline.join(encode_name(f.name_in(i), i) for i in range(f.n_in()))}
                default: return 0;
                }}
            }}

            const char* {fname}_name_out(casadi_int i) {{
                switch (i) {{
                {newline.join(encode_name(f.name_out(i), i) for i in range(f.n_out()))}
                default: return 0;
                }}
            }}

            int {fname}_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w) {{
            {f.codegen_work(self)}
              return 0;
            }}

            // Alloc memory
            int {fname}_alloc_mem(void) {{
            {f.codegen_alloc_mem(self)}
            }}

            // Initialize memory
            int {fname}_init_mem(int mem) {{
            {f.codegen_init_mem(self)}
            }}

            // Clear memory
            void {fname}_free_mem(int mem) {{
            {f.codegen_free_mem(self)}
            }}

            int {self.shorthand(name + "_checkout")}(void) {{
            int mid;
            if ({stack_counter}>=0) {{
              return {stack}[{stack_counter}--];
            }} else {{
              if ({mem_counter}==CASADI_MAX_NUM_THREADS) return -1;
              mid = {alloc_mem}();
              if (mid<0) return -1;
              if({init_mem}(mid)) return -1;
              return mid;
            }}

            return {stack}[{stack_counter}--];
        }}

        void {self.shorthand(name+"_release")}(int mem) {{
            {stack}[++{stack_counter}] = mem;
        }}


        """

    def generate(self,dir="."):
        with open(os.path.join(dir,self.name+".cpp"),"w") as out:
            out.write("#define CASADI_MAX_NUM_THREADS 1\n")
            for e in self.add_includes:
                out.write(f"#include \"{e}\"\n")
            out.write(self.auxiliaries)
            out.write(self.body)

class Wrapper:
    def __init__(self,userparam):
        self.added_declarations = ""
        self.added_init_mem = ""
        self.added_body = ""
        self.sp_in = []
        self.sp_out = []
        self._name_in = []
        self._name_out = []
        self.userparam = userparam

    def set_sp_in(self, sp):
        self.sp_in = sp

    def set_sp_out(self, sp):
        self.sp_out = sp

    def set_name_in(self, name):
        self._name_in = name

    def set_name_out(self, name):
        self._name_out = name

    def add_declarations(self, decl):
        self.added_declarations += decl
    
    def add_init_mem(self, init_mem):
        self.added_init_mem += init_mem

    def add_body(self, body):
        self.added_body += body

    def signature(self, fname):
        return "int " + fname + "(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem)"

    def codegen(self, g, fname):
        g.body += f"{self.signature(fname)} {{\n"
        self.codegen_body(g)
        g.body += f"return 0;}}\n"

    def codegen_name(self, g, ns):
        return "fatrop_driver"
    # def codegen_mem_type(self):
    #     return "typeFATROP"
    def codegen_alloc_mem(self, g):
        name = self.codegen_name(g, False)
        mem_counter = g.shorthand(name + "_mem_counter")
        return f"return {mem_counter}++;"

    def codegen_init_mem(self, g):
        fatrop = self.codegen_mem(g, "mem")
        userparam = fatrop+"->userparam"
        return f"""
        // typeFATROP *fatrop = {fatrop};
        {self.added_init_mem}
        {fatrop} = fatrop;
        return 0;
        
        """

    def codegen_free_mem(self, g):
        fatrop = self.codegen_mem(g)
        userparam = fatrop+"->userparam"
        return f"postamble({userparam});\nfree({userparam});"

    def codegen_mem(self, g, index=0):
        name = self.codegen_name(g, False)
        mem_array = g.shorthand(name + "_mem")
        return mem_array+"[" + str(index) + "]"

    def codegen_body(self, g):
        g.body += self.added_body

    def n_in(self):
        return len(self.sp_in)

    def n_out(self):
        return len(self.sp_out)

    def sparsity_in(self, i):
        return self.sp_in[i]

    def sparsity_out(self, i):
        return self.sp_out[i]

    def name_in(self, i):
        return self._name_in[i]

    def name_out(self, i):
        return self._name_out[i]


    def codegen_work(self, g):
        r = f"""
            casadi_int sz_arg_local, sz_res_local, sz_iw_local, sz_w_local;
            *sz_arg=0, *sz_res=0, *sz_iw=0, *sz_w=0;
            //pmap_work(&sz_arg_local, &sz_res_local, &sz_iw_local, &sz_w_local);
            if (sz_arg_local>*sz_arg) *sz_arg=sz_arg_local;
            if (sz_res_local>*sz_res) *sz_res=sz_res_local;
            if (sz_iw_local>*sz_iw) *sz_iw=sz_iw_local;
            if (sz_w_local>*sz_iw) *sz_w=sz_w_local;

            *sz_arg += {self.n_in()};
            *sz_res += {self.n_out()};
        """
        return r



class SourceArtifact:
    def __init__(self, name):
        self.name = name





class FatropMethod(ExternalMethod):
    def __init__(self,
        verbose=False,
        fatrop_options=None,
        intg= 'rk',
        M = 1,
        **kwargs):
        """
        dt is post-processing: interplin
        

        GRAMPC is very much realtime iteration
        By default, ConvergenceCheck is even off, and you perform MaxMultIter outer iterations with MaxGradIter inner iterations.
        Default MaxMultIter = 1.

        
        """
        self.build_dir_abs = "foobar"
        supported = {}
        ExternalMethod.__init__(self, supported=supported, **kwargs)
        self.fatrop_options = {} if fatrop_options is None else fatrop_options
        our_defaults = {}
        for k,v in our_defaults.items():
            if k not in self.fatrop_options:
                self.fatrop_options[k] = v
        self.codegen_name = 'casadi_codegen'
        self.fatrop_driver = 'fatrop_driver'
        self.user = "((cs_struct*) userparam)"
        self.user_fatrop = "((cs_struct*) fatrop->userparam)"
        self.Nhor = self.N+1
        self.intg = intg
        self.M = M #Assumption!
        # self.N = N
        self.verbose = verbose
        self.artifacts = []
        self.poly_coeff = []  # Optional list to save the coefficients for a polynomial
        self.poly_coeff_z = []  # Optional list to save the coefficients for a polynomial
        self.xk = []  # List for intermediate integrator states
        self.zk = []
        self.samplers = {}
        self.variable_names = {}
    def set_name(self, name):
        self.build_dir_abs = name 
    def regname(self, symbol_in, name):
        self.variable_names[symbol_in] = name

    def fill_placeholders_integral(self, phase, stage, expr, *args):
        raise Exception("ocp.integral not supported. Use ocp.sum instead.")
        # if phase==1:
        #     return expr

    def fill_placeholders_sum_control(self, phase, stage, expr, *args):
        if phase == 1:
            return expr
        # raise Exception("ocp.sum not supported. Use ocp.integral instead.")

    def fill_placeholders_sum_control_plus(self, phase, stage, expr, *args):
        if phase == 1:
            return expr

    def fill_placeholders_DT_discrete(self, phase, stage, expr, *args):
        if phase == 1:
            if not stage._state_next:
                raise Exception("Discrete time integrator DT found but dynamics ode is continuous time") 
        return None

    def _register(self,fun_name,argtypes,restype):
        self.prefix=""
        fun = getattr(self.lib,self.prefix+fun_name)
        setattr(self,"_"+fun_name,fun)
        fun.argtypes = argtypes
        fun.restype = restype

    def transcribe_phase1(self, stage, **kwargs):

        # It is not really transcription because FATROP simply takes stage-wise costs as input. Not a large NLP as input.
        #Phase 1 deals with creating placeholder variables and objectives

        self.preamble = ["casadi_int sz_arg=0, sz_res=0, sz_iw=0, sz_w=0;",
                         "casadi_int sz_arg_local, sz_res_local, sz_iw_local, sz_w_local;",
                        ]
        self.postamble = []

        self.stage = stage
        self.opti = Opti()

        # Is computing the whole grid needed for FATROP?
        ## self.time_grid = self.grid(stage._t0, stage._T, self.N)
        self.normalized_time_grid = self.grid(0.0, 1.0, self.N)
        self.time_grid = self.normalized_time_grid
        if self.t_state:
            if isinstance(stage._T, FreeTime):
                stage.set_initial(stage.t, self.time_grid*stage._T.T_init)
            else:
                stage.set_initial(stage.t, self.time_grid*stage._T)
        if not isinstance(stage._T, FreeTime): self.time_grid*= stage._T
        if not isinstance(stage._t0, FreeTime): self.time_grid+= stage._t0
        self.control_grid = MX(stage.t0 + self.normalized_time_grid*stage.T).T

        if not isinstance(stage._T, FreeTime) and not isinstance(stage._t0, FreeTime):
            dT = stage._T/(self.N)
        else:
            dT = self.T/(self.N)
            stage.subject_to(stage.at_t0(self.T)>0)
            stage.set_initial(self.T, stage._T.T_init)

        # f = stage._ode()
        f = SamplingMethod(intg = self.intg, M = self.M).discrete_system(stage).expand()

        xkp1 = MX.sym('xkp1', stage.nx)
        x_sym = stage.x # MX.sym('x', stage.nx)
        u_sym = stage.u #MX.sym('u', stage.nu)
        global_params_sym = stage.p #MX.sym('p', stage.np)
        stage_params_sym = vertcat(*(stage.parameters['control'] + stage.parameters['control+']))
        self.stage_params_sym = stage_params_sym
        global_params_sym = vertcat(*stage.parameters[''])
        self.global_params_sym = global_params_sym
        x_next, _, _, _, _, _, _ = f(x_sym, u_sym, dT, 0, stage.p)
        self.x_next = x_next
        b_x = - xkp1 + x_next

        options = {}
        options["with_header"] = True
        self.codegen = CodeGenerator(f"{self.codegen_name}.c", options)

        BAbt = cs.jacobian(x_next, vertcat(u_sym, x_sym)).T
        BAbt = cs.vertcat(BAbt, b_x.T)
        # self.codegen.add(Function("BAbt", [xkp1, u_sym, x_sym, stage_params_sym, global_params_sym],  [densify(BAbt)]).expand())
        # self.codegen.add(Function("bk", [xkp1, u_sym, x_sym, stage_params_sym, global_params_sym], [densify(b_x)]).expand())

        


        

        self.artifacts.append(SourceArtifact(f"{self.codegen_name}.c"))
        self.artifacts.append(SourceArtifact(f"{self.codegen_name}.h"))

        self.wrapper_codegen = MyCodeGenerator(self.fatrop_driver)
        self.wrapper_codegen.add_include(f"{self.codegen_name}.h")
        self.wrapper_codegen.add_include("ocp/OCPBuiler.hpp")
        self.wrapper_codegen.add_include("time.h")
        self.wrapper_codegen.add_include("string.h")

        self.artifacts.append(SourceArtifact(f"{self.fatrop_driver}.cpp"))
        self.wrapper = Wrapper(userparam=self.user_fatrop)

        assert len(stage.variables['control'])==0, "variables defined on control grid not supported. Use controls instead."

        self.v = vvcat(stage.variables[''])
        self.X_gist = [MX.sym("Xg", stage.nx) for k in range(self.N+1)]
        self.U_gist = [MX.sym("Ug", stage.nu) for k in range(self.N)]
        self.V_gist = MX.sym("Vg", *self.v.shape)
        self.T_gist = MX.sym("Tg")

        # assert f.numel_out("alg")==0
        # assert f.numel_out("quad")==0
        # ffct = Function("cs_ffct", [stage.t, stage.x, stage.u, self.v, stage.p], [ densify(f(x=stage.x, u=stage.u, p=stage.p, t=stage.t)["ode"])],['t','x','u','p','p_fixed'],['out'])
        # self.gen_interface(ffct)
        # self.gen_interface(ffct.factory("cs_dfdx_vec",["t","x","adj:out","u","p","p_fixed"],["densify:adj:x"]))
        # self.gen_interface(ffct.factory("cs_dfdu_vec",["t","x","adj:out","u","p","p_fixed"],["densify:adj:u"]))
        # self.gen_interface(ffct.factory("cs_dfdp_vec",["t","x","adj:out","u","p","p_fixed"],["densify:adj:p"]))

        self.X = self.opti.variable(*stage.x.shape)
        self.U = self.opti.variable(*stage.u.shape)
        self.V = self.opti.variable(*self.v.shape)
        self.P = self.opti.parameter(*stage.p.shape)
        self.t = self.opti.parameter()
        self.T = self.opti.variable()

        self.raw = [stage.x,stage.u,stage.p,stage.t, self.v]
        self.optivar = [self.X, self.U, self.P, self.t, self.V]
        if self.free_time:
            self.raw += [stage.T]
            self.optivar += [self.T]

        

        inits = []
        inits.append((stage.T, stage._T.T_init if isinstance(stage._T, FreeTime) else stage._T))
        inits.append((stage.t0, stage._t0.T_init if isinstance(stage._t0, FreeTime) else stage._t0))

        self.control_grid_init = evalf(substitute([self.control_grid], [a for a,b in inits],[b for a,b in inits])[0])

        #self.control_grid = self.normalized_time_grid

        self.lagrange = MX(0)
        self.mayer = MX(0)
        self.objI = MX(0)
        var_mayer = []
        obj = MX(stage._objective)
        terms = get_terms(obj)
        for term in terms:
            n = [e.name() for e in symvar(term)]
            sumi = np.sum([e=="r_sum_control" for e in n])
            sumip = np.sum([e=="r_sum_control_plus" for e in n])
            summ = np.sum([e=="r_at_tf" for e in n])
            summI = np.sum([e=="r_at_t0" for e in n])
            if sumi + sumip + summ  + summI!= 1:
                raise Exception("Objective cannot be parsed")
            if sumi==1 or sumip ==1:
                n_hits = 0
                for e,parents in visit(term):
                    if e.is_symbolic() and e.name()=="r_sum_control":
                        n_hits+=1
                        for pi in range(len(parents)):
                            p = parents[pi]
                            pchild = parents[pi-1] if pi>0 else e
                            correct = False
                            # Distributive operations
                            if p.op()==cs.OP_MUL:
                                correct = True
                            if p.op()==cs.OP_DIV:
                                # Only allow integral in LHS
                                correct = hash(p.dep(0))==hash(pchild)
                            assert correct, "Objective cannot be parsed: integrals can only be multiplied or divided."
                    if n_hits>1:
                        raise Exception("Objective cannot be parsed")
                if summ!=0:
                    raise Exception("Objective cannot be parsed: operation combining integral and at_tf part not supported")
                self.lagrange += term
                self.objI += term
            if sumip==1 or summ ==1:
                self.mayer += term
            if summI ==1:
                self.objI += term 
        self.P0 = DM.zeros(stage.np)

    def set_value(self, stage, master, parameter, value):
        value = evalf(value)
        if parameter in stage.parameters['']:
            p = vec(parameter)
            fill_in(p, self.global_params_sym, value, self.global_params_value,0)
        else:
            p = vec(parameter)
            # for k in list(range(self.N)):
            if p.numel()==value.numel():
                if(value.shape[1] == p.shape[0]):
                    value = value.T
                value = cs.repmat(value,  1, self.N+1)
            if p.numel()*(self.N)==value.numel() or p.numel()*(self.N+1)== value.numel():
                if(value.shape[1] == p.shape[0]):
                    value = value.T
            assert(value.shape[0] == p.shape[0])
            if p.numel()*(self.N)== value.numel():
                value = cs.horzcat(value, value[:,-1])
            fill_in_array(p, self.stage_params_sym, value, self.stage_params_value)


        ## TODO this seems to work but is this the right way to do it?
        # master.stage._param_vals[parameter] = value
    def get_parameters(self, stage):
        self.global_params_value = DM.zeros(self.global_params_sym.shape)
        self.stage_params_value = DM.zeros(self.stage_params_sym.shape[0], self.N+1)
        for i, p in enumerate(stage.parameters['']):
            self.set_value(stage, None, p, stage._param_value(p))
        for i, p in enumerate(stage.parameters['control'] + stage.parameters['control+']):
            self.set_value(stage,None,  p, stage._param_value(p))
        return self.global_params_value, self.stage_params_value
    def set_initial(self, arg1, arg2, initial_dict):
        self.U0, self.X0 = self.get_initial(self.stage, initial_dict)
        self.myOCP.SetInitial(self.U0.T.full().flatten(), self.X0.T.full().flatten())
        pass
    def add_sampler(self, name, expr):
        self.samplers[name] = expr
    def get_initial(self, stage, initial_dict):

        U0= DM.zeros(stage.nu, self.N)
        X0 = DM.zeros(stage.nx, self.N+1)
        for var, expr in initial_dict.items():
                # print(var, expr)
                var = vec(var)
                expr = expr
                value = evalf(expr)
                # value = vec(value)
                if depends_on(var,stage.u):
                    assert not depends_on(var, self.v)
                    if var.numel()==value.numel():
                        value = vec(value)
                        if(value.shape[1] == var.shape[0]):
                            value = value.T
                        value = cs.repmat(value,  1, self.N)
                    if var.numel()*(self.N)==value.numel():
                        if(value.shape[1] == var.shape[0]):
                            value = value.T
                    if var.numel()*(self.N+1)==value.numel():
                        if(value.shape[1] == var.shape[0]):
                            value = value.T
                        value = value[:,:-1]
                    assert(value.shape[0] == var.shape[0])
                    fill_in_array(var, stage.u, value, U0)
                if depends_on(var,stage.x):
                    assert not depends_on(vec(var), self.v)
                    if var.numel()==value.numel():
                        value = vec(value)
                        if(value.shape[1] == var.shape[0]):
                            value = value.T
                        value = cs.repmat(value,  1, self.N+1)
                    if var.numel()*(self.N+1)==value.numel():
                        if(value.shape[1] == var.shape[0]):
                            value = value.T
                    assert(value.shape[0] == var.shape[0])
                    fill_in_array(var, stage.x, value, X0)
        return U0, X0

    # def eval_expr(expr, )
    def transcribe_phase2(self, stage, **kwargs):

        # Phase 2 adds the constraints
        
        opti_advanced = self.opti.advanced
        placeholders = kwargs["placeholders"]



        # Total Lagrange integrand
        lagrange = placeholders(self.lagrange,preference=['expose'])
        # Total Mayer term
        mayer = placeholders(self.mayer,preference=['expose'])
        objI = placeholders(self.objI,preference=['expose'])
        self.x_next = placeholders(self.x_next, preference='expose')

        x0_eq = []
        x0_b = []

        eq_init = [MX.zeros(0)]
        eq_mid = [MX.zeros(0)] #
        eq_term = [MX.zeros(0)]
        ineq_init = [MX.zeros(0)]
        ineq_mid = [MX.zeros(0)] # <=0
        ineq_term = [MX.zeros(0)]
        ub_init = [MX.zeros(0)]
        lb_init = [MX.zeros(0)]
        ub_mid = [MX.zeros(0)]
        lb_mid = [MX.zeros(0)]
        ub_term = [MX.zeros(0)]
        lb_term = [MX.zeros(0)]  

        # Process initial point constraints
        # Probably should de-duplicate stuff wrt path constraints code
        for c, meta, _ in stage._constraints["point"]:
            # Make sure you resolve u to r_at_t0/r_at_tf

            if not 'r_at_t0' in [a.name() for a in symvar(c)]:
                continue
            c = placeholders(c,max_phase=1)

            cb = c
            c = substitute([placeholders(c,preference='expose')],self.raw,self.optivar)[0]
            mc = opti_advanced.canon_expr(c) # canon_expr should have a static counterpart
            lb,canon,ub = substitute([mc.lb,mc.canon,mc.ub],self.optivar,self.raw)
            check = not depends_on(canon, vertcat(self.v))
            assert check, 'v variables are not supported yet'
            if mc.type == casadi.OPTI_EQUALITY:
                eq_init.append(canon-ub)
            else:
                assert mc.type in [casadi.OPTI_INEQUALITY, casadi.OPTI_GENERIC_INEQUALITY, casadi.OPTI_DOUBLE_INEQUALITY]
                ineq_init.append(canon)
                ub_init.append(ub)
                lb_init.append(lb)
        
        # Process terminal point constraints
        # Probably should de-duplicate stuff wrt path constraints code
        for c, meta, _ in stage._constraints["point"]:
            # Make sure you resolve u to r_at_t0/r_at_tf

            if not 'r_at_tf' in [a.name() for a in symvar(c)]:
                continue
            c = substitute([placeholders(c,preference='expose')],self.raw,self.optivar)[0]
            mc = opti_advanced.canon_expr(c) # canon_expr should have a static counterpart
            lb,canon,ub = substitute([mc.lb,mc.canon,mc.ub],self.optivar,self.raw)

            check = not depends_on(canon, vertcat(stage.u, self.v))
            assert check, "at t=tF, only constraints on x are allowed. Got '%s'" % str(c)

            if mc.type == casadi.OPTI_EQUALITY:
                eq_term.append(canon-ub)
            else:
                assert mc.type in [casadi.OPTI_INEQUALITY, casadi.OPTI_GENERIC_INEQUALITY, casadi.OPTI_DOUBLE_INEQUALITY]
                ineq_term.append(canon)
                ub_term.append(ub)
                lb_term.append(lb)
        

        # Process path constraints
        # TODO check for include first and include last
        for c, meta, args in stage._constraints["control"]+stage._constraints["integrator"]:
            c = substitute([placeholders(c,preference=['expose'])],self.raw,self.optivar)[0]
            mc = opti_advanced.canon_expr(c) # canon_expr should have a static counterpart
            lb,canon,ub = substitute([mc.lb,mc.canon,mc.ub],self.optivar,self.raw)
            check = not depends_on(canon, vertcat(self.v))
            assert check, 'v variables'
            # lb <= canon <= ub
            # Check for infinities
            try:
                lb_inf = np.all(np.array(evalf(lb)==-inf))
            except:
                lb_inf = False
            try:
                ub_inf = np.all(np.array(evalf(ub)==inf))
            except:
                ub_inf = False

            if mc.type == casadi.OPTI_EQUALITY:
                eq_mid.append(canon-ub)
                if args['include_first']:
                    eq_init.append(canon-ub)
                if args['include_last']:
                    check = not depends_on(canon, vertcat(stage.u, self.v))
                    if not check and not depends_on(canon, vertcat(stage.x)): continue
                    assert check, "at t=tF, only constraints on x are allowed. Got '%s'" % str(c)
                    eq_term.append(canon-ub)
            else:
                assert mc.type in [casadi.OPTI_INEQUALITY, casadi.OPTI_GENERIC_INEQUALITY, casadi.OPTI_DOUBLE_INEQUALITY]

                ineq_mid.append(canon)
                ub_mid.append(ub)
                lb_mid.append(lb)
                if args['include_first']:
                    ineq_init.append(canon)
                    ub_init.append(ub)
                    lb_init.append(lb)
                if args['include_last']:
                    check = not depends_on(canon, vertcat(stage.u, self.v))
                    if not check and not depends_on(canon, vertcat(stage.x)): continue
                    assert check, "at t=tF, only constraints on x are allowed. Got '%s'" % str(c)
                    ineq_term.append(canon)
                    ub_term.append(ub)
                    lb_term.append(lb)
        


        #### parameters
        global_params_value, stage_params_value =self.global_params_value, self.stage_params_value = self.get_parameters(stage)

        #### initializiaton
        U0, X0 = self.U0, self.X0 = self.get_initial(stage, stage._initial)


        eqI = vvcat(eq_init)
        eq = vvcat(eq_mid)
        eqF = vvcat(eq_term)
        ineqI = vvcat(ineq_init)
        ineq = vvcat(ineq_mid)
        ineqF = vvcat(ineq_term)
        lb_init = vvcat(lb_init)
        ub_init = vvcat(ub_init)
        lb_mid = vvcat(lb_mid)
        ub_mid = vvcat(ub_mid)
        ub_term = vvcat(ub_term)
        lb_term = vvcat(lb_term)

        ngI = eqI.shape[0]
        ng = eq.shape[0]
        ngF = eqF.shape[0]
        ngIneqI = ineqI.shape[0]
        ngIneq = ineq.shape[0]
        ngIneqF = ineqF.shape[0]
        dual_dyn = MX.sym('d_dyn', stage.nx)
        dual_eqI = MX.sym('d_eqI', ngI)
        dual_eq = MX.sym('d_eq', ng)
        dual_eqF = MX.sym('d_eqF', ngF)
        dualIneqI = MX.sym('d_IneqI', ngIneqI)
        dualIneq = MX.sym('d_Ineq', ngIneq)
        dualIneqF = MX.sym('d_IneqF', ngIneqF)
        nx = stage.nx
        nu = stage.nu

        #TODO: Stagewise equality constraints seem to be missing in FATROP?

        obj_scale = MX.sym('obj_scale')
                # BAbt
        stateskp1 = MX.sym("states_kp1", nx)
        BAbt = MX.zeros(nu+nx+1, nx)
        BAbt[:nu+nx,
             :] = jacobian(self.x_next, vertcat(stage.u, stage.x)).T
        b = (-stateskp1 + self.x_next)[:]
        BAbt[nu+nx, :] = b
        self.codegen.add(
            Function("BAbt", [stateskp1, stage.u, stage.x, self.stage_params_sym, self.global_params_sym], [densify(BAbt)]).expand())
        # b
        self.codegen.add(Function("bk", [stateskp1, stage.u,
                              stage.x, self.stage_params_sym, self.global_params_sym], [densify(b)]).expand())
        # RSQrqtI
        RSQrqtI = MX.zeros(nu+nx+1, nu + nx)
        [RSQI, rqI] = cs.hessian(objI, vertcat(stage.u, stage.x))
        RSQIGN = RSQI
        rqlagI = rqI
        if ngI > 0:
            [H, h]= cs.hessian(dual_eqI.T@eqI, vertcat(stage.u, stage.x))
            RSQI += H
            rqlagI += h
        [H,h] = cs.hessian(dual_dyn.T@self.x_next,
                        vertcat(stage.u, stage.x))
        RSQI += H
        rqlagI += h
        
        if ngIneqI > 0:
            [H,h] = cs.hessian(dualIneqI.T@ineqI,
                            vertcat(stage.u, stage.x))
            RSQI += H
            rqlagI += h
        RSQrqtI[:nu+nx, :] = RSQI
        RSQrqtI[nu+nx, :] = rqlagI[:]
        self.codegen.add(Function("RSQrqtI", [obj_scale, stage.u,
              stage.x, dual_dyn, dual_eqI, dualIneqI, self.stage_params_sym, self.global_params_sym], [densify(RSQrqtI)]).expand())
        RSQrqtI[:nu+nx, :] = RSQIGN
        RSQrqtI[nu+nx, :] = rqlagI[:]
        self.codegen.add(Function("RSQrqtIGN", [obj_scale, stage.u,
              stage.x, dual_dyn, dual_eqI, dualIneqI, self.stage_params_sym, self.global_params_sym], [densify(RSQrqtI)]).expand())
        # rqI
        self.codegen.add(Function("rqI", [obj_scale,
              stage.u, stage.x, self.stage_params_sym, self.global_params_sym], [densify(rqI)]).expand())
        # RSQrqt
        RSQrqt = MX.zeros(nu+nx+1, nu + nx)
        [RSQ, rq] = cs.hessian(lagrange, vertcat(stage.u, stage.x))
        RSQGN = RSQ
        rqlag = rq
        if ng > 0:
            [H, h]= cs.hessian(dual_eq.T@eq, vertcat(stage.u, stage.x))
            RSQ += H
            rqlag += h
        [H,h]= cs.hessian(dual_dyn.T@self.x_next,
                       vertcat(stage.u, stage.x))
        RSQ += H
        rqlag +=h

        if ngIneq > 0:
            [H,h] = cs.hessian(dualIneq.T@ineq,
                           vertcat(stage.u, stage.x))
            RSQ += H
            rqlag +=h
        RSQrqt[:nu+nx, :] = RSQ
        RSQrqt[nu+nx, :] = rqlag[:]
        self.codegen.add(Function("RSQrqt", [obj_scale, stage.u, stage.x,
              dual_dyn, dual_eq, dualIneq, self.stage_params_sym, self.global_params_sym], [densify(RSQrqt)]).expand())
        RSQrqt[:nu+nx, :] = RSQGN
        RSQrqt[nu+nx, :] = rqlag[:]
        self.codegen.add(Function("RSQrqtGN", [obj_scale, stage.u, stage.x,
              dual_dyn, dual_eq, dualIneq, self.stage_params_sym, self.global_params_sym], [densify(RSQrqt)]).expand())
        # rqF
        self.codegen.add(Function("rqk", [obj_scale,
              stage.u, stage.x, self.stage_params_sym, self.global_params_sym], [densify(rq)]).expand())
        # Lk
        self.codegen.add(Function("LI", [obj_scale, stage.u,
              stage.x, self.stage_params_sym, self.global_params_sym], [densify(objI)]).expand())
        # Lk
        self.codegen.add(Function("Lk", [obj_scale, stage.u,
              stage.x, self.stage_params_sym, self.global_params_sym], [densify(lagrange)]).expand())
        # RSQrqtF
        RSQrqtF = MX.zeros(nx+1, nx)
        [RSQF, rqF] = cs.hessian(mayer, vertcat(stage.x))
        RSQFGN = RSQF
        rqlagF = rqF
        if ngF > 0:
            [H, h]= cs.hessian(dual_eqF.T@eqF,
                            vertcat(stage.x))
            RSQF += H
            rqlagF += h
        if ngIneqF > 0:
            [H,h] = cs.hessian(dualIneqF.T@ineqF,
                           vertcat(stage.x))
            RSQF += H
            rqlagF += h
        # if ngIneq>-1:
        #     RSQF += cs.hessian(dualIneq.T@ineq, vertcat(stage.u, stage.x))[-1]
        RSQrqtF[:nx, :] = RSQF
        RSQrqtF[nx, :] = rqlagF[:]
        self.codegen.add(Function("RSQrqtF", [obj_scale, stage.u, stage.x,
              dual_dyn, dual_eqF, dualIneqF, self.stage_params_sym, self.global_params_sym], [densify(RSQrqtF)]).expand())
        RSQrqtF[:nx, :] = RSQFGN
        RSQrqtF[nx, :] = rqlagF[:]
        self.codegen.add(Function("RSQrqtFGN", [obj_scale, stage.u, stage.x,
              dual_dyn, dual_eqF, dualIneqF, self.stage_params_sym, self.global_params_sym], [densify(RSQrqtF)]).expand())
        # rqF
        self.codegen.add(Function("rqF", [obj_scale,
              stage.u, stage.x, self.stage_params_sym, self.global_params_sym], [densify(rqF)]).expand())
        # LF
        self.codegen.add(Function("LF", [obj_scale, stage.u,
              stage.x, self.stage_params_sym, self.global_params_sym], [densify(mayer)]).expand())
        # GgtI
        GgtI = MX.zeros(nu+nx+1, ngI)
        GgtI[:nu+nx,
             :] = jacobian(eqI, vertcat(stage.u, stage.x)).T
        GgtI[nu+nx, :] = eqI[:].T
        self.codegen.add(Function(
            "GgtI", [stage.u, stage.x, self.stage_params_sym, self.global_params_sym], [densify(GgtI)]).expand())
        # g_I
        self.codegen.add(Function("gI", [stage.u, stage.x, self.stage_params_sym,
              self.global_params_sym], [densify(eqI[:])]).expand())
        # Ggt
        Ggt = MX.zeros(nu+nx+1, ng)
        Ggt[:nu+nx,
             :] = jacobian(eq, vertcat(stage.u, stage.x)).T
        Ggt[nu+nx, :] = eq[:].T
        self.codegen.add(Function(
            "Ggt", [stage.u, stage.x, self.stage_params_sym, self.global_params_sym], [densify(Ggt)]).expand())
        # g
        self.codegen.add(Function("g", [stage.u, stage.x, self.stage_params_sym,
              self.global_params_sym], [densify(eq[:])]).expand())
        # GgtF
        GgtF = MX.zeros(nx+1, ngF)
        GgtF[:nx, :] = jacobian(eqF, stage.x).T
        GgtF[nx, :] = eqF[:].T
        self.codegen.add(Function(
            "GgtF", [stage.u, stage.x, self.stage_params_sym, self.global_params_sym], [densify(GgtF)]).expand())
        # g_F
        self.codegen.add(Function("gF", [stage.u, stage.x, self.stage_params_sym,
              self.global_params_sym], [densify(eqF[:])]).expand())
        # GgineqIt
        GgineqIt = MX.zeros(nu+nx+1, ngIneqI)
        GgineqIt[:nu+nx,
                :] = jacobian(ineqI, vertcat(stage.u, stage.x)).T
        GgineqIt[nu+nx, :] = ineqI[:].T
        self.codegen.add(Function("GgineqIt", [stage.u,
              stage.x, self.stage_params_sym, self.global_params_sym], [densify(GgineqIt)]).expand())
        self.codegen.add(Function("gineqI", [stage.u, stage.x, self.stage_params_sym, self.global_params_sym], [
              densify(ineqI[:])]).expand())
        # Ggineqt
        Ggineqt = MX.zeros(nu+nx+1, ngIneq)
        Ggineqt[:nu+nx,
                :] = jacobian(ineq, vertcat(stage.u, stage.x)).T
        Ggineqt[nu+nx, :] = ineq[:].T
        self.codegen.add(Function("Ggineqt", [stage.u,
              stage.x, self.stage_params_sym, self.global_params_sym], [densify(Ggineqt)]).expand())
        self.codegen.add(Function("gineq", [stage.u, stage.x, self.stage_params_sym, self.global_params_sym], [
              densify(ineq[:])]).expand())
        # GgineqFt
        GgineqFt = MX.zeros(nx+1, ngIneqF)
        GgineqFt[:nx,
                :] = jacobian(ineqF, vertcat(stage.x)).T
        GgineqFt[nx, :] = ineqF[:].T
        self.codegen.add(Function("GgineqFt", [
              stage.x, self.stage_params_sym, self.global_params_sym], [densify(GgineqFt)]).expand())
        self.codegen.add(Function("gineqF", [stage.x, self.stage_params_sym, self.global_params_sym], [
              densify(ineqF[:])]).expand())
        
        # codegenerate samplers
        for sampl in self.samplers.keys():
            self.codegen.add(Function("sampler_"+ str(sampl), [stage.u, stage.x, self.stage_params_sym, self.global_params_sym], [densify(self.samplers[sampl])]).expand())


        self.build_dir_abs = self.build_dir_abs
        prepare_build_dir(self.build_dir_abs)

        self.codegen.generate(self.build_dir_abs+os.sep)
        def get_sym_name(symbol):
            # return symbol.name() if bool(symbol not in self.variable_names) else self.variable_names[symbol]
            return symbol.name()

        # creating the json file for fatrop
        control_params_sym = stage.parameters['control'] + stage.parameters['control+']
        global_params_sym = stage.parameters['']
        control_params_offset = {get_sym_name(sym):get_offsets(vec(sym), vertcat(*control_params_sym)) for sym in control_params_sym}
        global_params_offset = {get_sym_name(sym):get_offsets(vec(sym), vertcat(*global_params_sym)) for sym in global_params_sym}
        states_sym = [vec(state) for state in  stage.states]
        states_offset = {get_sym_name(sym):get_offsets(vec(sym), vertcat(*states_sym)) for sym in stage.states}
        controls_sym = [vec(control) for control in  stage.controls]
        controls_offset = {get_sym_name(sym):get_offsets(vec(sym), vertcat(*controls_sym)) for sym in stage.controls}



        json_dict = {
                        'control_params_offset': control_params_offset,
                        'global_params_offset': global_params_offset,
                        'states_offset': states_offset,
                        'controls_offset': controls_offset,
                        'nx': stage.nx,
                        'nu': stage.nu,
                        'ngI': eqI.shape[0],
                        'ng': ng,
                        'ngF': eqF.shape[0],
                        'ng_ineqI': ngIneqI,
                        'ng_ineq': ngIneq,
                        'ng_ineqF': ineqF.shape[0],
                        'n_stage_params': self.stage_params_sym.shape[0],
                        'n_global_params': self.global_params_sym.shape[0],
                        'global_params': global_params_value.T.full().flatten().tolist(), #TODO
                        'stage_params' : stage_params_value.T.full().flatten().tolist(), #TODO
                        'params': [], #TODO
                        'K': self.N+1,
                        'initial_x': X0.T.full().flatten().tolist(),
                        'initial_u': U0.T.full().flatten().tolist(),
                        'lower': cs.repmat(evalf(lb_mid), (self.N-1, 1)).full().flatten().tolist(),
                        'upper': cs.repmat(evalf(ub_mid), (self.N-1, 1)).full().flatten().tolist(),
                        'lowerI': evalf(lb_init).full().flatten().tolist(),
                        'upperI': evalf(ub_init).full().flatten().tolist(),                                               
                        'lowerF': evalf(lb_term).full().flatten().tolist(),
                        'upperF': evalf(ub_term).full().flatten().tolist(),
                        'samplers': list(self.samplers.keys())
                    }
        

        import json
        with open(self.build_dir_abs + os.sep + 'casadi_codegen.json', 'w') as fp:
            json.dump(json_dict, fp, indent = 4)




        functions = str("./" + self.build_dir_abs + "/casadi_codegen.so")
        functions_c = str("./" + self.build_dir_abs + "/casadi_codegen.c")
        json_spec = str("./" + self.build_dir_abs + "/casadi_codegen.json")

        subprocess.run("gcc -fPIC -march=native -shared -Ofast " + functions_c + " -o " + functions, shell = True)
        # subprocess.run("gcc -fPIC -O0 -shared ./foobar/casadi_codegen.c -o ./foobar/casadi_codegen.so", shell = True)
        # subprocess.run("gcc -fPIC -march=native -shared -Ofast ./foobar/casadi_codegen.c -o ./foobar/casadi_codegen.so", shell = True)
        # print(functions)
        # print(json_spec)
        self.myOCP = fatropy.OCP(functions,json_spec)
        # print("FATROP CODE IS GERNERATED BUT FATROP CANNOT BE CALLED FROM ROCKIT YET")
        return


    def to_function(self, stage, name, args, results, *margs):
        print("args=",args)

        res = self.solver(p=stage.p)
        print(stage.p)
        print([stage.value(a) for a in args])


        [_,states] = stage.sample(stage.x,grid='control')
        [_,controls] = stage.sample(stage.u,grid='control-')
        variables = stage.value(vvcat(stage.variables['']))

        helper_in = [states,controls,variables, stage.T]
        helper = Function("helper", helper_in, results)

        arg_in = helper(res["x_opt"],res["u_opt"],res["v_opt"],res["T_opt"])

        ret = Function(name, args, arg_in, *margs)
        assert not ret.has_free()
        return ret

    def initial_value(self, stage, expr):
        ret = self.pmap(p=self.P0)
        parameters = []
        for p in stage.parameters['']:
            parameters.append(stage.value(p))
        
        [_,states] = stage.sample(stage.x,grid='control')
        [_,controls] = stage.sample(stage.u,grid='control-')
        variables = stage.value(vvcat(stage.variables['']))

        helper_in = [vvcat(parameters),states,controls,variables, stage.T]
        helper = Function("helper", helper_in, [expr])
        return helper(self.P0, cs.repmat(ret["x_current"], 1, self.N+1), cs.repmat(self.U0, 1, self.N), self.V0, 0).toarray(simplify=True)

    def solve(self, stage,limited=False):
        # self.global_params_value, self.stage_params_value = self.get_parameters(stage)
        self.myOCP.SetParams(self.stage_params_value.T.full().flatten(), self.global_params_value.T.full().flatten())


        retval = self.myOCP.Optimize()
        u_sol_fatrop = self.myOCP.u_sol
        x_sol_fatrop = self.myOCP.x_sol

        return OcpSolution(SolWrapper(self, vec(x_sol_fatrop), vertcat(vec(u_sol_fatrop), DM.zeros(1)), DM.zeros(0), DM.zeros(0), rT=stage.T), stage)

    def get_stats(self):
        stats = self.stats
        return dict((k,getattr(stats,k)) for k,_ in stats_fields)

    def non_converged_solution(self, stage):
        return self.last_solution

    def solve_limited(self, stage):
        return self.solve(stage,limited=True)

    def eval(self, stage, expr):
        placeholders = stage.placeholders_transcribed
        expr = placeholders(expr,max_phase=1)
        ks = [self.v,stage.T]
        vs = [self.V_gist, self.T_gist]
        ret = substitute([expr],ks,vs)[0]
        return ret
        
    @property
    def gist(self):
        return vertcat(ExternalMethod.gist.fget(self), self.V_gist, self.T_gist)

    def eval_at_control(self, stage, expr, k):
        placeholders = stage.placeholders_transcribed
        expr = placeholders(expr,max_phase=1)
        ks = [stage.x,stage.u,self.v,stage.T]
        vs = [self.X_gist[k], self.U_gist[min(k, self.N-1)], self.V_gist, self.T_gist]
        if not self.t_state:
            ks += [stage.t]
            vs += [self.control_grid[k]]
        ret = substitute([expr],ks,vs)[0]
        return ret

class SolWrapper:
    def __init__(self, method, x, u, v, T, rT=None):
        self.method = method
        self.x = x
        self.u = u
        self.T = T
        self.v = v
        self.rT = rT

    def value(self, expr, *args,**kwargs):
        placeholders = self.method.stage.placeholders_transcribed
        expr = substitute(expr,self.rT, self.T)
        ret = evalf(substitute([placeholders(expr)],[self.method.gist],[vertcat(self.x, self.u, self.v, self.T)])[0])
        return ret.toarray(simplify=True)

    def stats(self):
        return self.method.get_stats()
