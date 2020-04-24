from entities import Transition
from files import save, load_array

transition_path = "stats/transitions"


def save_transitions(transitions):
    save(transitions, transition_path)


def load_transitions():
    return load_array(
        transition_path, transform=lambda t: Transition(t[0], t[1], t[2], t[3])
    )
