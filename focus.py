def focus(dictonary, main="", secondary="", gain=10):
    has_main_letter = lambda t: any([l in t for l in main]) or len(main) == 0
    has_secondary_letter = lambda t: any([l in t for l in secondary])
    amount_of_secondary_letters = lambda word: sum([l in word for l in secondary])
    result = {
        k: max(1, amount_of_secondary_letters(k) * gain) * v
        for k, v in dictonary.items()
        if has_main_letter(k)
    }
    return result
