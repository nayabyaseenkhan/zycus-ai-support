# Zycus AI Support Triage

## AI-Assisted Customer Support Ticket Triage System

---

## 1. Project Overview

Zycus AI Support Triage is an AI-assisted customer support application designed to help support teams analyze and triage customer support tickets.

The system combines structured ticket data, customer account information, customer ticket history, risk detection, ticket summarization, knowledge-base retrieval, deterministic classification, an LLM interface, and structured output validation.

The application provides an interactive Streamlit interface where users can search for support tickets, select a ticket, analyze it, and view the complete triage result.

The system is designed as a modular prototype that can operate in development mode without requiring a production LLM API.

---

## 2. Problem Statement

Customer support teams often process a large number of support tickets. Manually reviewing each ticket can require significant time and can result in inconsistent decisions.

For every support ticket, a support agent may need to:

- Understand the customer's problem.
- Identify the type of issue.
- Check customer account information.
- Review previous customer interactions.
- Determine the urgency of the issue.
- Identify potential high-risk situations.
- Search internal documentation.
- Decide what action should be taken.
- Prepare a response to the customer.

The objective of this project is to automate and assist with these activities through a centralized support triage system.

The system combines data processing, business rules, knowledge retrieval, and an LLM interface to produce a structured and explainable triage result.

---

## 3. Project Objectives

The primary objectives of the project are:

1. Load customer support tickets from structured data.
2. Load customer account information.
3. Retrieve individual tickets using ticket IDs.
4. Retrieve customer account information.
5. Retrieve previous tickets belonging to a customer.
6. Handle missing account information gracefully.
7. Detect potential high-risk support situations.
8. Generate a concise ticket and customer summary.
9. Retrieve relevant information from the internal knowledge base.
10. Classify support tickets into predefined categories.
11. Determine ticket priority.
12. Estimate customer sentiment.
13. Generate recommended support actions.
14. Generate an AI-assisted support response.
15. Validate the final triage output using Pydantic.
16. Provide an interactive Streamlit user interface.
17. Provide unit, integration, and end-to-end tests.
18. Keep the architecture modular so production components can be added later.

---

## 4. System Architecture

The application follows a modular architecture.

The main components are:

- Data Loader
- Account Service
- Risk Detector
- Ticket Summarizer
- Knowledge Base Loader
- Knowledge Base Retriever
- Prompt Builder
- LLM Client
- Triage Agent
- Pydantic Models
- Streamlit Application
- Test Suite

The Triage Agent acts as the central orchestration component.

The general processing sequence is:

Customer Ticket -> Data Retrieval -> Customer Context -> Risk Detection -> Ticket Summarization -> Knowledge Retrieval -> Triage Processing -> Classification -> Recommended Action -> LLM Response -> Structured Validation -> Streamlit Display

Each component has a specific responsibility, which makes the application easier to test, maintain, and extend.

---

## 5. Technology Stack

The project uses the following technologies:

- Python
- Streamlit
- Pydantic
- Pandas
- NumPy
- Scikit-learn
- Python Dotenv
- JSON
- Markdown
- Git
- GitHub

Scikit-learn is used for the knowledge retrieval implementation.

Streamlit is used to build the interactive application.

Pydantic is used to validate the final structured triage result.

Python Dotenv is used for environment configuration.

---

## 6. Project Structure

The project is organized as follows:

zycus-ai-support/

app/
    streamlit_app.py

data/
    accounts.json
    tickets.json

knowledge-base/
    billing/
    onboarding/
    products/
    troubleshooting/

prompts/
    versions/

src/
    __init__.py
    check_data.py
    config.py
    models.py

    tam/
        __init__.py
        account_service.py
        risk_detector.py
        summarizer.py

    triage/
        __init__.py
        agent.py
        prompts.py
        retriever.py

    utils/
        __init__.py
        data_loader.py
        kb_loader.py
        llm_client.py
        validators.py

