# Publication and security boundary

**中文安全与敏感科研数据提示**：本仓只接受符合公开来源和许可边界的资料，公开 Issue、PR、运行输入与 Artifacts 不应携带密钥、私有链接、健康／临床个人数据或未经修复的漏洞细节；私密漏洞通过 GitHub Security Advisory 渠道反馈；编译、CI、DOI 和元数据校验均不构成隐私、医学或安全认证

**English scope note:** Use GitHub's private security-advisory channel for sensitive disclosures; never include credentials, private links, person-level health/clinical data or unpatched exploit details in public artifacts. Passing CI, repository publication and DOI metadata do not imply clinical, privacy or security certification


This is a public research-software repository. Only public interfaces, documented input/output formats, examples using synthetic non-sensitive data, tests and reproducibility metadata are published

Do **not** put tokens, private URLs, credentials, personally identifying research records, unpublished source documents, internal research plans, private decision records or access-controlled information in issues, pull requests, workflow inputs or CI artifacts

The public workflow may retrieve only the explicitly approved public GitHub repositories in `evidence/profiles/sources.json`. GitHub topic discovery is advisory and never automatically promotes a discovered repository into the allowed list

Report a potentially sensitive disclosure privately through GitHub's security-advisory feature when available, rather than opening a public issue. Git history retains earlier versions of deleted files and repository deletion does not reliably remove public copies or cached versions

Source compatibility, schema validation and successful GitHub Actions checks are not clinical validation, full standards certification, WorkflowHub publication or LifeMonitor monitoring confirmation
