# Script Constants

File: `common/script_constants/` + `documentation.md`
Defines structured constants that can be reused in scripts using `constant:path`.

## Concept

- Has schema (key type: int / fixed_point / nested)
- Only fields whose documentation states that they support constants can be used
- After changing the constants, you need to follow the document reloading order: constant library → user script

## Use

```pdx
# Example concept (subject to ontology documentation and reference points)
set_variable = { my_var = constant:sp_complexity.some_key }
```

Systems such as special projects make heavy use of constants (see files such as `special_project_constants`).

## Specification

- Put the new constants in your own file and write the schema clearly
- Don't assume any effect parameter accepts `constant:`
- The total conversion complex numerical table is suitable for constants; for ordinary national focuses, just write numbers directly

## Related

- `special-projects-template.md` / `variables-arrays-template.md` / `defines-template.md`
