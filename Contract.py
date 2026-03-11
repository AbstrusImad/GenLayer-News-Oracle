# v0.1.0
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *

import json
import typing


class NewsOracle(gl.Contract):
    """
    News Verification Oracle - A GenLayer Intelligent Contract that verifies
    the truthfulness of news articles by fetching their content from the web
    and using AI to analyze their credibility.
    
    This contract leverages GenLayer's unique capabilities:
    - Native web access to read news articles
    - LLM-powered analysis for credibility assessment
    - Decentralized consensus for verification results
    """

    # State variables
    total_verifications: u256
    
    def __init__(self):
        """Initialize the News Oracle contract."""
        self.total_verifications = u256(0)

    @gl.public.write
    def verify_news(self, news_url: str, claim: str) -> typing.Any:
        """
        Verify a news article's credibility by fetching its content and
        analyzing it with AI.
        
        Args:
            news_url (str): The URL of the news article to verify.
            claim (str): The specific claim being made that needs verification.
        
        Returns:
            dict: Verification result with verdict, confidence, and analysis.
        """

        article_url = news_url
        news_claim = claim

        def analyze_article() -> typing.Any:
            # Fetch the web page content using GenLayer's native web access
            web_data = gl.nondet.web.render(article_url, mode="text")

            task = f"""
You are a professional fact-checker and news verification expert.

CLAIM TO VERIFY:
"{news_claim}"

SOURCE ARTICLE URL: {article_url}

ARTICLE CONTENT:
{web_data}
End of article content.

Your task is to analyze the article and determine whether the claim is supported, 
contradicted, or if there's not enough information to make a determination.

Consider the following factors:
1. Does the article directly support or contradict the claim?
2. Are there specific facts, quotes, or data that back or refute the claim?
3. Is the source generally considered reliable?
4. Are there any logical fallacies or misleading information?
5. Is the claim taken out of context?

Respond ONLY with the following JSON format, nothing else:
{{
    "verdict": str, // One of: "TRUE", "FALSE", "PARTIALLY_TRUE", "UNVERIFIABLE", "MISLEADING"
    "confidence": int, // Confidence score from 0 to 100
    "summary": str, // A brief 1-2 sentence summary of the verification result
    "key_evidence": str, // The most important piece of evidence from the article
    "reasoning": str // Detailed reasoning for the verdict (2-3 sentences)
}}
It is mandatory that you respond only using the JSON format above,
nothing else. Don't include any other words or characters,
your output must be only JSON without any formatting prefix or suffix.
This result should be perfectly parsable by a JSON parser without errors.
"""
            result = (
                gl.nondet.exec_prompt(task).replace("```json", "").replace("```", "")
            )
            return json.loads(result)

        # Use prompt_comparative for consensus - validators independently verify
        # and compare results using LLM comparison
        result_json = gl.eq_principle.prompt_comparative(
            analyze_article,
            principle="`verdict` field must be exactly the same. `confidence` must be within 15 points. `key_evidence` and `reasoning` must convey the same conclusion."
        )

        self.total_verifications = u256(int(self.total_verifications) + 1)

        return result_json

    @gl.public.write
    def verify_claim_only(self, claim: str) -> typing.Any:
        """
        Verify a claim without a specific article URL. The contract will
        use its AI capabilities to assess the claim based on general knowledge.
        
        Args:
            claim (str): The claim to verify.
            
        Returns:
            dict: Verification result with verdict, confidence, and analysis.
        """

        news_claim = claim

        def assess_claim() -> typing.Any:
            task = f"""
You are a professional fact-checker and news verification expert.

CLAIM TO VERIFY:
"{news_claim}"

Analyze this claim based on your knowledge. Consider:
1. Is this claim factually accurate based on widely known information?
2. Are there well-documented sources that support or refute this claim?
3. Is this a common misconception or misinformation?
4. Could this be satire or taken out of context?

Respond ONLY with the following JSON format, nothing else:
{{
    "verdict": str, // One of: "TRUE", "FALSE", "PARTIALLY_TRUE", "UNVERIFIABLE", "MISLEADING"
    "confidence": int, // Confidence score from 0 to 100
    "summary": str, // A brief 1-2 sentence summary of the verification result
    "reasoning": str // Detailed reasoning for the verdict (2-3 sentences)
}}
It is mandatory that you respond only using the JSON format above,
nothing else. Don't include any other words or characters,
your output must be only JSON without any formatting prefix or suffix.
This result should be perfectly parsable by a JSON parser without errors.
"""
            result = (
                gl.nondet.exec_prompt(task).replace("```json", "").replace("```", "")
            )
            return json.loads(result)

        result_json = gl.eq_principle.prompt_comparative(
            assess_claim,
            principle="`verdict` field must be exactly the same. `confidence` must be within 20 points. `reasoning` must reach the same conclusion."
        )

        self.total_verifications = u256(int(self.total_verifications) + 1)

        return result_json

    @gl.public.write
    def cross_verify_news(self, claim: str, source_urls: str) -> typing.Any:
        """
        Cross-reference a claim against multiple news sources for enhanced
        verification. Takes a comma-separated list of URLs.
        
        Args:
            claim (str): The claim to verify.
            source_urls (str): Comma-separated list of URLs to cross-reference.
            
        Returns:
            dict: Cross-verification result with per-source analysis.
        """

        news_claim = claim
        urls = [url.strip() for url in source_urls.split(",")]

        def cross_reference() -> typing.Any:
            # Fetch content from multiple sources
            sources_content = []
            for i, url in enumerate(urls[:3]):  # Limit to 3 sources for efficiency
                try:
                    web_data = gl.nondet.web.render(url, mode="text")
                    sources_content.append(f"SOURCE {i+1} ({url}):\n{web_data}\n---END SOURCE {i+1}---")
                except Exception:
                    sources_content.append(f"SOURCE {i+1} ({url}):\n[Failed to fetch]\n---END SOURCE {i+1}---")

            all_sources = "\n\n".join(sources_content)

            task = f"""
You are a professional fact-checker performing cross-source verification.

CLAIM TO VERIFY:
"{news_claim}"

SOURCES:
{all_sources}

Analyze all sources and cross-reference them to determine the claim's validity.
Consider:
1. Do the sources agree or disagree with each other?
2. What is the consensus across sources?
3. Are there any contradictions between sources?
4. Which sources provide the strongest evidence?

Respond ONLY with the following JSON format, nothing else:
{{
    "verdict": str, // One of: "TRUE", "FALSE", "PARTIALLY_TRUE", "UNVERIFIABLE", "MISLEADING"
    "confidence": int, // Confidence score from 0 to 100
    "summary": str, // A brief 1-2 sentence summary
    "sources_agree": bool, // Whether the sources generally agree
    "source_count": int, // Number of sources successfully analyzed
    "reasoning": str // Detailed cross-reference reasoning (2-3 sentences)
}}
It is mandatory that you respond only using the JSON format above,
nothing else. Don't include any other words or characters,
your output must be only JSON without any formatting prefix or suffix.
This result should be perfectly parsable by a JSON parser without errors.
"""
            result = (
                gl.nondet.exec_prompt(task).replace("```json", "").replace("```", "")
            )
            return json.loads(result)

        result_json = gl.eq_principle.prompt_comparative(
            cross_reference,
            principle="`verdict` must be exactly the same. `sources_agree` must be the same. `confidence` must be within 15 points. `reasoning` must reach the same overall conclusion."
        )

        self.total_verifications = u256(int(self.total_verifications) + 1)

        return result_json

    @gl.public.view
    def get_stats(self) -> dict[str, typing.Any]:
        """Get the oracle's statistics."""
        return {
            "total_verifications": int(self.total_verifications),
        }
