# Author: Etienne de Montalivet <etienne.demontalivet@protonmail.com>
# License: BSD 3 clause

"""Specific metrics used for forecasting epilepsy"""

import math
from datetime import timedelta
from typing import Union

import numpy as np
import pandas as pd
import warnings


# pylint: disable=missing-raises-doc,too-many-locals
def compute_ioc(
    y_true: pd.Series,
    y_pred: pd.Series,
    threshold: float,
    epoch_size: float,
    overlap: float,
    preictal_duration: float,
    groups: pd.Series,
    label_to_num: dict,
):
    # pylint: disable=line-too-long
    """Compute the Improvement Over Chance.

    The chance is a random process poisson based classifier that
    uses the same amount of time in warning. See notes.

    Parameters
    ----------
    y_true : pd.Series
        The true values.
    y_pred : pd.Series
        The predicted values, output of the classifier/postprocessing stage.
    threshold : float
        The threshold to use to consider a prediction as 0 or 1.
    epoch_size : float
        The epoch size in seconds.
    overlap : float
        The overlap in seconds.
    preictal_duration : float
        The preictal duration in minutes.
    groups : pd.Series
        A pandas Series that has the same length as `y_true` and `y_pred` that contains
        the group number of each sample.
    label_to_num : dict
        A dictionary containing the string labels as keys and corresponding integer values.

    Returns
    -------
    float
        Improvement Over Chance

    Notes
    -----
    See *The Statistics of a Practical Seizure Warning System* for more detail.
    (doi:10.1088/1741-2560/5/4/004)

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from pyepilepsy.metrics import compute_ioc
    >>> from datetime import datetime

    >>> y_true_arr = [0, 0, 0, 0, 0, 1, 1, 7, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 7]
    >>> y_pred_arr = [0.1, 0.12, 0.13, 0.56, 0.7, 0.8, 0.6, 0.9,  0.2, 0.1, 0.8, 0.1, 0.2, 0.1, 0.2, 0.7, 0.6, 0.7, 0.9]

    >>> datetime_index = np.hstack([
    ...     pd.date_range("09:00", "12:30", freq="30min", tz="Europe/Paris").to_numpy(),
    ...     pd.date_range("14:00", "19:00", freq="30min", tz="Europe/Paris").to_numpy()
    ... ])
    >>> y_true = pd.Series(
    ...     data=y_true_arr,
    ...     index=datetime_index
    ... )
    >>> y_pred = pd.Series(
    ...     data=y_pred_arr,
    ...     index=datetime_index
    ... )
    >>> groups = pd.Series(
    ...     data=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ...     index=datetime_index
    ...     )
    >>> compute_ioc(
    ...     y_true=y_true,
    ...     y_pred=y_pred,
    ...     threshold=0.58,
    ...     epoch_size=60*30,
    ...     overlap=60*10,
    ...     preictal_duration=60,
    ...     groups=groups,
    ...     label_to_num= {'ictal': 7, 'preictal': 1, 'interictal': 0}
    ...     )
    0.4736842105263158
    """
    if not isinstance(y_pred, pd.Series):
        raise ValueError("y_pred has to be a pd.Series. Please convert it.")
    if not isinstance(y_true, pd.Series):
        raise ValueError("y_true has to be a pd.Series. Please convert it.")
    y_true.sort_index(inplace=True)
    y_pred.sort_index(inplace=True)

    total_duration = len(y_true) * (epoch_size - overlap)
    if total_duration == 0:
        raise ValueError("WTF: total duration is null...")
    seizure_label = label_to_num["ictal"]

    y_pred_01 = y_pred.copy()
    mask_low = y_pred_01 <= threshold
    mask_high = y_pred_01 > threshold
    y_pred_01[mask_low] = 0
    y_pred_01[mask_high] = 1
    y_pred_01 = y_pred_01.astype(int)

    # detected seizure(s) ? and horizon (TODO)
    detected_seizures = 0
    nb_seizures = 0
    n_tp = 0
    n_fp = 0
    for group in groups.unique():
        # check if a seizure is in group...
        if seizure_label in y_true[groups == group].values:
            nb_seizures += 1
            group_mask_tp = np.logical_and(
                np.logical_and(groups == group, y_pred_01 == 1), y_true == 1
            )
            group_mask_fp = np.logical_and(
                np.logical_and(groups == group, y_pred_01 == 1), y_true == 0
            )
            n_fp += np.sum(group_mask_fp)
            if np.sum(group_mask_tp) > 0:
                detected_seizures += 1
                n_tp += np.sum(group_mask_tp)

    ns = nb_seizures
    if ns == 0:
        raise ValueError(
            "Cannot compute seizure rate detection because there is no seizure !"
        )
    sr = detected_seizures / ns

    # get mask of bad annotations
    bad_mask = pd.Series(data=np.zeros(y_true.shape), index=y_pred.index)
    for key, val in label_to_num.items():
        if "BAD" in key:
            bad_mask[y_true == val] = 1

    # Time in Warning
    tiw = (
        compute_tiw(
            y_pred_01,
            tau=preictal_duration,
            epoch_size=epoch_size,
            overlap=overlap,
            bad_mask=bad_mask,
        )
        / total_duration
    )
    ioc = sr - tiw

    return ioc


