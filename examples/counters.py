#!/usr/bin/env python3

import concur as c


def counter():
    counter = 0
    while True:
        action, _ = yield from c.orr(
            [ c.text(f"Count: {counter}")
            , c.orr_same_line([c.button("Increment"), c.button("Decrement"), c.button("Reset")])
            ])
        if action == "Increment":
            counter += 1
        elif action == "Decrement":
            counter -= 1
        elif action == "Reset":
            counter = 0
        yield


def app():
    return c.orr([counter(), counter()])


if __name__ == "__main__":
    c.main("Counter", app(), 500, 500)
