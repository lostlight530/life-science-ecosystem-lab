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
    doc: Frozen GitHub evidence records in JSON array form
  topics:
    type: File
    doc: Versioned topic registry JSON
outputs:
  candidate:
    type: File
    outputSource: aggregate/candidate
  validation_report:
    type: File
    outputSource: validate/report
  knowledge:
    type: File
    outputSource: extract_knowledge/knowledge
  knowledge_verification:
    type: File
    outputSource: verify_knowledge/report
steps:
  aggregate:
    run: tools/aggregate.cwl
    in:
      records: records
      topics: topics
    out: [candidate]
  validate:
    run: tools/validate.cwl
    in:
      candidate: aggregate/candidate
    out: [report]
  extract_knowledge:
    run: tools/knowledge.cwl
    in:
      candidate: aggregate/candidate
      topics: topics
    out: [knowledge]
  verify_knowledge:
    run: tools/verify-knowledge.cwl
    in:
      candidate: aggregate/candidate
      topics: topics
      knowledge: extract_knowledge/knowledge
    out: [report]
