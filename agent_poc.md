class CoordinatorAgent:
    def handle_request(request):
        intent = llm.classify_intent(request)
        agent = select_agent(intent)
        context = build_context(request, intent)
        result = agent.run(context)
        return combine_results(result)

class SubAgent:
    def run(context):
        plan = llm.plan_tool_calls(context, tools)
        results = [call_tool(step) for step in plan]
        return llm.synthesize(context, results)

# Specialized agents
AWSCostAgent(SubAgent)          # usage, billing, savings
ArchitectureAgent(SubAgent)     # topology, best practices
ProblemDetectionAgent(SubAgent) # configs, security, scaling
RecommendationAgent(SubAgent)   # rank findings, action items

class EvaluationAgent:
    def evaluate(test_case, trace, response):
        return {
            "agent_selection": check_selection(test_case, trace),
            "tool_usage": check_tools(test_case, trace),
            "accuracy": score_accuracy(test_case, response),
            "hallucination": detect_hallucination(trace, response),
        }

class AgentEvaluationSuite:
    def run(test_cases):
        for case in test_cases:
            response, trace = coordinator.handle_request(case.input)
            evaluate(case, trace, response)
