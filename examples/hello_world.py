#!/usr/bin/env python3

import concur as c
import concur.integrations.glfw as window


def app():
    while True:
        yield from c.button("Hello!")
        yield
        yield from c.orr([c.text("Hello, world!"), c.button("Restart?")])
        yield


if __name__ == "__main__":
    window.main(app(), "Hello World", 500, 500)
