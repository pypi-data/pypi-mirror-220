import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.widgets import Slider

from starred.utils.generic_utils import Downsample


def single_PSF_plot(model, data, sigma_2, kwargs, n_psf=0, figsize=(15, 8), units=None, upsampling=None):
    """
    Plots the narrow PSF fit for a single observation.

    :param model: array containing the model
    :param data: array containing the observations
    :param sigma_2: array containing the square of the noise maps
    :param kwargs: dictionary containing the parameters of the model
    :param n_psf: selected PSF index
    :type n_psf: int
    :param figsize: tuple that indicates the size of the figure
    :param units: units in which the pixel values are expressed
    :type units: str
    :param upsampling_factor: Provide the upsampling factor to degrade the model to the image resolution. Leave to 'None' to show the higher resolution model.
    :type upsampling_factor: int

    :return: output figure

    """
    if units is not None:
        str_unit = '[' + units + ']'
    else:
        str_unit = ''
    estimated_full_psf = model.model(n_psf, **kwargs)
    analytic = model.get_moffat(kwargs['kwargs_moffat'], norm=True)
    s = model.get_narrow_psf(**kwargs, norm=True)
    background = model.get_background(kwargs['kwargs_background'])

    if upsampling is not None:
        analytic = Downsample(analytic, factor=upsampling)
        s = Downsample(s, factor=upsampling)
        background = Downsample(background, factor=upsampling)

    dif = data[n_psf, :, :] - estimated_full_psf
    rr = dif / np.sqrt(sigma_2[n_psf, :, :])

    fig, axs = plt.subplots(2, 3, figsize=figsize)
    fraction = 0.046
    pad = 0.04
    font_size = 14
    ticks_size = 6

    plt.rc('font', size=font_size)
    axs[0, 0].set_title('Data %s' % str_unit, fontsize=font_size)
    axs[0, 0].tick_params(axis='both', which='major', labelsize=ticks_size)
    axs[0, 1].set_title('PSF model %s' % str_unit, fontsize=font_size)
    axs[0, 1].tick_params(axis='both', which='major', labelsize=ticks_size)
    axs[0, 2].set_title('Map of relative residuals', fontsize=font_size)
    axs[0, 2].tick_params(axis='both', which='major', labelsize=ticks_size)
    axs[1, 0].set_title('Moffat', fontsize=font_size)
    axs[1, 0].tick_params(axis='both', which='major', labelsize=ticks_size)
    axs[1, 1].set_title('Grid of pixels', fontsize=font_size)
    axs[1, 1].tick_params(axis='both', which='major', labelsize=ticks_size)
    axs[1, 2].set_title('Narrow PSF', fontsize=font_size)
    axs[1, 2].tick_params(axis='both', which='major', labelsize=ticks_size)

    fig.colorbar(axs[0, 0].imshow(data[n_psf, :, :], norm=colors.SymLogNorm(linthresh=100), origin='lower'),
                 ax=axs[0, 0], fraction=fraction, pad=pad, format='%.0e')
    fig.colorbar(axs[0, 1].imshow(estimated_full_psf, norm=colors.SymLogNorm(linthresh=100), origin='lower'),
                 ax=axs[0, 1], fraction=fraction, pad=pad, format='%.0e')
    fig.colorbar(axs[0, 2].imshow(rr, origin='lower'), ax=axs[0, 2], fraction=fraction, pad=pad)
    fig.colorbar(axs[1, 0].imshow(analytic, norm=colors.SymLogNorm(linthresh=1e-2), origin='lower'), ax=axs[1, 0],
                 fraction=fraction,
                 pad=pad)
    fig.colorbar(axs[1, 1].imshow(background, origin='lower'), ax=axs[1, 1], fraction=fraction,
                 pad=pad)
    fig.colorbar(axs[1, 2].imshow(s, norm=colors.SymLogNorm(linthresh=1e-3), origin='lower'), ax=axs[1, 2],
                 fraction=fraction, pad=pad)

    for ax in np.array(axs).flatten():
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

    plt.tight_layout()

    return fig


