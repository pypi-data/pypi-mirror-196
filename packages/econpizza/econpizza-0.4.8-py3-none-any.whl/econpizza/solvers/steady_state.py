# -*- coding: utf-8 -*-

import jax
import time
import jax.numpy as jnp
from grgrjax import newton_jax, val_and_jacfwd, amax
from ..parser.build_functions import get_func_stst_raw


def solver(jval, fval):
    """A default solver to solve indetermined problems.
    """
    return jnp.linalg.pinv(jval) @ fval


def _get_stst_dist_objs(model, res, maxit_backwards, maxit_forwards):
    """Get the steady state distribution and decision outputs, which is an auxilliary output of the steady state function. Compile error messages if things go wrong.
    """

    res_backw, res_forw = res['aux']
    vfSS, decisions_output, exog_grid_vars, cnt_backwards = res_backw
    distSS, cnt_forwards = res_forw
    decisions_output_names = model['decisions']['outputs']

    # compile informative message
    mess = ''
    if jnp.isnan(jnp.array(vfSS)).any() or jnp.isnan(jnp.array(decisions_output)).any():
        mess += f"Backward iteration returns 'NaN's. "
    elif jnp.isnan(distSS).any():
        mess += f"Forward iteration returns 'NaN's. "
    elif distSS.min() < 0:
        mess += f"Distribution contains negative values ({distSS.min():0.1e}). "
    if cnt_backwards == maxit_backwards:
        mess += f'Maximum of {maxit_backwards} backwards calls reached. '
    if cnt_forwards == maxit_forwards:
        mess += f'Maximum of {maxit_forwards} forwards calls reached. '

    # TODO: this should loop over the objects in distSS/vfSS and store under the name of the distribution/decisions (i.e. 'D' or 'Va')
    model['steady_state']["distributions"] = distSS
    model['steady_state']['value_functions'] = vfSS
    model['steady_state']['decisions'] = {
        oput: decisions_output[i] for i, oput in enumerate(decisions_output_names)}

    return mess


