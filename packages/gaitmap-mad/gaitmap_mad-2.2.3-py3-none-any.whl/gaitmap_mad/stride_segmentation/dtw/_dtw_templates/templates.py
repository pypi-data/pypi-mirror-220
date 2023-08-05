"""Dtw template base classes and helper."""
from importlib.resources import open_text
from typing import Iterable, List, Optional, Sequence, Tuple, Union, cast

import numpy as np
import pandas as pd
from tpcp import HyperParameter, OptimizableParameter, cf
from typing_extensions import Self

from gaitmap.base import BaseAlgorithm
from gaitmap.data_transform import BaseTransformer, FixedScaler, TrainableTransformerMixin
from gaitmap.utils._types import _Hashable
from gaitmap.utils.array_handling import multi_array_interpolation
from gaitmap.utils.datatype_helper import SingleSensorData, is_single_sensor_data


class BaseDtwTemplate(BaseAlgorithm):
    """Base class for dtw templates."""

    use_cols: Optional[Sequence[Union[str, int]]]

    def __init__(
        self,
        *,
        scaling: Optional[BaseTransformer] = None,
        use_cols: Optional[Sequence[Union[str, int]]] = None,
    ):
        self.scaling = scaling
        self.use_cols = use_cols

    def get_data(self) -> Union[np.ndarray, pd.DataFrame]:
        """Return the template data."""
        raise NotImplementedError

    def _apply_scaling(self, data, sampling_rate_hz: float) -> SingleSensorData:
        if not self.scaling:
            return data
        if isinstance(data, np.ndarray):
            raise TypeError(
                "Data Transformations are only supported for dataframe templates at the moment."
                "Explicitly set `self.scaling` to None."
            )
        return self.scaling.clone().transform(data, sampling_rate_hz=sampling_rate_hz).transformed_data_

    def transform_data(self, data: SingleSensorData, sampling_rate_hz: float) -> SingleSensorData:
        """Transform external data according to the template scaling.

        This method should be applied to the data before the template is matched.
        There is usually no need to do this manually, as all the implemented Dtw methods do this automatically
        internally.

        Parameters
        ----------
        data : SingleSensorData
            The data to transform.
        sampling_rate_hz : float
            The sampling rate of the data.
            This will be forwarded to the scaler, incase it is used.

        Returns
        -------
        SingleSensorData
            The transformed data.

        """
        return self._apply_scaling(data, sampling_rate_hz)


class BarthOriginalTemplate(BaseDtwTemplate):
    """Template used for stride segmentation by Barth et al.

    Parameters
    ----------
    scaling
        A multiplicative factor used to downscale the signal before the template is applied.
        The downscaled signal should then have have the same value range as the template signal.
        A large scale difference between data and template will result in mismatches.
        At the moment only homogeneous scaling of all axis is supported.
        Note that the actual use of the scaling depends on the DTW implementation and not all DTW class might use the
        scaling factor in the same way.
        For this template the default value is 500, which is adapted for data that has a max-gyro peak of approx.
        500 deg/s in `gyr_ml` during the swing phase.
        This is appropriate for most walking styles.
    use_cols
        The columns of the template that should actually be used.
        The default (all gyro axis) should work well, but will not match turning stride.
        Note, that this template only consists of gyro data (i.e. you can only select one of
        :obj:`~gaitmap.utils.consts.BF_GYR`)

    Notes
    -----
    As this template was generated by interpolating multiple strides, it does not really have a single sampling rate.
    The original were all recorded at 102.4 Hz, but as the template is interpolated to 200 samples, its is closer to an
    effective sampling rate of 200 Hz (a normal stride is around 0.8-1.5s).
    This template reports a sampling rate of 204.8 Hz, to prevent resampling for this very common sampling rate.

    See Also
    --------
    gaitmap.stride_segmentation.DtwTemplate: Base class for templates
    gaitmap.stride_segmentation.BarthDtw: How to apply templates for stride segmentation

    """

    template_file_name = "barth_original_template.csv"
    sampling_rate_hz = 204.8

    def __init__(self, *, scaling=cf(FixedScaler(scale=500.0)), use_cols: Optional[Sequence[Union[str, int]]] = None):
        super().__init__(scaling=scaling, use_cols=use_cols)

    def get_data(self) -> Union[np.ndarray, pd.DataFrame]:
        """Return the template data.

        This will only return the columns of data that are listed in `use_cols` and will apply the scaling.
        """
        with open_text(
            "gaitmap_mad.stride_segmentation.dtw._dtw_templates",
            cast(str, self.template_file_name),
        ) as test_data:
            data = pd.read_csv(test_data, header=0)
        template = data

        use_cols = template.columns if self.use_cols is None else self.use_cols
        return self._apply_scaling(template[list(use_cols)], self.sampling_rate_hz)


