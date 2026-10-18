cwlVersion: v1.2
class: Workflow
label: Source-Grounded Life Science Workflow Knowledge Cartography
id: '#main'
doc: >
  Deterministic, offline replay of approved GitHub evidence records. The separately
  callable GitHub collector acquires source snapshots; this workflow consumes a
  frozen records fixture and a topic profile, produces a candidate, extracts topic-linked source-cited knowledge and verifies every artifact.
requirements:
  - class: SubworkflowFeatureRequirement
inputs:
  records:
    type: File
    label: Frozen GitHub evidence records
    doc: Frozen GitHub evidence records in JSON array form
  topics:
    type: File
    label: Versioned topic registry
    doc: Versioned topic registry JSON
outputs:
  candidate:
    type: File
    label: Candidate evidence package
    doc: Deterministically aggregated evidence candidate before knowledge extraction
    outputSource: aggregate/candidate
  validation_report:
    type: File
    label: Validation report
    doc: Machine-readable validation result for the evidence candidate
    outputSource: validate/report
  knowledge:
    type: File
    label: Source-grounded knowledge map
    doc: Topic-linked knowledge map with source citations and explicit unknowns
    outputSource: extract_knowledge/knowledge
  knowledge_verification:
    type: File
    label: Knowledge verification report
    doc: Machine-readable verification of provenance, topic links and knowledge structure
    outputSource: verify_knowledge/report
steps:
  aggregate:
    label: Aggregate evidence records
    doc: Normalize supplied records and construct the deterministic evidence candidate
    run: tools/aggregate.cwl
    in:
      records: records
      topics: topics
    out: [candidate]
  validate:
    label: Validate evidence candidate
    doc: Check the candidate schema and source-provenance contract
    run: tools/validate.cwl
    in:
      candidate: aggregate/candidate
    out: [report]
  extract_knowledge:
    label: Extract source-grounded knowledge
    doc: Construct topic-linked source-cited knowledge and explicit coverage gaps
    run: tools/knowledge.cwl
    in:
      candidate: aggregate/candidate
      topics: topics
    out: [knowledge]
  verify_knowledge:
    label: Verify knowledge map
    doc: Verify references, topic links, declared unknowns and structural integrity
    run: tools/verify-knowledge.cwl
    in:
      candidate: aggregate/candidate
      topics: topics
      knowledge: extract_knowledge/knowledge
    out: [report]
