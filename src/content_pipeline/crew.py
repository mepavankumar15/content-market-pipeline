import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class ContentPipelineCrew:
    """Content Pipeline Crew"""
    
    # Load configs relative to this file
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Initialize the custom LLM since we're using LiteLLM/xAI via crewai.LLM
        self.llm = LLM(
            model="xai/grok-4.3",
            temperature=0.7,
            api_key=os.environ.get("XAI_API_KEY")
        )

    @agent
    def trend_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_researcher'],
            verbose=True,
            llm=self.llm
        )

    @agent
    def seo_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_analyst'],
            verbose=True,
            llm=self.llm
        )

    @agent
    def blog_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['blog_writer'],
            verbose=True,
            llm=self.llm
        )

    @agent
    def social_repurposer(self) -> Agent:
        return Agent(
            config=self.agents_config['social_repurposer'],
            verbose=True,
            llm=self.llm
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.trend_researcher()
        )

    @task
    def seo_task(self) -> Task:
        return Task(
            config=self.tasks_config['seo_task'],
            agent=self.seo_analyst(),
            context=[self.research_task()]
        )

    @task
    def blog_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_task'],
            agent=self.blog_writer(),
            context=[self.research_task(), self.seo_task()]
        )

    @task
    def social_task(self) -> Task:
        return Task(
            config=self.tasks_config['social_task'],
            agent=self.social_repurposer(),
            context=[self.blog_task()]
        )

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