tests/
    test_data_loader.py
    test_end_to_end.py
    test_kb_chunker.py
    test_kb_loader.py
    test_llm_client.py
    test_missing_account.py
    test_models.py
    test_prompts.py
    test_retriever.py
    test_risk_detector.py
    test_summarizer.py
    test_triage_agent.py
    test_triage_flow.py

.env.example
.gitignore
DESIGN.md
README.md
requirements.txt

---

## 7. Data Layer

The application currently uses JSON files as the data source.

The data directory contains:

data/accounts.json
data/tickets.json

The ticket dataset contains 500 support tickets.

The account dataset contains 50 customer accounts.

The data loader is implemented in:

src/utils/data_loader.py

The data loader provides functions for:

- Loading JSON data.
- Loading all tickets.
- Loading all accounts.
- Finding a ticket by ticket ID.
- Finding an account by account ID.
- Building an account lookup.
- Retrieving tickets belonging to an account.
- Retrieving recent tickets for an account.

The implementation uses Python's pathlib and JSON modules.

---

## 8. Data Validation

The project includes a data validation script:

src/check_data.py

It can be executed using:

python -m src.check_data

The validation process checks whether the ticket and account datasets can be loaded correctly and whether account relationships can be identified.

The current dataset contains 500 tickets and 50 accounts.

The validation also identifies tickets for which the referenced account is not available.

This is important because real-world support data can contain incomplete or inconsistent relationships.

The application does not assume that every ticket will always have a valid customer account.

---

## 9. Customer Account Service

The Account Service is implemented in:

src/tam/account_service.py

Its purpose is to create customer context for a support ticket.

The service attempts to retrieve:

- The ticket.
- The related customer account.
- Previous tickets for the customer.
- Relevant customer ticket history.

The customer context is passed to the rest of the triage pipeline.

If the ticket has no matching account, the system handles the missing account gracefully.

The ticket can still continue through the triage workflow using the information that is available.

This prevents incomplete customer data from causing the application to fail.

---

## 10. Missing Account Handling

Missing account information is treated as an expected data-quality scenario.

The application does not terminate when a ticket references an unavailable account.

Instead, the system provides an appropriate message indicating that account information is unavailable and continues processing the ticket.

For example, the application may display:

"Account information is not available for this ticket."

The system can still perform:

- Ticket analysis.
- Risk assessment.
- Ticket summarization.
- Knowledge-base retrieval.
- Category classification.
- Sentiment analysis.
- Priority determination.
- Recommended action generation.
- AI response generation.

This demonstrates defensive handling of incomplete customer data.

---

## 11. Knowledge Base

The project contains an internal knowledge base stored in Markdown format.

The knowledge base is organized into the following categories:

knowledge-base/

billing/
onboarding/
products/
troubleshooting/

The documentation covers common support topics such as:

- Billing and subscription issues.
- Product information.
- Product configuration.
- Onboarding.
- Authentication.
- Single Sign-On.
- Troubleshooting.
- Integrations.

The knowledge base allows the system to retrieve relevant internal documentation based on the customer's ticket.

---

## 12. Knowledge Base Loading

Knowledge-base processing is implemented in:

src/utils/kb_loader.py

The loader reads the Markdown files from the knowledge-base directory and prepares them for retrieval.

The documents are processed into smaller chunks so that relevant sections can be retrieved instead of sending entire documents to the model.

The knowledge-base loader also preserves metadata such as the document source and category.

This allows the final triage result to identify which knowledge-base documents were used.

---

## 13. Knowledge Base Retrieval

The Knowledge Base Retriever is implemented in:

src/triage/retriever.py

The retriever uses the ticket subject and description to create a search query.

The query is compared against knowledge-base content to identify relevant documents.

The retrieval process consists of:

1. Reading the knowledge-base documents.
2. Splitting documents into chunks.
3. Converting text into numerical representations.
4. Comparing the ticket query with knowledge-base content.
5. Ranking relevant results.
6. Returning the top matching results.
7. Removing duplicate knowledge sources before displaying them.

The retriever provides the Triage Agent with relevant documentation that can help support the customer's issue.