def multiple_PSF_plot(model, data, sigma_2, kwargs, masks=None, figsize=None, units=None):
    """
    Plots the narrow PSF fit for all observations.

    :param model: array containing the model
    :param data: array containing the observations
    :param sigma_2: array containing the square of the noise maps
    :param kwargs: dictionary containing the parameters of the model
    :param masks:  array containing the masks
    :param figsize: tuple that indicates the size of the figure
    :param units: units in which the pixel values are expressed
    :type units: str

    :return: output figure
    """
    if units is not None:
        str_unit = '[' + units + ']'
    else:
        str_unit = ''

    if figsize is None:
        nimage,nx,ny = np.shape(data)
        figsize = (12+nimage*2, 10)
    fig, axs = plt.subplots(2, model.M, figsize=figsize)
    plt.subplots_adjust(wspace=0.3)
    if model.M == 1:
        axs = np.asarray([axs]).T
    fraction = 0.046
    pad = 0.04
    font_size = 14
    plt.rc('font', size=12)
    fmt_PSF = '%.0e'
    fmt_residuals = '%2.f'

    if masks is not None:
        alphas = masks
        ind = np.where(masks == 0)
        alphas[ind] = 0.01
        kargs = [{'alpha':alphas[i,:,:]} for i in range(model.M)]
    else:
        kargs = [{} for i in range(model.M)]

    for i in range(model.M):
        estimated_full_psf = model.model(i, **kwargs)
        axs[0, i].set_title('PSF model %i %s' % (i + 1, str_unit), fontsize=font_size)
        axs[0, i].tick_params(axis='both', which='major', labelsize=10)
        axs[1, i].set_title('Relative residuals %i' % (i + 1), fontsize=font_size)
        axs[1, i].tick_params(axis='both', which='major', labelsize=10)

        fig.colorbar(axs[0, i].imshow(estimated_full_psf, norm=colors.SymLogNorm(linthresh=100), origin='lower'),
                     ax=axs[0, i], fraction=fraction, pad=pad, format=fmt_PSF)
        fig.colorbar(axs[1, i].imshow((data[i, :, :] - estimated_full_psf) / np.sqrt(sigma_2[i, :, :]),
                                      origin='lower', **kargs[i]), ax=axs[1, i], fraction=fraction, pad=pad, format=fmt_residuals)

    for ax in np.array(axs).flatten():
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

    return fig


def display_data(data, sigma_2=None, masks=None, figsize=None, units=None, center=None):
    """
    Plots the observations and the noise maps.

    :param data: array containing the observations
    :param sigma_2: array containing the square of the noise maps
    :param figsize: tuple that indicates the size of the figure
    :param units: units in which the pixel values are expressed
    :type units: str
    :param center: x and y coordinates of the centers of the observations

    :return: output figure
    """
    if sigma_2 is None:
        row = 1
        show_sigma = False
    else:
        row = 2
        show_sigma = True

    if figsize is None:
        nimage,nx,ny = np.shape(data)
        figsize = (12+nimage*2, 10)

    if units is not None:
        str_unit = '[' + units + ']'
    else:
        str_unit = ''

    n_image, nx, ny = np.shape(np.asarray(data))
    fig, axs = plt.subplots(row, n_image, figsize=figsize)
    plt.subplots_adjust(wspace=0.3)
    if row == 1 and n_image == 1:
        axs = [[axs]]
    elif row == 1:
        axs = [axs]
    elif n_image == 1:
        axs = np.asarray([axs]).T
    fraction = 0.046
    pad = 0.04
    fontsize = 12

    if masks is not None:
        alphas = masks
        ind = np.where(masks == 0)
        alphas[ind] = 0.9
        kargs = [{'alpha':alphas[i,:,:]} for i in range(n_image)]
    else:
        kargs = [{} for i in range(n_image)]

    for i in range(n_image):
        plt.rc('font', size=12)
        axs[0][i].set_title('Data %i %s' % (i + 1, str_unit), fontsize=fontsize)
        axs[0][i].tick_params(axis='both', which='major', labelsize=10)

        if show_sigma:
            axs[1][i].set_title('Noise map %i %s' % (i + 1, str_unit), fontsize=fontsize)
            axs[1][i].tick_params(axis='both', which='major', labelsize=10)

        fig.colorbar(axs[0][i].imshow(data[i, :, :], norm=colors.SymLogNorm(linthresh=10), origin='lower',  **kargs[i]),
                     ax=axs[0][i],
                     fraction=fraction, pad=pad, format='%.0e')
        if center is not None:
            c_x, c_y = center[0], center[1]
            axs[0][i].scatter(nx/2. + c_x[i], ny/2. + c_y[i], marker='x', c='r')

        if show_sigma:
            fig.colorbar(
                axs[1][i].imshow(np.sqrt(sigma_2[i, :, :]), norm=colors.SymLogNorm(linthresh=10), origin='lower', **kargs[i]),
                ax=axs[1][i],
                fraction=fraction, pad=pad, format='%2.f')

    for ax in axs.flatten():
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    plt.tight_layout()

    return fig

