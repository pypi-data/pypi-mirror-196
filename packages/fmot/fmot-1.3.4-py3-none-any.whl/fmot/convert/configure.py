from fmot.qat.nn import quantizers
from typing import *

observer_dict = {
    'min_max': quantizers.MinMaxObserver,
    'moving_min_max': quantizers.MovingAverageMinMaxObserver,
    'gaussian': quantizers.GaussianObserver
}

def configure_param_observer(obs_class: Union[str, quantizers.ObserverBase]='min_max'):
    """
    Configure the default parameter observer.

    Arguments:
        obs_class (str, or class): Default 'min_max'. If a string, options are: 
                'min_max': MinMaxObserver
                'moving_min_max': MovingAverageMinMaxObserver
                'gaussian': GaussianObserver
            Can also pass in a class directly
    """
    if isinstance(obs_class, str):
        obs_class = observer_dict[obs_class]
    
    quantizers.DEFAULT_OBSERVERS['param'] = obs_class