---

## 14. Ticket Summarization

The Ticket Summarizer is implemented in:

src/tam/summarizer.py

The summarizer creates a concise representation of the available customer and ticket context.

The summary can contain:

- Ticket subject.
- Ticket description.
- Customer account information.
- Previous ticket history.
- Relevant customer context.

The summary is useful for providing a compact representation of the customer's situation to the triage process.

If the ticket description is missing, the system continues using the available information.

---

## 15. Risk Detection

Risk detection is implemented in:

src/tam/risk_detector.py

The Risk Detector analyzes the ticket for predefined high-risk indicators.

Potential risk indicators may include:

- Critical issues.
- Urgent requests.
- Security-related concerns.
- Severe access problems.
- Significant failures.
- Other predefined high-risk terms or conditions.

The risk assessment produces information such as:

- Risk level.
- Whether the ticket is high risk.
- Reasons for the risk assessment.

High-risk tickets can receive higher priority and an escalation recommendation.

The risk detector is designed as a separate component so that more advanced risk models can be introduced later.

---

## 16. Ticket Classification

Ticket classification is implemented inside the Triage Agent.

The current prototype uses deterministic keyword-based classification.

The supported categories are:

- billing
- authentication
- technical
- onboarding
- general

Examples include:

Billing:

Issues involving invoices, payments, subscriptions, charges, or refunds.

Authentication:

Issues involving login, passwords, authentication, SSO, access, or locked accounts.

Technical:

Issues involving errors, bugs, crashes, failures, integrations, or functionality not working.

Onboarding:

Issues involving setup, configuration, onboarding, or getting started.

General:

Issues that do not match the predefined categories.

The deterministic approach provides predictable behavior during development and testing.

---

## 17. Sentiment Classification

The system also estimates the sentiment of the customer's ticket.

The supported sentiment values are:

- positive
- neutral
- negative

The current implementation uses a lightweight rule-based approach.

Examples of negative indicators include:

- angry
- frustrated
- urgent
- critical
- failed
- failure
- cannot
- unable
- not working
- problem
- issue

Examples of positive indicators include:

- thank
- thanks
- great
- appreciate
- happy

The system compares positive and negative indicators and determines the resulting sentiment.

This approach is intentionally simple and deterministic for the current prototype.

A production implementation could replace this with an LLM-based sentiment classifier or a dedicated NLP model.

---

## 18. Priority Determination

Priority is determined using the risk assessment.

The current prototype follows a simple rule:

If the ticket is identified as high risk, the priority is set to high.

If the ticket is not high risk, the priority is set to normal.

This approach ensures that tickets containing high-risk indicators can be escalated appropriately.

A production implementation could use additional signals such as:

- Customer account tier.
- Business impact.
- Number of affected users.
- SLA requirements.
- Historical severity.
- Security classification.
- Revenue impact.

---

## 19. Recommended Action

The system generates a recommended action based on the ticket category and risk assessment.

Examples include:

For billing issues:

"Review the customer's billing and subscription information."

For authentication issues:

"Review authentication and account-access configuration."

For technical issues:

"Investigate the technical issue using the relevant troubleshooting guidance."

For onboarding issues:

"Provide the customer with the relevant onboarding and setup guidance."

For high-risk tickets:

"Escalate to the appropriate support team immediately because high-risk indicators were detected."

For general tickets:

"Review the ticket and provide appropriate support based on the available context."

These recommendations are designed to provide an initial action for the support team.

---

## 20. Triage Agent

The Triage Agent is implemented in:

src/triage/agent.py

It acts as the central orchestration layer of the application.

The Triage Agent coordinates:

- Account Service.
- Risk Detector.
- Ticket Summarizer.
- Knowledge Base Retriever.
- Prompt Builder.
- LLM Client.
- Ticket classification.
- Sentiment classification.
- Priority determination.
- Recommended action generation.
- Structured result creation.

The general processing sequence is:

1. Receive a ticket ID.
2. Build customer context.
3. Validate that the ticket exists.
4. Build a search query from the ticket.
5. Retrieve relevant knowledge-base documents.
6. Assess ticket risk.
7. Generate customer and ticket summary.
8. Build the triage prompt.
9. Send the prompt to the LLM client.
10. Determine ticket category.
11. Determine sentiment.
12. Determine priority.
13. Generate recommended action.
14. Collect knowledge sources.
15. Remove duplicate knowledge sources.
16. Create the structured TriageResult.
17. Validate the result using Pydantic.
18. Return the final triage result.

---

## 21. Prompt Engineering

Prompt construction is implemented in:

src/triage/prompts.py

The prompt builder combines the available context before sending it to the LLM client.

The prompt can include:

- Ticket information.
- Customer information.
- Previous ticket history.
- Risk assessment.
- Ticket summary.
- Relevant knowledge-base content.

The project separates system instructions from the ticket-specific user prompt.

This separation makes the prompt architecture easier to maintain and modify.

The prompts can also be versioned in:

prompts/versions/

This allows future prompt improvements to be tracked independently.

---

## 22. LLM Client

The LLM interface is implemented in:

src/utils/llm_client.py

The LLM client provides an abstraction between the Triage Agent and the actual language model.

This design allows the application to use a development/mock model during testing while keeping the main triage logic independent of a specific LLM provider.

The current development mode returns a deterministic response such as:

"Development-mode response. The ticket context was processed successfully. A production LLM should generate the final classification, reasoning, and recommended response."

This behavior is intentional.

It allows the complete application workflow to be tested without requiring a production API key.

A production model can be connected later without redesigning the entire application.

---

## 23. Environment Configuration

Environment configuration is handled using a .env file.

The repository contains:

.env.example

The local .env file is intentionally excluded from Git.

Example configuration:

LLM_API_KEY=
LLM_MODEL=development-mock

The API key should never be hard-coded into Python source files or committed to GitHub.

For production usage, the appropriate LLM API key and model configuration can be supplied through environment variables.

---

## 24. Structured Output

The final triage result is defined using Pydantic models.

The implementation is located in:

src/models.py

The structured result contains fields such as:

- ticket_id
- category
- priority
- sentiment
- is_high_risk
- risk_level
- risk_reasons
- recommended_action
- response
- knowledge_sources

Pydantic validation ensures that the application produces a predictable and structured result.

This also prevents invalid category, priority, sentiment, or other structured values from being silently accepted.

---

## 25. Streamlit Application

The user interface is implemented in:

app/streamlit_app.py

The application provides an interactive interface for support ticket analysis.

The main interface features include:

- Ticket search.
- Category filtering.
- Ticket selection.
- Ticket analysis.
- Ticket details.
- Customer context.
- Risk assessment.
- Customer summary.
- Triage result.
- Recommended action.
- AI response.
- Knowledge-base sources.

The user can search for a ticket using its ticket ID or subject.

The user can also filter tickets by category.

After selecting a ticket, the user can run the analysis and view the generated result.

---

## 26. User Experience

The application displays the analysis in clearly separated sections.

The main sections are:

Ticket Details

Displays:

- Ticket ID.
- Subject.
- Description.

Customer Context

Displays available customer account information.

If no account is available, the system clearly indicates that account information is unavailable.

Risk Assessment

Displays:

- Risk level.
- High-risk status.
- Risk reasons.

Customer Summary

Displays:

- Ticket summary.
- Previous ticket history.
- Available customer context.

Triage Result

Displays:

- Category.
- Priority.
- Sentiment.

Recommended Action

Displays the action that the support team should consider.

AI Response

Displays the response returned by the configured LLM client.

Knowledge Sources

Displays the knowledge-base documents used during retrieval.

Duplicate knowledge sources are removed before display.

---

## 27. Example Triage Scenario

Example ticket:

Ticket ID:

TKT-10005

Subject:

SSO configuration not working for new users — AnalyticsHub

The application can analyze the ticket and produce a result such as:

Category:

authentication

Priority:

normal

Sentiment:

negative

Risk Level:

low

Recommended Action:

Review authentication and account-access configuration.

Knowledge Sources:

troubleshooting/authentication-sso.md

onboarding/onboarding-guide.md

If customer account information is unavailable, the system continues processing the ticket rather than failing.

---

## 28. Error Handling

The application contains handling for common failure scenarios.

### Missing Ticket

If the requested ticket does not exist, the system raises a controlled error indicating that the ticket could not be found.

### Missing Account

If a ticket does not have a matching account, the system continues with an empty or unavailable customer context.

### Missing Description

If a ticket has no description, the system uses the available ticket information and displays that the description is unavailable.

### Invalid Data

The validation layer is used to identify invalid structured data.

### LLM Development Mode

If the application is running in development mode, the mock LLM client provides a deterministic response instead of making an external API request.

---

## 29. Testing Strategy

The project contains a dedicated tests directory.

The tests cover individual components as well as complete workflows.

The current test modules are:

test_data_loader.py

test_end_to_end.py

test_kb_chunker.py

test_kb_loader.py

test_llm_client.py

test_missing_account.py

test_models.py

test_prompts.py

test_retriever.py

test_risk_detector.py

test_summarizer.py

test_triage_agent.py

test_triage_flow.py

---

## 30. Unit Testing

Individual components are tested independently.

The unit tests cover:

- Data loading.
- Knowledge-base chunking.
- Knowledge-base loading.
- Knowledge retrieval.
- LLM client behavior.
- Pydantic model validation.
- Prompt generation.
- Risk detection.
- Ticket summarization.
- Triage agent behavior.

This makes it easier to identify problems at the component level.

---

## 31. Integration Testing

Integration tests verify that multiple components work correctly together.

The integration flow includes:

- Account Service with ticket data.
- Risk Detector with ticket information.
- Summarizer with customer context.
- Retriever with the knowledge base.
- Prompt builder with triage context.
- LLM client with the Triage Agent.
- Triage Agent with the structured result model.

---

## 32. End-to-End Testing

The project also includes end-to-end testing.

The end-to-end test verifies that a complete ticket can move through the application pipeline.

The tested flow includes:

Ticket Selection

to

Ticket Retrieval

to

Customer Context

to

Risk Assessment

to

Knowledge Retrieval

to

Triage Processing

to

Classification

to

Recommended Action

to

LLM Response

to

Final Structured Result

The project also tests:

- Valid tickets.
- Missing-account tickets.
- Invalid tickets.

This ensures that the application handles both normal and edge-case scenarios.

---

## 33. Running the Tests

First activate the virtual environment.

On Windows:

.venv\Scripts\Activate.ps1

Install the required packages:

pip install -r requirements.txt

Individual tests can then be executed using:

python -m tests.test_data_loader

python -m tests.test_end_to_end

python -m tests.test_kb_chunker

python -m tests.test_kb_loader

python -m tests.test_llm_client

python -m tests.test_missing_account

python -m tests.test_models

python -m tests.test_prompts

python -m tests.test_retriever

python -m tests.test_risk_detector

python -m tests.test_summarizer

python -m tests.test_triage_agent

python -m tests.test_triage_flow

All tests are designed to provide clear success or failure output.

---

## 34. Running the Application

After activating the virtual environment and installing the dependencies, run:

python -m streamlit run app/streamlit_app.py

The application will normally be available at:

http://localhost:8501

The Streamlit interface allows the user to search and analyze support tickets interactively.

---

## 35. Data Validation Command

Before running the application, the dataset can be validated using:

python -m src.check_data

This confirms that the data files can be loaded and that the expected ticket and account data are available.

---

## 36. Installation

Clone the repository:

git clone <repository-url>

Navigate into the project:

cd zycus-ai-support

Create a virtual environment:

python -m venv .venv

Activate the environment on Windows:

.venv\Scripts\Activate.ps1

Install the dependencies:

pip install -r requirements.txt

