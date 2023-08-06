from copy import deepcopy

import jax.numpy as jnp
import numpy as np
from scipy.optimize import Bounds

__all__ = ['Parameters']


class Parameters(object):
    """
    Parameters class.

    """

    def __init__(self, image_class, kwargs_init, kwargs_fixed, kwargs_up=None, kwargs_down=None):
        """
        :param image_class: image class 
        :param kwargs_init: dictionary with information on the initial values of the parameters 
        :param kwargs_fixed: dictionary containing the fixed parameters 
        :param kwargs_up: dictionary with information on the upper bounds of the parameters 
        :param kwargs_down: dictionary with information on the lower bounds of the parameters 

        """
        self._image = image_class
        self._kwargs_init = kwargs_init
        self._kwargs_fixed = kwargs_fixed
        self._kwargs_up = kwargs_up
        self._kwargs_down = kwargs_down
        self._kwargs_free_indices = self.get_nan_indices()
        self._update_arrays()

    @property
    def optimized(self):
        """Checks whether a function is optimized."""
        return hasattr(self, '_map_values')

    def initial_values(self, as_kwargs=False, copy=False):
        """Returns the initial values of the parameters."""
        if as_kwargs:
            return deepcopy(self._kwargs_init) if copy else self._kwargs_init
        else:
            return deepcopy(self._init_values) if copy else self._init_values

    def current_values(self, as_kwargs=False, restart=False, copy=False):
        """Returns the current values of the parameters."""
        if restart is True or not self.optimized:
            return self.initial_values(as_kwargs=as_kwargs, copy=copy)
        return self.best_fit_values(as_kwargs=as_kwargs, copy=copy)

    def best_fit_values(self, as_kwargs=False, copy=False):
        """Maximum-a-postriori estimate."""
        if as_kwargs:
            return deepcopy(self._kwargs_map) if copy else self._kwargs_map
        else:
            return deepcopy(self._map_values) if copy else self._map_values

    def set_best_fit(self, args):
        """Sets the maximum-a-postriori estimate as the parameter values."""
        self._map_values = args
        self._kwargs_map = self.args2kwargs(self._map_values)

    def _update_arrays(self):
        self._init_values = self.kwargs2args(self._kwargs_init)
        self._kwargs_init = self.args2kwargs(self._init_values)  # for updating missing fields
        self._num_params = len(self._init_values)
        if self.optimized:
            self._map_values = self.kwargs2args(self._kwargs_map)

    def _set_params(self, kwargs, kwargs_key):
        """Setting the parameters."""
        args = []
        kwargs_profile = kwargs[kwargs_key]
        kwargs_fixed_k = self._kwargs_fixed[kwargs_key]
        param_names = self.get_param_names_for_model(kwargs_key)
        for name in param_names:
            if not name in kwargs_fixed_k and name != 'lambda':
                if isinstance(kwargs_profile[name], list):
                    args += kwargs_profile[name]
                elif isinstance(kwargs_profile[name], (np.ndarray, np.generic)):
                    args += kwargs_profile[name].tolist()
                elif isinstance(kwargs_profile[name], (jnp.ndarray, jnp.generic)):
                    args += kwargs_profile[name].tolist()
                else:
                    args += [kwargs_profile[name]]
            else:
                #add the indices in the self._kwargs_free_indices
                free_ind = self._kwargs_free_indices[kwargs_key][name]
                if len(free_ind)>=1:
                    args += kwargs_profile[name][free_ind].tolist()
        return args

    def get_bounds(self):
        """Returns the upper and lower bounds of the parameters."""
        if self._kwargs_up is None or self._kwargs_down is None:
            return None
        else:
            list_down_limit = []
            list_up_limit = []
            for kwargs_key in self._kwargs_down.keys():
                param_names = self.get_param_names_for_model(kwargs_key)
                for name in param_names:
                    if not name in self._kwargs_fixed[kwargs_key].keys():
                        assert name in self._kwargs_up[kwargs_key].keys(), \
                            "Missing '%s' key in the kwargs_up['%s']" % (name, kwargs_key)
                        assert name in self._kwargs_down[
                            kwargs_key].keys(), "Missing '%s' key in the kwargs_down['%s']" % (name, kwargs_key)
                        up = self._kwargs_up[kwargs_key][name]
                        down = self._kwargs_down[kwargs_key][name]
                        if isinstance(down, list):
                            list_down_limit += down
                        else:
                            list_down_limit += [self._kwargs_down[kwargs_key][name]]
                        if isinstance(up, list):
                            list_up_limit += up
                        else:
                            list_up_limit += [self._kwargs_up[kwargs_key][name]]

            return (jnp.array(list_down_limit).flatten(),
                          jnp.array(list_up_limit).flatten())

    def update_kwargs(self, kwargs_init=None, kwargs_fixed=None, kwargs_up=None,
                      kwargs_down=None):

        """Updates the kwargs with provided values."""
        if kwargs_init is not None:
            self._kwargs_init = kwargs_init
        if kwargs_fixed is not None:
            self._kwargs_fixed = kwargs_fixed
            self._kwargs_free_indices = self.get_nan_indices()
        if kwargs_init is not None:
            self._kwargs_up = kwargs_up
        if kwargs_init is not None:
            self._kwargs_down = kwargs_down

    def _param_names(self, kwargs, kwargs_key):
        """Setting the parameters."""
        names = []
        kwargs_profile = kwargs[kwargs_key]
        kwargs_fixed_k = self._kwargs_fixed[kwargs_key]
        param_names = self.get_param_names_for_model(kwargs_key)
        for name in param_names:
            if not name in kwargs_fixed_k and name != 'lambda':
                if isinstance(kwargs_profile[name], list):
                    if len(kwargs_profile[name]) == 1:
                        names += [name]
                    else:
                        names += [name + '_%i'%i for i in range(len(kwargs_profile[name]))]
                elif isinstance(kwargs_profile[name], (np.ndarray, np.generic)) or isinstance(kwargs_profile[name], (jnp.ndarray, jnp.generic)) :
                    if len(kwargs_profile[name]) == 1:
                        names += [name]
                    else:
                        names += [name + '_%i'%i for i in range(len(kwargs_profile[name].tolist()))]
                else:
                    names += [name]
            else:
                num_free_param = len(self._kwargs_free_indices[kwargs_key][name])
                if num_free_param == 1:
                    names += [name + '_%i'%self._kwargs_free_indices[kwargs_key][name]]
                elif num_free_param > 1:
                    names += [name + '_%i'%x for i,x in enumerate(self._kwargs_free_indices[kwargs_key][name])]
        return names

    def get_nan_indices(self):
        kwargs_indice_free = {}
        for kwargs_key in self._kwargs_fixed.keys():
            kwargs_indice_free[kwargs_key]={}
            for key in self._kwargs_fixed[kwargs_key]:
                indices = jnp.where(jnp.isnan(self._kwargs_fixed[kwargs_key][key]))[0]
                kwargs_indice_free[kwargs_key][key] = indices

        return kwargs_indice_free