class TrainableTemplateMixin:
    """Mixin for templates that can be optimized/trained/generated from data."""

    def self_optimize(
        self,
        data_sequences: Iterable[SingleSensorData],
        sampling_rate_hz: Optional[float] = None,
        *,
        columns: Optional[List[_Hashable]] = None,
        **_,
    ) -> Self:
        """Optimize or recreate the template from data sequences."""
        raise NotImplementedError


class DtwTemplate(BaseDtwTemplate):
    """Wrap all required information about a dtw template.

    Parameters
    ----------
    data
        The actual data representing the template.
        If this should be a array or a dataframe might depend on your usecase.
        This data is the **unscaled** version of the template.
        Use the `get_data` method to get the correctly scaled template.
    sampling_rate_hz
        The sampling rate that was used to record the template data.
        This will be overwritten by the sampling rate of provided to the `self_optimize` method.
    scaling
        A valid scaler instance, that is used to transform the template data.
        It is usually a good idea to choose a scaler that maps the template to a range from -1-1.
        The same scaler must then be applied to the data before matching the template.
        This can be done using the `transform_data` method.

        Note that the scaler is not adapted to the template in any way for this base `DtwTemplate` class.
        The scaler will be applied to the data (using `transform_data`) and to the template (using `get_data`) as is.
        If you want to use a trainable scaler, that is modified based on the template data, use one of the
        `TrainableTemplateMixin` subclasses and create new templates via the provided `self_optimize` method.
    use_cols
        The columns of the template that should actually be used.
        If the template is an array this must be a list of **int**, if it is a dataframe, the content of `use_cols`
        must match a subset of these columns.
        This will affect the return value of the `get_data` method.

    See Also
    --------
    gaitmap.stride_segmentation.BaseDtw: How to apply templates
    gaitmap.stride_segmentation.BarthDtw: How to apply templates for stride segmentation

    """

    sampling_rate_hz: Optional[float]
    template_file_name: Optional[str]
    scaling: Optional[BaseTransformer]
    data: Optional[Union[np.ndarray, pd.DataFrame]]

    def __init__(
        self,
        *,
        data: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        sampling_rate_hz: Optional[float] = None,
        scaling: Optional[BaseTransformer] = None,
        use_cols: Optional[Sequence[Union[str, int]]] = None,
    ):

        self.data = data
        self.sampling_rate_hz = sampling_rate_hz
        super().__init__(scaling=scaling, use_cols=use_cols)

    def get_data(self) -> Union[np.ndarray, pd.DataFrame]:
        """Return the template data.

        This will only return the columns of data that are listed in `use_cols` and will apply the scaling.
        """
        data = self.data
        if data is None:
            raise ValueError(
                "No data was provided for this template. "
                "Either pass a dataframe or a numpy array to the constructor or use `self_optimize` (if "
                "implemented by the Template class you are using) to calculate a template from example "
                "data."
            )
        template = data

        if self.use_cols is None:
            return self._apply_scaling(template, self.sampling_rate_hz)
        use_cols = list(self.use_cols)
        if isinstance(template, np.ndarray):
            if template.ndim < 2:
                raise ValueError("The stored template is only 1D, but a 2D array is required to use `use_cols`")
            return np.squeeze(template[:, use_cols])
        return self._apply_scaling(template[use_cols], self.sampling_rate_hz)


