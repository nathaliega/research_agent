import time
from agents import Runner, trace
from duckduckgo_search import DDGS

from models import SearchResult
from research_agents.follow_up_agent import FollowUpDecisionResponse
from research_agents.follow_up_agent import follow_up_decision_agent
from research_agents.search_agent import search_agent
from research_agents.query_agent import QueryResponse, query_agent
from research_agents.synthesis_agent import synthesis_agent

class ResearchCoordinator:
    def __init__(self, query: str):
        self.query = query
        self.search_results = []
        self.iteration = 1

    async def research(self) -> str:
        with trace("Deep Research Workflow"):

            query_response = await self.generate_queries()
            await self.perform_research_for_queries(queries=query_response.queries)

            while self.iteration < 3:
                decision_response = await self.generate_followup()

                if not decision_response.should_follow_up:
                   break

                self.iteration += 1
                await self.perform_research_for_queries(queries=decision_response.queries)

            final_report = await self.synthesis_report()
            return final_report
            
    async def generate_queries(self) -> QueryResponse:
        # Run the query agent
        result = await Runner.run(query_agent, input=self.query)
        return result.final_output
        
    def duckduckgo_search(self, query: str):
        try:
            results = DDGS().text(query, region='us-en', safesearch='on', timelimit='y', max_results=3)
            return list(results)  # Convert generator to list
        except Exception as ex:
            print(f"Search error for query '{query}': {str(ex)}")
            return []

    async def perform_research_for_queries(self, queries: list[str]) -> None:
        # get all of the search results for each query
        all_search_results = {}
        for query in queries:
            search_results = self.duckduckgo_search(query)
            all_search_results[query] = search_results
            print(f"Found {len(search_results)} results for query: {query}")

        for query in queries:
            for result in all_search_results[query]:
                search_input = f"Title: {result['title']}\nURL: {result['href']}"
                agent_result = await Runner.run(search_agent, input=search_input)

                search_result = SearchResult(
                    title=result['title'],
                    url=result['href'],
                    summary=agent_result.final_output
                )

                self.search_results.append(search_result)
                print(f"Added search result: {result['title']}")

    async def synthesis_report(self) -> str:
        findings_text = f"Query: {self.query}\n\nSearch Results:\n"
        for i, result in enumerate(self.search_results, 1):
            findings_text += f"\n{i}. Title: {result.title}\n   URL: {result.url}\n   Summary: {result.summary}\n"

        result = await Runner.run(synthesis_agent, input=findings_text)
        return result.final_output
         
    async def generate_followup(self) -> FollowUpDecisionResponse:
        findings_text = f"Original Query: {self.query}\n\nCurrent Findings:\n"
        for i, result in enumerate(self.search_results, 1):
            findings_text += f"\n{i}. Title: {result.title}\n   URL: {result.url}\n   Summary: {result.summary}\n"

        result = await Runner.run(follow_up_decision_agent, input=findings_text)
        return result.final_output