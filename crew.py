import os
from crewai import Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task

from agents import (
    create_trend_researcher,
    create_seo_analyst,
    create_blog_writer,
    create_social_repurposer
)
from tasks import (
    create_research_task,
    create_seo_task,
    create_blog_task,
    create_social_task
)

@CrewBase
class ContentPipelineCrew:
    """Content Pipeline Crew"""
    
    def __init__(self):
        # We assume XAI_API_KEY is in the environment
        self.llm = LLM(
            model="xai/grok-4.3",
            temperature=0.7,
            api_key=os.environ.get("XAI_API_KEY")
        )

    @agent
    def trend_researcher(self):
        return create_trend_researcher(self.llm)

    @agent
    def seo_analyst(self):
        return create_seo_analyst(self.llm)

    @agent
    def blog_writer(self):
        return create_blog_writer(self.llm)

    @agent
    def social_repurposer(self):
        return create_social_repurposer(self.llm)

    @task
    def research_task(self):
        return create_research_task(self.trend_researcher())

    @task
    def seo_task(self):
        return create_seo_task(self.seo_analyst(), [self.research_task()])

    @task
    def blog_task(self):
        return create_blog_task(self.blog_writer(), [self.research_task(), self.seo_task()])

    @task
    def social_task(self):
        return create_social_task(self.social_repurposer(), [self.blog_task()])

    @crew
    def crew(self) -> Crew:
        """Creates the Content Marketing Pipeline Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False
        )
