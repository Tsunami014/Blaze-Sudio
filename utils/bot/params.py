#each one is just a dictionary

#NOTE that for all of these they do not need all the parameters to be there, it's just that for the
#NORMAL dictionary it is there to show you all the (best) options and provide some needed defaults
#The NORMAL dictionary is the defaults
NORMAL = {'n_ctx': 1024, #The larger the number, the more relevant/lengthy the response
          'n_predict': 128, #The larger the number, the longer the response
          'repeat_penalty': 1.2, #The penalty to repeating the same things
          'repeat_last_n': 10, #The number of tokens back to check for repeats
          'context_erase': 0.5} #who knows

LONG = {'n_ctx': 2048, 
        'n_predict': 256, 
        'repeat_penalty': 2.2, 
        'repeat_last_n': 15}

SUPERLONG = {'n_ctx': 4096, 
             'n_predict': 1024, 
             'repeat_penalty': 2.5, 
             'repeat_last_n': 15}

SUPERDUPERLONG = {'n_ctx': 8192, 
                  'n_predict': 2048, 
                  'repeat_penalty': 2.5, 
                  'repeat_last_n': 15}

LONGEST = {'n_ctx': 99999999999999999, 
      'n_predict': 9999999999, 
      'repeat_penalty': 2.5, 
      'repeat_last_n': 15}

NO_REPEATS = {'n_ctx': 2048,
              'repeat_penalty': 9,
              'repeat_last_n': 100}

NO_REPEATS_EVER = {'n_ctx': 4096,
                   'repeat_penalty': 10,
                   'repeat_last_n': 1000,
                   'context_erase': 0.1}

SUPERCTX = {'n_ctx': 4096,
            'context_erase': 0.1}

SUPERDUPERCTX = {'n_ctx': 8192,
                 'context_erase': 0.1}

from copy import deepcopy
def joinParams(params1, params2):
    """
    Joins two params dictionaries

    Parameters
    ----------
    params1 : dict
        The first parameters to join. If any of these are in the other dictionary they will be replaced with the ones from the other.
    params2 : dict
        The second parameters to join to the first ones. These will all be in the resulting dictionary as they are.

    Returns
    -------
    dict
        The dictionary of parameters that has all the params from the second and all others from the first.
    """    
    d = deepcopy(params1)
    d.update(params2)
    return d

def halfParams(params1):
    """
    Halves a dictionary of parameters (makes each parameter half of the way closer to the defaults).

    Parameters
    ----------
    params1 : dict
        The parameters to halve.

    Returns
    -------
    dict
        The resulting dictionary of parameters, each param half of the way closer to the default
    """    
    d = {}
    for i in params1:
        try:
            d[i] = (params1[i] - NORMAL[i]) / 2 + (params1[i] - NORMAL[i])
        except ZeroDivisionError:
            d[i] = params1[i]
    return d
