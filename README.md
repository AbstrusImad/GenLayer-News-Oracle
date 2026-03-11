News Verification Oracle — An Intelligent Contract that leverages GenLayer's unique capabilities (native web access + LLM-powered analysis) to verify the truthfulness of news articles and claims in a decentralized manner.

Key Features:
• verify_news: Receives a news article URL and a specific claim, fetches the article content using gl.nondet.web.render(), and uses AI to analyze its credibility — returning a structured verdict (TRUE/FALSE/PARTIALLY_TRUE/MISLEADING/UNVERIFIABLE) with confidence score, key evidence, and detailed reasoning.
• verify_claim_only: Verifies a claim using only AI knowledge without requiring a source URL — useful for quick fact-checking of widely known statements.
• cross_verify_news: Cross-references a claim against up to 3 different news sources simultaneously, comparing how they report the same event and checking for consistency.

The contract uses gl.eq_principle.prompt_comparative for consensus, ensuring validators independently verify each analysis and agree on the verdict before finalizing results on-chain.

Deployed on Asimov Testnet.
Contract address: 0x6ce642c37b919ce3c94f605318e9335a94099fdb4f091ada791e9fc01eaeeac7
