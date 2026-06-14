from crewai import Task

def create_research_task(agent):
    return Task(
        description="Research the topic '{topic}' and provide:\n1. A brief overview (2-3 sentences)\n2. 3 compelling content angles\n3. Target audience description\n4. 5 key talking points",
        expected_output="Structured research brief",
        agent=agent
    )

def create_seo_task(agent, context_tasks):
    return Task(
        description="Based on the research brief, provide:\n1. 5 SEO keywords (ranked by priority)\n2. Suggested blog post title (include primary keyword)\n3. Meta description (max 155 chars)",
        expected_output="SEO brief with keywords, title, meta description",
        agent=agent,
        context=context_tasks
    )

def create_blog_task(agent, context_tasks):
    return Task(
        description="Write a complete blog post about '{topic}' using the research brief and SEO keywords. Format:\n- Title (use suggested SEO title)\n- Introduction (hook the reader)\n- Section 1 with H2\n- Section 2 with H2\n- Section 3 with H2\n- Conclusion\n- CTA (e.g. comment, share, subscribe)",
        expected_output="Full blog post in Markdown format",
        agent=agent,
        context=context_tasks
    )

def create_social_task(agent, context_tasks):
    return Task(
        description="Repurpose the blog post into social media content. Return clearly labelled sections:\n## LINKEDIN POST\n## TWITTER THREAD (Tweet 1, Tweet 2, Tweet 3, Tweet 4, Tweet 5, Tweet 6, Tweet 7)\nEach tweet must be under 280 characters. Use hooks, stats, insights, and end with a CTA.\n## INSTAGRAM CAPTION",
        expected_output="All 3 platform posts, clearly separated sections containing the social media posts.",
        agent=agent,
        context=context_tasks
    )