# pylint: disable=too-many-statements
def compute_tiw(
    y_pred_01: pd.Series,
    tau: float,
    epoch_size: float,
    overlap: float,
    bad_mask: Union[pd.Series, None] = None,
) -> float:
    """Extract the time in warning of the current predictions given a tau

    The computation has been optimized using the following approach:

    ..

        * sort predictions and mask
        * remove ``bad_mask`` firings
        * extract time-continuous predictions. On each block:
            * get the firing indexes
            * apply the tiw from last firing index
            * apply the tiw on all ``tau`` seconds after all firings indexes
            * return the warning block + the last firing index
        * apply ``bad_mask`` firings again

    Parameters
    ----------
    y_pred_01 : pd.Series
        The prediction series filled with 0 and 1. Index must be of type datetime64.
    tau : float
        The warning time to fire when a positive/preictal class is detected (in minutes).
        We must have be ``tau >= epoch_size``
    epoch_size : float
        The epoch size in seconds
    overlap : float
        The overlap between 2 successive epochs in seconds.
    bad_mask : pd.Series, optional
        A mask to remove some warning windows (such as bad annotations). Must contains 1 and 0.
        1 is to remove, 0 is to keep. If None, nothing is removed. The default is None.

    Returns
    -------
    float
        the duration of time in warning in seconds

    Notes
    -----
    In a cross-val context, the TiW is probably reduced because a group ends with the ictal
    segment, so if a warning is fired at the end, the time in warning that should be generated
    after the current time segment is not added. BUT, for global results, the time in warning
    is computed again based on all `y_pred_01` tested groups and these missing time in warning
    segments are accounted for.

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from pyepilepsy.metrics import compute_tiw
    >>> y_pred_arr = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1]
    >>> datetime_index = np.hstack([
    ...     pd.date_range("09:00", "12:30", freq="30min").to_numpy(),
    ...     pd.date_range("14:00", "19:00", freq="30min").to_numpy()
    ... ])
    >>> y_pred_01 = pd.Series(
    ...     data=y_pred_arr,
    ...     index=datetime_index
    ... )
    >>> compute_tiw(
    ...     y_pred_01=y_pred_01,
    ...     tau=30,
    ...     epoch_size=60*40,
    ...     overlap=60*10,
    ...     bad_mask=None
    ... )
    18000

    >>> bad_mask = pd.Series(
    ...     data=[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ...     index=datetime_index
    ... )
    >>> compute_tiw(
    ...     y_pred_01=y_pred_01,
    ...     tau=30,
    ...     epoch_size=60*40,
    ...     overlap=60*10,
    ...     bad_mask=bad_mask
    ... )
    16200
    """

    def tiw_on_block(block, tau, epoch_size, overlap, old_last_firing_dt):
        next_pos_epochs = math.ceil(
            (tau - overlap) / (epoch_size - overlap)
        )  # the epoch at t + tau
        pos_indexes = np.argwhere(block.values == 1)
        if pos_indexes.shape[0] > 0:
            pos_indexes = pos_indexes[:, 0]
        else:
            pos_indexes = []

        warning_block = block.copy()

        # deal with previous firing datetime
        if old_last_firing_dt is not None:
            if old_last_firing_dt + timedelta(seconds=tau) > block.index[0]:
                # we have to update some epochs...
                over_warning_time = (
                    (old_last_firing_dt + timedelta(seconds=tau)) - block.index[0]
                ).total_seconds()
                last_warning_epoch = int(
                    min(over_warning_time / (epoch_size - overlap), len(warning_block))
                )
                over_epochs = np.arange(last_warning_epoch)
                warning_block[warning_block.index[over_epochs]] = 1

        # deal with insed block firing
        if len(pos_indexes) > 0:
            max_index = len(warning_block)
            warning_indexes = []
            for index in pos_indexes:
                if index + next_pos_epochs < max_index:
                    warning_indexes.append(
                        np.arange(index, index + 1 + next_pos_epochs)
                    )
                else:
                    warning_indexes.append(np.arange(index, max_index))
            warning_indexes = np.concatenate(warning_indexes)
            warning_block[
                warning_block.index[warning_indexes]
            ] = 1  # we have our warning block

            last_firing_dt = block.index[pos_indexes[-1]]
        else:
            last_firing_dt = None
            # reuse old firing datetime if its warning time go after the end of the current block
            if old_last_firing_dt is not None:
                if old_last_firing_dt + timedelta(seconds=tau) > block.index[-1]:
                    last_firing_dt = old_last_firing_dt

        return warning_block, last_firing_dt

    tau = tau * 60  # tau in seconds now
    if bad_mask is None:
        bad_mask = pd.Series(
            data=np.zeros(len(y_pred_01)),
            index=y_pred_01.index,
        )
    bad_mask = bad_mask.astype(bool)

    # work on another series
    warning_epochs = y_pred_01.copy()
    # sort the series
    warning_epochs.sort_index(inplace=True)
    bad_mask.sort_index(inplace=True)
    # erase some bad warning epochs
    warning_epochs[bad_mask] = 0

    gaps = (
        np.argwhere(
            (warning_epochs.index[1:] - warning_epochs.index[:-1])
            != timedelta(seconds=epoch_size - overlap)
        )
    ).flatten()
    gaps += 1
    gaps = np.insert(gaps, 0, 0)
    gaps = np.insert(gaps, len(gaps), len(warning_epochs))

    warning_blocks = []
    last_firing_dt = None
    for i in range(len(gaps) - 1):
        # we extract a time-continuous block of predictions
        block = warning_epochs.iloc[gaps[i] : gaps[i + 1]]
        warning_block, last_firing_dt = tiw_on_block(
            block, tau, epoch_size, overlap, last_firing_dt
        )
        warning_blocks.append(warning_block)
    warning_blocks = pd.concat(warning_blocks).sort_index()

    # note: this line is not a duplicate
    warning_blocks[bad_mask] = 0

    # init time in warning
    tiw = 0
    if (warning_blocks == 1).any():
        # now, we compute the tiw taking care of the overlap between windows
        tiw = np.sum(warning_blocks.values) * (epoch_size - overlap)

    return tiw