class InterpolatedDtwTemplate(DtwTemplate, TrainableTemplateMixin):
    """A template that is created by interpolating and then averaging the data of multiple sequences.

    Use the self_optimize method to create a template from data.

    Parameters
    ----------
    data
        The actual data representing the template.
        If this should be a array or a dataframe might depend on your usecase.
        This data is the **unscaled** version of the template.
        Use the `get_data` method to get the correctly scaled template.
    sampling_rate_hz
        The sampling rate that was used to record the template data.
        This will be overwritten by the sampling rate of provided to the `self_optimize` method.
    scaling
        A valid scaler instance, that is used to transform the template data.
        It is usually a good idea to choose a scaler that maps the template to a range from -1-1.
        The same scaler must then be applied to the data before matching the template.
        This can be done using the `transform_data` method.

        If the scaling is `optimizable`, its parameters will be optimized when a new template is created using the
        `self_optimize` method of the template.
    interpolation_method
        The method used to interpolate the data, when creating a new template using `self_optimize`.
        Refer to :func:`~scipy.interpolate.interp1d` for possible options.
    n_samples
        The number of samples the created template should have.
        If `None`, the average length of all provided trainings sequences will be used.
    use_cols
        The columns of the template that should actually be used.
        If the template is an array this must be a list of **int**, if it is a dataframe, the content of `use_cols`
        must match a subset of these columns.
        This will affect the return value of the `get_data` method.

    Notes
    -----
    This class can be used in combination with :func:`~gaitmap.utils.array_handling.iterate_region_data` to easily
    create a new template based on a labeled stride list.

    See Also
    --------
    gaitmap.stride_segmentation.BaseDtw: How to apply templates
    gaitmap.stride_segmentation.BarthDtw: How to apply templates for stride segmentation

    """

    scaling: OptimizableParameter[Optional[BaseTransformer]]
    data: OptimizableParameter[Optional[Union[np.ndarray, pd.DataFrame]]]
    sampling_rate_hz: OptimizableParameter[Optional[float]]
    interpolation_method: HyperParameter[str]
    n_samples: HyperParameter[Optional[int]]

    def __init__(
        self,
        *,
        data: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        sampling_rate_hz: Optional[float] = None,
        scaling: Optional[BaseTransformer] = None,
        interpolation_method: str = "linear",
        n_samples: Optional[int] = None,
        use_cols: Optional[Sequence[Union[str, int]]] = None,
    ):
        self.interpolation_method = interpolation_method
        self.n_samples = n_samples
        super().__init__(
            data=data,
            sampling_rate_hz=sampling_rate_hz,
            scaling=scaling,
            use_cols=use_cols,
        )

    def self_optimize(
        self,
        data_sequences: Iterable[SingleSensorData],
        sampling_rate_hz: Optional[float] = None,
        *,
        columns: Optional[List[_Hashable]] = None,
        **_,
    ):
        """Create a template from multiple data sequences.

        All data sequences will be interpolated to match `self.n_samples` and then averaged.
        If `self.scaling` is `optimizable`, the scaler will be optimized as well based on the final template data.
        Note, that the scaler is not trained or applied to the data, before the template is generated,
        but only trained on the final template.

        If you need to normalize the data before interpolation, do it on your own and train your own scaler instance.
        In this case it set `self.scaling` to `None`.
        To correctly apply the template to new data, make sure that you apply your custom scaler to the data before
        feeding it into any of the `Dtw` methods.

        Parameters
        ----------
        data_sequences
            A sequence of pandas dataframes that contain the data to be used for the template.
        sampling_rate_hz
            The sampling rate that was used to record the template data.
            Note, that the final sampling rate might not match this value exactly, as the effective sampling rate
            will be approximated based on the actual length of the final template.
        columns
            The columns of the data that should be used for the template.

        Returns
        -------
        self
            The template instance with the template data, sampling rate and scaling adapted based on the data.

        """
        template_df, effective_sampling_rate = _create_interpolated_dtw_template(
            data_sequences,
            sampling_rate_hz,
            kind=self.interpolation_method,
            n_samples=self.n_samples,
            columns=columns,
        )
        self.sampling_rate_hz = effective_sampling_rate
        if isinstance(self.scaling, TrainableTransformerMixin):
            self.scaling = self.scaling.self_optimize([template_df], sampling_rate_hz=self.sampling_rate_hz)
        self.data = template_df
        return self


def _create_interpolated_dtw_template(
    signal_sequences: Iterable[SingleSensorData],
    sampling_rate_hz: float,
    kind: str = "linear",
    n_samples: Optional[int] = None,
    columns: Optional[List[_Hashable]] = None,
) -> Tuple[pd.DataFrame, float]:
    expected_col_order = columns
    arrays = []
    for df in signal_sequences:
        is_single_sensor_data(df, check_acc=False, check_gyr=False, frame="any", raise_exception=True)
        if expected_col_order is None:
            expected_col_order = df.columns
        arrays.append(df[expected_col_order].to_numpy())

    del signal_sequences
    # get mean stride length over given strides
    mean_stride_samples = int(np.rint(np.mean([len(df) for df in arrays])))
    n_samples = n_samples or mean_stride_samples
    resampled_sequences_df_list = multi_array_interpolation(arrays, n_samples, kind=kind)

    template = np.mean(resampled_sequences_df_list, axis=0)
    template_df = pd.DataFrame(template.T, columns=expected_col_order)

    # When we interpolate all templates to a fixed number of samples, the effective sampling rate changes.
    # We approximate the sampling rate using the average stride length in the provided data.
    effective_sampling_rate = sampling_rate_hz
    if n_samples and sampling_rate_hz:
        effective_sampling_rate = n_samples / (mean_stride_samples / sampling_rate_hz)

    return template_df, effective_sampling_rate
