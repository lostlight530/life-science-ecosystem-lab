# Life Science Bio Tool (third independent software asset)

`ls-bio` executes **biological file data processing** rather than repository provenance inspection or document retrieval. It can be run locally without either of the other two repository CLIs, cloud credentials, LLMs, GPUs, or network access.

```sh
python -m pip install --no-deps -e .
ls-bio protein-fasta --input path/to/protein.fasta --output build/protein-fasta-report.json
ls-bio protein-pdb --input path/to/structure.pdb --output build/protein-pdb-report.json
```

### Supported inputs and bounded outputs

- FASTA: actual protein sequence parsing, canonical/uncertain residue composition, distinct headers, complete input SHA-256, stable JSON report. Supports standard 20 amino acids and uncertain/rare `B/X/Z/J/U/O` codes, reports noncanonical positions. Rejects gaps, stop symbols and malformed input; this is **not** a multiple-sequence alignment reader.
- PDB: fixed-width `ATOM` records, only C-alpha (`CA`) records from the first model, chain-level observed sequence residue counts with explicit warnings for unknown three-letter residue names and duplicate C-alpha records. It does not inspect all atoms or prove PDB chemical geometry, fold accuracy, full-chain completeness or sequence alignment.
- Both modes limit source input to 8 MB; reports exclude full source sequences and atomic coordinates, and retain only bounded quality counts, digest and safe source identifiers.

### Workflow integration and reproducibility

Portable CWL CommandLineTool wrappers are in `.github/bio/protein-fasta.cwl` and `.github/bio/protein-pdb.cwl`. `python -m unittest discover -s tests -v` checks deterministic reports, malformed input rejection, first-model behavior and CLI. The separate `life-science-bio.yml` CI also runs CWL replay. CWL inputs require explicit EDAM format declarations, supplied by `.github/bio/test/fasta-job.yml` and `.github/bio/test/pdb-job.yml`. The optional scheduled or manual pinned-sample job verifies immutable GitHub tree/blob identity before running on external research example files. Only metadata summaries are retained.

### bio.tools / ELIXIR registration

`metadata/biotools-protein-audit.draft.json` is a **candidate**, not a registered entry and contains no invented tool ID. It uses reviewed EDAM terms for Proteins (topic_0078), Sequence analysis (operation_2403), Protein structure analysis (operation_2406), Protein sequence (data_2976), FASTA (format_1929), PDB (format_1476) and Sequence report (data_2955). All operations map to implemented commands. A real bio.tools account, current registry validation and actual public accession are independently required before stating registration.

Public reference: [bio.tools Curators Guide](https://biotools.readthedocs.io/en/latest/curators_guide.html), [biotoolsSchema](https://github.com/bio-tools/biotoolsSchema), [EDAM ontology](https://www.ebi.ac.uk/ols4/ontologies/edam/).
