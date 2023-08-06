import warnings
from functools import partial

import jax.numpy as jnp
import numpy as np
from jax import jit
from utils.jax_utils import decompose, scale_norms


class Loss(object):
    """
    Class that manages the (auto-differentiable) loss function, defined as:
    L = - log(likelihood) - log(regularization) - log(positivity) - log(prior)

    Note that gradient, hessian, etc. are computed in the ``InferenceBase`` class.

    """

    _supported_ll = ('l2_norm')
    _supported_regul_source = ('l1_starlet')

    def __init__(self, data, deconv_class, param_class, sigma_2,
                 regularization_terms=None, regularization_strength_scales=None, regularization_strength_hf=None,
                 regularization_strength_positivity=0., regularization_strength_positivity_ps=0., W=None,
                 regularize_full_model = False, regularize_pts_source = False, prior=None):
        """
        :param data: array containing the observations
        :param deconv_class: deconvolution class from ``starred.deconvolution.deconvolution``
        :param param_class: parameters class from ``starred.deconvolution.parameters``
        :param sigma_2: array containing the square of the noise maps
        :param N: number of observations stamps
        :type N: int
        :param regularization_terms: information about the regularization terms
        :type regularization_terms: str
        :param regularization_strength_scales: Lagrange parameter that weights intermediate scales in the transformed domain 
        :type regularization_strength_scales: float
        :param regularization_strength_hf: Lagrange parameter weighting the highest frequency scale
        :type regularization_strength_hf: float
        :param regularization_strength_positivity: Lagrange parameter weighting the positivity of the background. 0 means no positivity constrain.
        :type regularization_strength_positivity: float
        :param regularization_strength_positivity_ps: Lagrange parameter weighting the positivity of the point sources. 0 means no positivity constrain.
        :type regularization_strength_positivity: float
        :param W: weight matrix. Shape (n_scale, n_pix*subsampling_factor, n_pix*subsampling_factor)
        :type W: jax.numpy.array
        :param regularize_full_model: option to regularise just the background (False) or background + point source channel (True)
        :type regularize_full_model: bool
        :param regularize_pts_source: option to regularise the point source channel
        :type regularize_pts_source: bool
        :param prior: Prior class containing Gaussian prior on the free parameters
        :type prior: Prior class

        """
        self._data = data
        self._sigma_2 = sigma_2
        self.W = W
        self._deconv = deconv_class
        self._datar = self._data.reshape(self._deconv.epochs,
                                         self._deconv.image_size,
                                         self._deconv.image_size)
        self._sigma_2r = self._sigma_2.reshape(self._deconv.epochs,
                                               self._deconv.image_size,
                                               self._deconv.image_size)

        self._param = param_class
        self.epochs = self._deconv.epochs
        self.regularize_full_model = regularize_full_model
        self.regularize_pts_source = regularize_pts_source
        self.prior = prior
        self._init_likelihood()
        self._init_prior()
        self._init_regularizations(regularization_terms, regularization_strength_scales, regularization_strength_hf,
                                   regularization_strength_positivity, regularization_strength_positivity_ps)

    # @partial(jit, static_argnums=(0,))
    def __call__(self, args):
        return self.loss(args)

    def loss(self, args):
        """Defined as the negative log(likelihood*regularization)."""
        kwargs = self._param.args2kwargs(args)
        neg_log = - self._log_likelihood(kwargs)
        if self._st_src_lambda != 0 or self._st_src_lambda_hf !=0 :
            neg_log -= self._log_regul(kwargs)
        if self._pos_lambda != 0:
            neg_log -= self._log_regul_positivity(kwargs)
        if self._pos_lambda_ps != 0.:
            neg_log -= self._log_regul_positivity_ps(kwargs)
        if self.prior is not None:
            neg_log -= self._log_prior(kwargs)
        if self.regularize_pts_source:
            neg_log -= self._log_regul_pts_source(kwargs)

        return jnp.nan_to_num(neg_log, nan=1e15, posinf=1e15, neginf=1e15)

    @property
    def datar(self):
        """Returns the observations array."""
        return self._datar.astype(dtype=np.float32)

    @property
    def sigma_2r(self):
        """Returns the noise map array."""
        return self._sigma_2r.astype(dtype=np.float32)

    def _init_likelihood(self):
        """Intialization of the data fidelity term of the loss function."""
        self._log_likelihood = self._log_likelihood_chi2

    def _init_prior(self):
        """
        Initialization of the prior likelihood
        """
        if self.prior is None:
            self._log_prior =  lambda x: 0.
        else :
            self._log_prior = self._log_prior_gaussian

    def _init_regularizations(self, regularization_terms, regularization_strength_scales, regularization_strength_hf,
                              regularization_strength_positivity, regularization_strength_positivity_ps):
        """Intialization of the regularization terms of the loss function."""
        regul_func_list = []
        # add the log-regularization function to the list
        regul_func_list.append(getattr(self, '_log_regul_' + regularization_terms))

        if regularization_terms == 'l1_starlet':
            n_pix_src = min(*self.datar[0, :, :].shape) * self._deconv._upsampling_factor
            self.n_scales = int(np.log2(n_pix_src))  # maximum allowed number of scales
            if self.W is None:  # old fashion way
                if regularization_strength_scales != 0 and regularization_strength_hf != 0:
                    warnings.warn('lambda is not normalized. Provide the weight map !')
                wavelet_norms = scale_norms(self.n_scales)[:-1]  # ignore coarsest scale
                self._st_src_norms = jnp.expand_dims(wavelet_norms, (1, 2)) * jnp.ones((n_pix_src, n_pix_src))
            else:
                self._st_src_norms = self.W[:-1]  # ignore the coarsest scale
            self._st_src_lambda = float(regularization_strength_scales)
            self._st_src_lambda_hf = float(regularization_strength_hf)

        # positivity term
        self._pos_lambda = float(regularization_strength_positivity)
        self._pos_lambda_ps = float(regularization_strength_positivity_ps)
        # build the composite function (sum of regularization terms)
        self._log_regul = lambda kw: sum([func(kw) for func in regul_func_list])

    # @partial(jit, static_argnums=(0,))
    def _log_likelihood_chi2(self, kwargs):
        """Computes the data fidelity term of the loss function using the L2 norm."""
        model = self._deconv.model(kwargs)
        return - 0.5 * (1. / self.epochs) * jnp.sum((model - self.datar) ** 2 / self.sigma_2r)

        # return - 0.5 * jnp.sum(jnp.array([jnp.sum(jnp.subtract(self.data[i,:,:], self._deconv.model(i, **kwargs)[0])**2 / self.sigma_2[i,:,:]) for i in range(self.epochs)]))

    # @partial(jit, static_argnums=(0,))
    def _log_regul_l1_starlet(self, kwargs):
        """
        Computes the regularization terms as the sum of:
        
        - the L1 norm of the Starlet transform of the highest frequency scale, and
        - the L1 norm of the Starlet transform of all remaining scales (except the coarsest).
        """
        if self.regularize_full_model:
            toreg, _ = self._deconv.getDeconvolved(kwargs, epoch=0)
        else :
            toreg = kwargs['kwargs_background']['h'].reshape(self._deconv.image_size_up, self._deconv.image_size_up)
        st = decompose(toreg, self.n_scales)[:-1]  # ignore coarsest scale
        st_weighted_l1_hf = jnp.sum(self._st_src_norms[0] * jnp.abs(st[0]))  # first scale (i.e. high frequencies)
        st_weighted_l1 = jnp.sum(self._st_src_norms[1:] * jnp.abs(st[1:]))  # other scales
        tot_l1_reg = - (self._st_src_lambda_hf * st_weighted_l1_hf + self._st_src_lambda * st_weighted_l1)
        return tot_l1_reg / self._deconv._upsampling_factor**2

    def _log_regul_positivity(self, kwargs):
        """
        Computes the posivity constraint term. A penalty is applied if the epoch with the smallest background mean has negative pixels.

        :param kwargs:
        """
        h = jnp.array(kwargs['kwargs_background']['h'])
        sum_pos = -jnp.where(h < 0., h, 0.).sum()
        return - self._pos_lambda * sum_pos

    def _log_regul_positivity_ps(self, kwargs):
        """
        Computes the posivity constraint term for the point sources. A penalty is applied if one of the point sources have negative amplitude.

        :param kwargs:
        """
        fluxes = jnp.array(kwargs['kwargs_analytic']['a'])
        min_amp = jnp.min(fluxes, initial=0.)
        return - self._pos_lambda * jnp.abs(jnp.minimum(0., min_amp))

    def _log_regul_pts_source(self, kwargs):
        """
        Penalty term to the pts source, to compensate for the fact that the pts source channel is not regularized

        :param kwargs:
        """
        pts_source_channel = self._deconv.shifted_gaussians(kwargs['kwargs_analytic']['c_x'],
                                                     kwargs['kwargs_analytic']['c_y'],
                                                     jnp.mean(kwargs['kwargs_analytic']['a']) * jnp.ones_like(kwargs['kwargs_analytic']['a']))

        st = decompose(pts_source_channel, self.n_scales)[:-1]  # ignore coarsest scale
        st_weighted_l1_hf = jnp.sum(self._st_src_norms[0] * jnp.abs(st[0]))  # first scale (i.e. high frequencies)
        st_weighted_l1 = jnp.sum(self._st_src_norms[1:] * jnp.abs(st[1:]))  # other scales
        tot_l1_reg = - (self._st_src_lambda_hf * st_weighted_l1_hf + self._st_src_lambda * st_weighted_l1)

        return tot_l1_reg / self._deconv._upsampling_factor**2



    def _log_prior_gaussian(self, kwargs):
        return self.prior.logL(kwargs)

    def update_weights(self, W):
        """Updates the weight matrix W."""
        self._st_src_norms = W[:-1]
        self.W = W

class Prior(object):
    def __init__(self, prior_analytic=None, prior_background=None):
        """

        :param prior_analytic: list of [param_name, mean, 1-sigma priors]
        :param prior_background: list of [param_name, mean, 1-sigma priors]
        """
        self._prior_analytic, self._prior_background = prior_analytic, prior_background

    def logL(self, kwargs):
        logL = 0
        logL += self._prior_kwargs(kwargs['kwargs_analytic'], self._prior_analytic)
        logL += self._prior_kwargs(kwargs['kwargs_background'], self._prior_background)

        return logL

    @staticmethod
    def _prior_kwargs(kwargs, prior):
        """

        :param kwargs: keyword argument
        :param prior: prior
        :return: logL
        """
        if prior is None:
            return 0
        logL = 0
        for i in range(len(prior)):
            param_name, value, sigma = prior[i]
            model_value = kwargs[param_name]
            dist = (model_value - value) ** 2 / sigma ** 2 / 2
            logL -= np.sum(dist)
        return logL

