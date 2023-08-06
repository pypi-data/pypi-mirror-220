"""
For some problems multiple (competing) solvers/simulations exists.
In order to abstract the concrete solver code away into the problem it solves,
Flavours are to be mixed into your code or backend.

.. mermaid::

    classDiagram
        direction BT

        class BackendFlavor {
            <<abstract>>
            <<concept>>
        }

        class FieldLineTracerBackend {
            <<abstract>>
            +/*abstract*/ _find_lcfs()
            +/*abstract*/ _trace_diffusion()
        }
         class FieldlinesBackend {
            <<abstract>>
            + _find_lcfs()
            + _trace_diffusion()
        }
         class FltBackend {
            <<abstract>>
            + _find_lcfs()
            + _trace_diffusion()
        }

        FieldLineTracerBackend --|> Flavor
        FltBackend --|> FieldLineTracerBackend
        FieldlinesBackend --|> FieldLineTracerBackend

"""
# TODO-1(@dboe): Add an abstract Flavour and FlavourBackend class - move abstaction to new module
