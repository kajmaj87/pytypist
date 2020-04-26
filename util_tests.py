from entities import Transition


def prepare_stage(stage_text, written_text, delete_char="<", key_time=10):
    first_key = True
    result = []
    char_in_text = 1
    check_chars = (
        lambda x, y: "CORRECT" if x == y else "ERASE" if l == delete_char else "ERROR"
    )
    transform_erase = lambda x: "ERASE" if x == delete_char else x
    last_key = "START"
    current_text = ""
    for l in written_text:
        if l == delete_char:
            current_text = current_text[:-1]
            state = "ERASE"
        else:
            current_text += l
            if current_text == stage_text[:char_in_text]:
                state = "CORRECT"
                char_in_text += 1
            else:
                state = "ERROR"
        result.append(
            t(s=transform_erase(last_key), e=transform_erase(l), st=state, t=key_time)
        )
        last_key = l

    return result


def t(s="", e="", st="", t=0):
    return Transition(s, e, st, t)
