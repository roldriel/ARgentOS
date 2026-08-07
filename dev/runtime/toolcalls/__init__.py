"""Reference runtime: Execution Context materializations (prompt and tool calls).

This package is a reference implementation on the runtime side of the
protocol/runtime boundary. It is not protocol: `.agents/` defines what an
Execution Context is and how it is delivered; this package only decides how a
concrete runtime represents it.
"""
