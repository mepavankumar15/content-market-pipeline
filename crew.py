import os
import patch_chromadb  # Must run before crewai/chromadb imports
from crewai import Crew, Process, LLM

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


def build_crew():
    """Builds and returns the Content Marketing Pipeline Crew."""
    llm = LLM(
        model="xai/grok-4.3",
        temperature=0.7,
        api_key=os.environ.get("XAI_API_KEY")
    )

    # Create agents
    trend_researcher = create_trend_researcher(llm)
    seo_analyst = create_seo_analyst(llm)
    blog_writer = create_blog_writer(llm)
    social_repurposer = create_social_repurposer(llm)

    # Create tasks with dependencies
    research_task = create_research_task(trend_researcher)
    seo_task = create_seo_task(seo_analyst, [research_task])
    blog_task = create_blog_task(blog_writer, [research_task, seo_task])
    social_task = create_social_task(social_repurposer, [blog_task])

    # Build the crew
    crew = Crew(
        agents=[trend_researcher, seo_analyst, blog_writer, social_repurposer],
        tasks=[research_task, seo_task, blog_task, social_task],
        process=Process.sequential,
        verbose=True,
        memory=False
    )

    return crew
