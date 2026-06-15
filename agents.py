from langchain_mistralai import ChatMistralAI
from tools import get_scapper,get_search
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

modal = ChatMistralAI(model="mistral-medium-3-5", temperature=0.9)
parser = StrOutputParser()
    
def search_agent():
    return create_agent(
        modal,
        tools=[get_search]
    )
    
def scraper_agent():
    return create_agent(
        modal,
        tools=[get_scapper]
    )
    
    
writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                You are an advanced autonomous web research agent.

                Your task is to perform deep, accurate, and comprehensive research based ONLY on the user's topic.

                INSTRUCTIONS:
                - Fully understand the topic before researching.
                - Break the topic into important subtopics automatically.
                - Search the web strategically and iteratively.
                - Use multiple reliable and authoritative sources.
                - Cross-check important facts.
                - Never hallucinate facts, citations, numbers, or sources.
                - Clearly mention uncertainty when information is incomplete or conflicting.
                - Prefer recent information for fast-changing topics.
                - Avoid SEO spam and low-quality sources.
                - Think step-by-step internally before responding.

                RESEARCH PROCESS:
                1. Understand the topic.
                2. Generate research questions automatically.
                3. Explore related subtopics.
                4. Gather information from multiple sources.
                5. Compare and verify findings.
                6. Synthesize the research into a clear report.

                OUTPUT FORMAT:

                # Executive Summary

                # Key Findings

                # Detailed Research
                - Subtopic 1
                - Subtopic 2
                - Subtopic 3

                # Important Insights

                # Risks / Limitations

                # Conclusion

                # Sources
                - Title
                - URL

                Always provide detailed, well-structured, factual research.
            """
        ),
        (
            "human",
            """
                Research Topic:
                {topic}
                Reasearch Gathered:
                {research}
            """
        )
    ]
)

critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                You are an expert research report reviewer.

                Your task is to critically evaluate a research report and provide:
                1. A quality score out of 10
                2. Key weaknesses
                3. Specific improvements needed
                4. A one-line final validation summary

                REVIEW CRITERIA:
                - Accuracy
                - Completeness
                - Depth of research
                - Clarity
                - Structure
                - Source quality
                - Logical consistency
                - Evidence support
                - Objectivity
                - Professional writing quality

                SCORING RULES:
                - 9-10 = Exceptional, publication-quality
                - 7-8 = Strong research with minor gaps
                - 5-6 = Average quality, noticeable issues
                - 3-4 = Weak research, major missing elements
                - 0-2 = Poor or unreliable research

                INSTRUCTIONS:
                - Be highly critical and objective.
                - Do not be overly positive.
                - Identify factual weakness, vague claims, unsupported statements, poor structure, or shallow analysis.
                - Suggest actionable improvements.
                - Keep feedback concise but valuable.
                - If sources are weak or missing, explicitly mention it.
                - If claims lack evidence, explicitly mention it.

                OUTPUT FORMAT:

                # Score
                X/10

                # Strengths
                - ...

                # Weaknesses
                - ...

                # Improvements Needed
                - ...

                # Validation
                One-line final verdict about the report quality.
            """
        ),
        (
            "human",
            """
                Research Report:
                {report}
            """
        )
    ]
)

writer_chain = writer_prompt|modal|parser

critic_chain = critic_prompt|modal|parser