def compute_sensitivity_chance_pred(
    preictal_duration: float, tau: float, rho: float
) -> float:
    """Compute the sensitivity of a random poisson based chance predictor
    given the time in warning ratio of the predictor.

    Parameters
    ----------
    preictal_duration : float
        The preictal duration in minutes
    tau : float
        The firing duration in minutes
    rho : float
        The time in warning ratio of the predictor to compare with chance

    Returns
    -------
    float
        Sensitivity of a random poisson based chance predictor

    Notes
    -----
    See *The Statistics of a Practical Seizure Warning System* for more detail.
    (doi:10.1088/1741-2560/5/4/004)

    Note that I am not sure about the validity of the formula without
    ``preictal_duration=tau``, even if it looks logical.

    Examples
    --------
    Let's say we have built a classifier with a postprocessing stage that gives
    ``tiw=0.2`` for a preictal duration of 60min. To compare with alarm systems,
    we use ``tau=preictal_duration``, so that any preictal detection leads to
    a warning during the seizure. We then have:

    >>> from pyepilepsy.metrics import compute_sensitivity_chance_pred
    >>> compute_sensitivity_chance_pred(preictal_duration=60, tau=60, rho=0.2)
    0.19999999999999996

    We find, as in the paper, that :math:`Sen_{chance-predictor} \\approx rho`
    """
    if np.isclose(rho, 1.0):
        warnings.warn("rho close to one so we take 0.99")
        rho = 0.99
    lam = -np.log(1 - rho) / tau
    return 1 - np.exp(-lam * preictal_duration)
