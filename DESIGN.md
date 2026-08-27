# Zycus AI Support — Design Note

## 1. Failure Modes

The first production failure mode is incorrect ticket classification or prioritisation. A support ticket may contain ambiguous language, incomplete descriptions, or multiple issues, causing the system to assign the wrong category or urgency. This can be detected through the evaluation harness, monitoring classification distributions, and tracking corrections made by support engineers. Mitigation includes structured output validation, explicit acceptance criteria, knowledge-base retrieval, risk detection, and regression tests for ambiguous and high-risk tickets.

The second failure mode is incorrect or incomplete customer context. A ticket may reference an account that does not exist in the account dataset, or account information may be incomplete. The system therefore treats customer context as optional instead of assuming it always exists. Missing accounts are handled gracefully, and the ticket can still be triaged. For the TAM workflow, missing or incomplete account data is also covered by adversarial evaluation cases.

The third failure mode is incorrect risk detection. A ticket containing security, production-impact, escalation, or customer-impact signals could be incorrectly classified as low risk. This is particularly important because missing a high-risk ticket is more serious than producing an unnecessary escalation. The system uses deterministic risk detection rules and validates high-risk scenarios through the evaluation harness. Production monitoring should track false negatives and allow support teams to override the automated assessment.

## 2. Latency vs Quality

The main trade-off is between richer context and response speed. Task 1 retrieves relevant knowledge-base documents and customer/account context before generating the triage result. This improves classification and response quality but requires additional processing compared with a simple keyword classifier.

If latency became the hard constraint, I would reduce the retrieval depth, cache knowledge-base results, precompute document representations, and use a smaller/faster model for straightforward tickets. Complex or high-risk tickets could still be routed through the more detailed pipeline.

## 3. Data Sensitivity

Support tickets and account summaries may contain sensitive customer information or PII. The application is designed around the provided synthetic dataset and does not introduce external customer data. Environment variables are used for API credentials, `.env` is excluded through `.gitignore`, and the real API key is never committed to the repository.

For a production deployment, I would additionally minimize the data sent to an external LLM by sending only the fields required for the task, redact or mask known PII before external API calls, use an approved enterprise LLM endpoint with appropriate data-retention controls, and maintain audit logging without storing unnecessary sensitive content.

## 4. Scaling

The current implementation is suitable for the provided synthetic dataset and a lightweight internal application. At 10× the ticket volume, the first bottleneck would likely be repeated knowledge-base retrieval and LLM/API calls rather than the deterministic Python processing itself.

To scale the system, I would cache frequently used retrieval results, maintain an indexed/vector-based knowledge-base retriever, process independent tickets asynchronously, and add request-level monitoring and rate limiting. For the TAM workflow, account summaries could also be precomputed or refreshed incrementally instead of rebuilding the entire context for every request.

The evaluation harness would remain part of the deployment process so changes to retrieval, prompts, models, or risk rules could be checked against the same regression cases before release.