def dict_to_kwargs_list(dict):
        """
        Transform dictionnary into a list kwargs. All entry must have the same lenght.

        :param
        """
        k_list = []
        keys = list(dict.keys())
        for i in range(len(dict[keys[0]])):
            k_list.append({})
            for key in keys:
                k_list[i][key]=dict[key][i]

        return k_list
    
def plot_deconvolution(model, data, sigma_2, s, kwargs, epoch = 0, units=None, figsize=(15, 10), cut_dict=None):
    """
    Plots the results of the deconvolution.

    :param data: array containing the observations. Has shape (n_epoch, n_pixel, n_pixel).
    :param sigma_2: array containing the square of the noise maps (n_epoch, n_pixel, n_pixel).
    :param s: array containing the narrow PSF (n_epoch, n_pixel*susampling factor, n_pixel*susampling factor).
    :param epoch: index of the epoch to plot
    :param kwargs: dictionary containing the parameters of the model
    :type epoch: int
    :param figsize: tuple that indicates the size of the figure
    :param units: units in which the pixel values are expressed
    :type units: str

    :return: output figure
    """

    if units is not None:
        str_unit = '[' + units + ']'
    else:
        str_unit = ''

    if cut_dict is None :
        #Default setting
        cut_dict = {
            'linthresh':[5e2,5e2,None,5e1,5e1,1e-3],
            'vmin':[None, None, None, None, None, None],
            'vmax':[None, None, None, None, None, None],
        }

    k_dict = dict_to_kwargs_list(cut_dict)
    output = model.model(kwargs)[epoch]
    deconv, h = model.getDeconvolved(kwargs, epoch)
    data_show = data[epoch, :, :]

    dif = data_show - output
    rr = np.abs(dif) / np.sqrt(sigma_2[epoch, :, :])

    fig, axs = plt.subplots(2, 3, figsize=(15, 8))
    fraction = 0.046
    pad = 0.04
    font_size = 10
    ticks_size = 6

    plt.rc('font', size=font_size)
    axs[0, 0].set_title(f'Data {str_unit}', fontsize=8)
    axs[0, 0].tick_params(axis='both', which='major', labelsize=ticks_size)
    axs[0, 1].set_title(f'Convolving back {str_unit}', fontsize=8)
    axs[0, 1].tick_params(axis='both', which='major', labelsize=ticks_size)
    axs[0, 2].set_title('Map of relative residuals', fontsize=8)
    axs[0, 2].tick_params(axis='both', which='major', labelsize=ticks_size)
    axs[1, 0].set_title(f'Background {str_unit}', fontsize=8)
    axs[1, 0].tick_params(axis='both', which='major', labelsize=ticks_size)
    axs[1, 1].set_title(f'Deconvolved image {str_unit}', fontsize=8)
    axs[1, 1].tick_params(axis='both', which='major', labelsize=ticks_size)
    axs[1, 2].set_title('Narrow PSF', fontsize=8)
    axs[1, 2].tick_params(axis='both', which='major', labelsize=ticks_size)

    fig.colorbar(axs[0, 0].imshow(data_show, norm=colors.SymLogNorm(**k_dict[0]), origin='lower'), ax=axs[0, 0], fraction=fraction, pad=pad)
    fig.colorbar(axs[0, 1].imshow(output, norm=colors.SymLogNorm(**k_dict[1]), origin='lower'), ax=axs[0, 1], fraction=fraction,pad=pad)
    if 'linthresh' in k_dict[2].keys():
        del k_dict[2]['linthresh']
    fig.colorbar(axs[0, 2].imshow(rr, origin='lower', **k_dict[2]), ax=axs[0, 2], fraction=fraction, pad=pad)
    fig.colorbar(axs[1, 0].imshow(h, norm=colors.SymLogNorm(**k_dict[3]), origin='lower'), ax=axs[1, 0], fraction=fraction,pad=pad)
    fig.colorbar(axs[1, 1].imshow(deconv, norm=colors.SymLogNorm(**k_dict[4]), origin='lower'), ax=axs[1, 1],fraction=fraction, pad=pad)
    fig.colorbar(axs[1, 2].imshow(s[epoch, :, :], norm=colors.SymLogNorm(**k_dict[5]), origin='lower'), ax=axs[1, 2],fraction=fraction, pad=pad)

    return fig

