from rl.policy import LinearAnnealedPolicy


class BinnedLinAnnPolicy(LinearAnnealedPolicy):

    """
    LinearAnnealedPolicy for Binned Curriculum Learning

    Description
        The intention of designing this module is to run the existing LinearAnnealedPolicy repeatedly within an interval.
        Specifically, the attr value is repeatedly annealed from value_max to value_min within the interval of steps defined by bins.

        Once all the parameters are defined, a pattern of attr value shows below:
            step 0 ~ int(bins[0] * decreasing_ratio) : attr goes down from value_max to value_min
            step int(bins[0] * decreasing_ratio) ~ bins[0] : attr = value_min
            step bins[i] ~ int(bins[i] + (bins[i + 1] - bins[i]) * decreasing_ratio) : attr goes down AGAIN from value_max to value_min
            ...
            step bins[-1] ~ bins[-1] + nb_steps : attr goes down AGAIN from value_max to value_min
            step bins[-1] + nb_steps ~ inf : attr = value_min

    Parameters
    ----------
    inner_policy : Type[Policy]
        Policy object that chooses agent's action
    attr : str
        A name of instance variable within the inner_policy to be annealed
    value_max : float
        Maximum value of attr variable
    value_min : float
        Minimum value of attr variable
    value_test : float
        Test value of attr variable (constant)
    nb_steps : int
        Annealing steps at last phase
    decreasing_ratio : float
        Ratio of step lengths that are annealed within an interval. Definitely it should between 0.0 and 1.0.
    bins : list[int]
        List of interval boundaries. DO NOT INCLUDE 0 and inf.
    
    Reference
    ---------
    https://github.com/tensorneko/keras-rl2
        See help(rl.policy.LinearAnnealedPolicy).
    """

    def __init__(self, inner_policy, attr, value_max, value_min, value_test, nb_steps, decreasing_ratio, bins):
        super(BinnedLinAnnPolicy, self).__init__(inner_policy, attr, value_max, value_min, value_test, nb_steps)
        self.decreasing_ratio = decreasing_ratio
        self.bins = [0] + bins
        return

    def get_current_value(self):
        if self.agent.training:
            idx = sum([int(int(self.agent.step) >= bin_) for bin_ in self.bins])
            upper = self.bins[idx]
            lower = self.bins[idx - 1]
            if idx == len(self.bins) - 1:
                landing_step = self.nb_steps
            else:
                landing_step = int((upper - lower) * self.decreasing_ratio)
            a = -float(self.value_max - self.value_min) / float(landing_step)
            b = float(self.value_max)
            value = max(self.value_min, a * float(self.agent.step - lower) + b)
        else:
            value = self.value_test
        return value