def solve_stst(model, tol=1e-8, maxit=15, tol_backwards=None, maxit_backwards=2000, tol_forwards=None, maxit_forwards=5000, force=False, raise_errors=True, check_rank=False, verbose=True, **newton_kwargs):
    """Solves for the steady state.

    Parameters
    ----------
    model : PizzaModel
        PizzaModel instance
    tol : float, optional
        tolerance of the Newton method, defaults to 1e-8
    maxit : int, optional
        maximum of iterations for the Newton method, defaults to 15
    tol_backwards : float, optional
        tolerance required for backward iteration. Defaults to tol
    maxit_backwards : int, optional
        maximum of iterations for the backward iteration. Defaults to 2000
    tol_forwards : float, optional
        tolerance required for forward iteration. Defaults to tol
    maxit_forwards : int, optional
        maximum of iterations for the forward iteration. Defaults to 5000
    force : bool, optional
        force recalculation of steady state, even if it is already evaluated. Defaults to False
    verbose : bool, optional
        level of verbosity. Defaults to True
    newton_kwargs : keyword arguments
        keyword arguments passed on to the Newton method

    Returns
    -------
    rdict : dict
        a dictionary containing information about the root finding result. Note that the results are added to the model (PizzaModel instance) automatically, `rdict` is hence only useful for model debugging.
    """

    st = time.time()

    evars = model["variables"]
    func_pre_stst = model['context']["func_pre_stst"]
    par = model["parameters"]
    shocks = model.get("shocks") or ()
    fixed_vals = model['steady_state']['fixed_evalued']

    tol_backwards = tol if tol_backwards is None else tol_backwards
    tol_forwards = 1e-2*tol if tol_forwards is None else tol_forwards

    # check if steady state was already calculated
    try:
        cond0 = jnp.allclose(model["stst_used_pars"], jnp.array(
            list(fixed_vals.values())))
        cond1 = model["stst_used_setup"] == (
            model.get('functions_file_plain'), tol, maxit, tol_backwards, maxit_backwards, tol_forwards, maxit_forwards)
        if cond0 and cond1 and not force:
            if verbose:
                print(
                    f"(solve_stst:) Steady state already {'known' if model['stst_used_success'] else 'FAILED'}.")

            return model['stst_used_res']
    except KeyError:
        model['compiled_objects']['compiled_model_flag'] = False
        pass

    # reset for recalculation
    model['stst_jacobian'] = None
    model['stacked_func'] = None

    # get all necessary functions
    func_eqns = model['context']['func_eqns']
    func_backw = model['context'].get('func_backw')
    func_stst_dist = model['context'].get('func_stst_dist')

    # get initial values for heterogenous agents
    decisions_output_init = model['init_run'].get('decisions_output')
    exog_grid_vars_init = model['init_run'].get('exog_grid_vars')
    init_vf = model.get('init_vf')

    # get the actual steady state function
    func_stst_raw = get_func_stst_raw(func_pre_stst, func_backw, func_stst_dist, func_eqns, shocks, init_vf, decisions_output_init,
                                      exog_grid_vars_init, tol_backw=tol_backwards, maxit_backw=maxit_backwards, tol_forw=tol_forwards, maxit_forw=maxit_forwards)

    # define jitted stst function that returns jacobian and func. value
    func_stst = jax.jit(val_and_jacfwd(func_stst_raw, has_aux=True))
    # store functions
    model["context"]['func_stst_raw'] = func_stst_raw
    model["context"]['func_stst'] = func_stst

    # actual root finding
    x_init = jnp.array(list(model['init'].values()))

    res = newton_jax(func_stst, x_init, maxit, tol,
                     solver=solver, verbose=verbose, **newton_kwargs)

    # exchange those values that are identified via stst_equations
    stst_vals, par_vals = func_pre_stst(res['x'])

    model["stst"] = dict(zip(evars, stst_vals))
    model["parameters"] = dict(zip(par, par_vals))

    # calculate dist objects and compile message
    mess = _get_stst_dist_objs(model, res, maxit_backwards,
                               maxit_forwards) if model.get('distributions') else ''
    # calculate error
    err = amax(res['fun'])

    if err > tol or not res['success'] or check_rank:
        jac = res['jac']
        rank = jnp.linalg.matrix_rank(jac)
        if rank:
            nvars = len(evars)+len(par)
            nfixed = len(fixed_vals)
            if rank != nvars - nfixed:
                mess += f"Jacobian has rank {rank} for {nvars - nfixed} degrees of freedom ({nvars} variables/parameters, {nfixed} fixed). "

    # check if any of the fixed variables are neither a parameter nor variable
    if mess:
        not_var_nor_par = list(set(fixed_vals) - set(evars) - set(par))
        mess += f"Fixed value(s) ``{'``, ``'.join(not_var_nor_par)}`` not defined. " if not_var_nor_par else ''

    if err > tol or not res['success']:
        if not res["success"] or raise_errors:
            mess = f"Steady state FAILED (error is {err:1.2e}). {res['message']} {mess}"
        else:
            mess = f"{res['message']} WARNING: Steady state error is {err:1.2e}. {mess}"
        if raise_errors:
            raise Exception(mess)
    elif verbose:
        duration = time.time() - st
        mess = f"Steady state found ({duration:1.5g}s). {res['message']}" + (
            ' WARNING: ' + mess if mess else '')

    # cache everything if search was successful
    model["stst_used_pars"] = jnp.array(
        list(model['steady_state']['fixed_evalued'].values()))
    model["stst_used_setup"] = model.get(
        'functions_file_plain'), tol, maxit, tol_backwards, maxit_backwards, tol_forwards, maxit_forwards
    model["stst_used_res"] = res
    model["stst_used_success"] = res['success']

    if mess:
        print(f"(solve_stst:) {mess}")

    return res