def view_deconv_model(model, kwargs, data, sigma_2, figsize=(9,7.5)):
    output = model.model(kwargs)
    psf = model.psf
    noisemap = sigma_2 ** 0.5

    # setup for first epoch
    deconvs = [model.getDeconvolved(kwargs, i) for i in range(len(output))]
    deconv, h = deconvs[0]
    s = psf[0]

    ##########################################################################
    # figure
    fig, axs = plt.subplots(2, 3, figsize=figsize)
    for ax in axs.flatten():
        ax.set_xticks([])
        ax.set_yticks([])

    datap = axs[0, 0].imshow(data[0], origin='lower')
    axs[0, 0].set_title('data')

    modelp = axs[0, 1].imshow(output[0], origin='lower')
    axs[0, 1].set_title('model')

    diffp = axs[1, 0].imshow((data[0] - output[0]) / noisemap[0], origin='lower')
    axs[1, 0].set_title('(data-model)/noise')

    backp = axs[1, 1].imshow(h, origin='lower')
    axs[1, 1].set_title('background')

    decp = axs[0, 2].imshow(deconv, origin='lower')
    axs[0, 2].set_title('deconvolved')

    psfp = axs[1, 2].imshow(s, origin='lower')
    axs[1, 2].set_title('narrow psf')

    plt.tight_layout()

    if len(output)>1:
        axcolor   = 'lightgoldenrodyellow'
        axslider  = plt.axes([0.1, 0.05, 0.75, 0.01], facecolor=axcolor)
        slider    = Slider(axslider, 'Epoch', 0, len(output)-1, valinit=0, valstep=1)
        #######################################################################
        # functions for slider update, only if more than one epoch.
        def press(event): #pragma: no cover
            try:
                button = event.button
            except:
                button = 'None'
            if event.key == 'right' or button == 'down':
                if slider.val < len(output) - 1:
                    slider.set_val(slider.val + 1)
            elif event.key == 'left' or button == 'up':
                if slider.val > 0:
                    slider.set_val(slider.val - 1)
            update(slider.val)
            fig.canvas.draw_idle()
        
        def reset(event):#pragma: no cover
            slider.reset()
            
        def update(val):#pragma: no cover
            epoch0 = int(slider.val)
            deconv, h = deconvs[epoch0]
            s = psf[epoch0]
            # update all the plots
            datap.set_data(data[epoch0])
            modelp.set_data(output[epoch0])
            diffp.set_data((data[epoch0] - output[epoch0])/noisemap[epoch0])
            backp.set_data(h)
            decp.set_data(deconv)
            psfp.set_data(s)
            
    
        fig.canvas.mpl_connect('key_press_event', press)
        fig.canvas.mpl_connect('scroll_event', press)
        slider.on_changed(update)
    
    plt.show(block=False)

