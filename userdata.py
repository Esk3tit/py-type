from dataclasses import dataclass


@dataclass
class UserData:
    """
    Calculate avg wpm and accuracy by diving respective sum by number of trials
    """
    max_wpm: int = 0
    wpm_sum: int = 0
    num_trials: int = 0
    accuracy_sum: int = 0

    def avg_wpm(self) -> int:
        return self.wpm_sum // self.num_trials

    def avg_accuracy(self) -> int:
        return self.accuracy_sum // self.num_trials