Create the local environment file:

copy .env.example .env

Update the .env file with the appropriate configuration if a production LLM is being used.

---

## 37. Dependencies

The main project dependencies are:

pandas

numpy

pydantic

python-dotenv

scikit-learn

streamlit

The dependency list is maintained in:

requirements.txt

---

## 38. Security Considerations

The project follows basic security practices.

API credentials are stored in environment variables.

The local .env file is excluded from Git.

The .env.example file contains placeholders instead of real credentials.

The application does not require API credentials when operating in development/mock mode.

Production deployment should use secure secret management rather than storing credentials directly in source code.

---

## 39. Data Quality Considerations

The supplied support dataset contains incomplete relationships between tickets and customer accounts.

Not every ticket has a matching account.

The application explicitly handles this situation rather than assuming perfect data.

This demonstrates an important production-oriented design principle:

Application logic should be resilient to incomplete or inconsistent source data.

The system can still provide useful ticket analysis even when customer account information is unavailable.

---

## 40. Design Decisions

The application follows a separation-of-concerns approach.

The main responsibilities are divided as follows:

data_loader.py

Responsible for loading structured data.

kb_loader.py

Responsible for loading and preparing knowledge-base documents.

account_service.py

Responsible for customer account context.

risk_detector.py

Responsible for identifying risk indicators.

summarizer.py

Responsible for generating ticket and customer summaries.

retriever.py

Responsible for knowledge-base retrieval.

prompts.py

Responsible for prompt construction.

llm_client.py

Responsible for interaction with the configured language model.

models.py

Responsible for structured result validation.

agent.py

Responsible for orchestrating the complete triage workflow.

streamlit_app.py

Responsible for the user interface.

This modular design makes the system easier to maintain, test, and extend.

---

## 41. Why a Triage Agent Is Used

The Triage Agent provides a central orchestration layer instead of placing all business logic directly inside the Streamlit application.

This provides several benefits:

- Easier testing.
- Separation between UI and business logic.
- Reusable ticket analysis.
- Easier integration with APIs.
- Easier integration with external LLMs.
- Easier future migration to an agentic architecture.
- Better maintainability.

The Streamlit application is therefore primarily responsible for presenting information, while the Triage Agent handles the analysis workflow.

---

## 42. Current Prototype Limitations

The current implementation is a development prototype.

The main limitations are:

1. The LLM currently operates in development/mock mode.
2. Ticket classification currently uses deterministic keyword rules.
3. Sentiment classification currently uses deterministic keyword rules.
4. Priority logic is currently based primarily on risk detection.
5. JSON files are used instead of a production database.
6. Knowledge retrieval uses a lightweight retrieval approach.
7. There is no production authentication system.
8. There is no production monitoring system.
9. There is no persistent conversation memory.
10. There is no production-grade ticket management integration.

These limitations are intentional because the current objective is to demonstrate the complete architecture and working triage pipeline.

---

## 43. Production Improvements

The following improvements could be implemented for production deployment.

### Production LLM

Connect the LLM client to a production model provider.

### Database

Replace JSON files with a production database such as PostgreSQL.

### Vector Database

Use a persistent vector database for scalable semantic retrieval.

### Improved Retrieval

Introduce embedding-based semantic search and hybrid keyword plus semantic retrieval.

### Advanced Classification

Use trained models or LLM-based classification for category and sentiment.

### Authentication

Add authentication and authorization for support agents.

### Monitoring

Add application logs, metrics, tracing, and model monitoring.

### Human Escalation

Introduce human-in-the-loop workflows for high-risk tickets.

### Evaluation

Add automated evaluation for:

- Classification accuracy.
- Retrieval quality.
- Response quality.
- Risk detection accuracy.
- Hallucination detection.

### CI/CD

Add automated testing and deployment pipelines.

---

## 44. Future AI Capabilities

The architecture can be extended into a more advanced AI support platform.

Potential improvements include:

- Retrieval-Augmented Generation.
- Embedding-based semantic search.
- Vector databases.
- LLM-based ticket classification.
- LLM-based sentiment analysis.
- Automated escalation.
- Conversation memory.
- Multi-agent support workflows.
- Customer-specific recommendations.
- Support response quality evaluation.
- Human feedback collection.
- Continuous improvement from support-agent feedback.

The current modular architecture provides a foundation for these capabilities.

---

## 45. Development Mode

The application currently supports development mode.

Development mode is useful because it allows the entire application to be tested without requiring an external LLM service.

The configuration can use:

LLM_MODEL=development-mock

In this mode, the LLM client returns a predictable response.

This makes development and testing:

- Faster.
- More reliable.
- Less dependent on external services.
- Safer because API credentials are not required.

When a production LLM is configured, the same Triage Agent architecture can use the production client.

---

## 46. Validation Results

The project has been tested across the major components.

The validated components include:

- Data loader.
- Knowledge-base loader.
- Knowledge-base chunking.
- Knowledge retriever.
- Account service.
- Missing-account handling.
- Pydantic models.
- Prompt generation.
- LLM client.
- Risk detector.
- Ticket summarizer.
- Triage agent.
- Complete triage flow.
- End-to-end ticket processing.
- Streamlit application.

The application has successfully processed valid tickets, missing-account tickets, and invalid-ticket scenarios.

---

## 47. Example Application Output

A successful ticket analysis can contain the following information:

Ticket Details:

Ticket ID: TKT-10005

Subject:

SSO configuration not working for new users — AnalyticsHub

Customer Context:

Account information is not available for this ticket.

Risk Assessment:

Risk Level: low

No high-risk indicators detected.

Customer Summary:

Subject: SSO configuration not working for new users — AnalyticsHub

Issue: No description available.

Triage Result:

Category: authentication

Priority: normal

Sentiment: negative

Recommended Action:

Review authentication and account-access configuration.

AI Response:

Development-mode response.

Knowledge Sources:

troubleshooting/authentication-sso.md

onboarding/onboarding-guide.md

This demonstrates that the system can continue to produce a useful triage result even when some customer information is unavailable.

---

## 48. Git and Repository Management

The repository excludes local and generated files that should not be committed.

Examples include:

.env

.venv/

__pycache__/

*.pyc

.vscode/

.pytest_cache/

Operating-system temporary files.

The .env file is specifically excluded to prevent accidental exposure of API credentials.

The repository contains .env.example so that other developers know which environment variables are required.

---

## 49. Repository Readiness

Before submitting or sharing the project, verify the following:

- README is present.
- .gitignore is configured.
- .env is not committed.
- .venv is not committed.
- API keys are not committed.
- Data files are present.
- Knowledge-base documents are present.
- Source code is present.
- Tests are present.
- Streamlit application runs successfully.
- Data validation passes.
- End-to-end tests pass.
- Triage flow tests pass.
- Missing-account handling works.
- Knowledge sources are displayed without duplicates.
- Development LLM mode works.

---

## 50. Conclusion

Zycus AI Support Triage demonstrates how customer support automation can combine structured data processing, customer context, risk detection, knowledge retrieval, deterministic business logic, LLM integration, and structured validation into a single support workflow.

The application is designed with modular components so that individual services can be tested independently and replaced or upgraded as the project moves toward production.

The current implementation provides a functional development prototype with:

- Ticket search.
- Ticket analysis.
- Customer context.
- Missing-account handling.
- Risk assessment.
- Ticket summarization.
- Knowledge-base retrieval.
- Category classification.
- Priority determination.
- Sentiment analysis.
- Recommended support actions.
- LLM response generation.
- Structured Pydantic validation.
- Streamlit user interface.
- Unit testing.
- Integration testing.
- End-to-end testing.

The architecture provides a foundation for future production capabilities such as RAG, vector databases, production LLMs, database integration, automated escalation, monitoring, evaluation, and agentic support workflows.

---

## 51. Author

Developed as an AI-assisted customer support triage prototype for technical evaluation.