def make_movie(model, kwargs, data, sigma_2, outpath, figsize=(9,7.5), epochs_list=None, duration=20, loop=1, format='gif'):
    output = model.model(kwargs)
    psf = model.psf
    noisemap = sigma_2 ** 0.5

    if epochs_list is None:
        epochs_list = range(len(output))

    # setup for first epoch
    deconvs = [model.getDeconvolved(kwargs, i) for i in range(len(output))]
    deconv, h = deconvs[0]
    s = psf[0]

    ##########################################################################
    # figure
    fig, axs = plt.subplots(2, 3, figsize=figsize)
    for ax in axs.flatten():
        ax.set_xticks([])
        ax.set_yticks([])

    datap = axs[0, 0].imshow(data[0], origin='lower')
    axs[0, 0].set_title('data')

    modelp = axs[0, 1].imshow(output[0], origin='lower')
    axs[0, 1].set_title('model')

    diffp = axs[1, 0].imshow((data[0] - output[0]) / noisemap[0], origin='lower')
    axs[1, 0].set_title('(data-model)/noise')

    backp = axs[1, 1].imshow(h, origin='lower')
    axs[1, 1].set_title('background')

    decp = axs[0, 2].imshow(deconv, origin='lower')
    axs[0, 2].set_title('deconvolved')

    psfp = axs[1, 2].imshow(s, origin='lower')
    axs[1, 2].set_title('narrow psf')

    plt.tight_layout()

    # update all the plots
    files = []
    for i, epoch0 in enumerate(epochs_list):
        deconv, h = deconvs[epoch0]
        s = psf[epoch0]
        datap.set_data(data[epoch0])
        modelp.set_data(output[epoch0])
        diffp.set_data((data[epoch0] - output[epoch0]) / noisemap[epoch0])
        backp.set_data(h)
        decp.set_data(deconv)
        psfp.set_data(s)

        file_png = os.path.join(outpath, "frame{0:05d}.png".format(i))
        fig.savefig(file_png)
        files.append(file_png)

    if format == 'gif':
        gif_name = os.path.join(outpath, "deconv.gif")
        make_gif(files, gif_name, duration=duration, loop=loop)
    elif format in ['FMP4', 'mp4v']:
        video_name = os.path.join(outpath, 'deconv.mp4')
        fps = duration / len(files)
        make_video(files, outvid=video_name, fps=fps, size=None,
                   is_color=True, format=format)
    else:
        RuntimeError('Unsupported video format. Use "gif" or "FMP4".')


def make_gif(list_files, output_path, duration=100, loop= 1):
    try:
        from PIL import Image
    except ImportError as e:
        print(e)
        print('Python package PIL is required for gif creation.')
    frames = [Image.open(image) for image in list_files]
    frame_one = frames[0]
    frame_one.save(output_path, format="GIF", append_images=frames,
               save_all=True, duration=duration)

def make_video(images, outvid=None, fps=5, size=None,
               is_color=True, format="XVID"):
    """
    Create a video from a list of images.

    @param      outvid      output video
    @param      images      list of images to use in the video
    @param      fps         frame per second
    @param      size        size of each frame
    @param      is_color    color
    @param      format      see http://www.fourcc.org/codecs.php
    @return                 see http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

    The function relies on http://opencv-python-tutroals.readthedocs.org/en/latest/.
    By default, the video will have the size of the first image.
    It will resize every image to this size before adding them to the video.
    """
    try:
        from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
    except ImportError as e:
        print(e)
        print('Python package opencv-python is required for video creation.')
        exit()

    fourcc = VideoWriter_fourcc(*format)
    vid = None
    for image in images:
        if not os.path.exists(image):
            raise FileNotFoundError(image)
        img = imread(image)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = VideoWriter(outvid, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = resize(img, size)
        vid.write(img)
    vid.release()
    return vid

def plot_loss(loss_history, figsize = (10,5),  ax = None, title = None):
    if ax is None:
        fig, ax = plt.subplots(1,1, figsize =figsize)
    ax.plot(range(len(loss_history)), loss_history)
    ax.set_xlabel('Steps')
    ax.set_ylabel('Loss')
    ax.set_yscale('log')

    if title is not None: 
        ax.set_title(title)

    return fig 
