# Historical bench topology

Migrated from WireSpaces/hardware/bench. The original README and exact source files are preserved in ../../imports/legacy-hardware.tar.gz. This topology is a code-generator fixture and historical bench plan, not accepted Board 1 circuitry (ADR-003/007).

With WireSpaces and ws-hardware checked out side by side, run from the WireSpaces repository:

```sh
codegen/.venv/bin/python codegen/wiring_codegen.py ../ws-hardware/libraries/legacy/bench/topology.yaml --local-host Gateway --explain
```

Schema documentation remains in WireSpaces/codegen/README.md. No topology or hardware validation is implied by migration.

The YAML editor-schema modeline now points to the sibling WireSpaces checkout; topology content is otherwise unchanged.
