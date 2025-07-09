import pandas as pd
class PromptGenerator:
    """Handles generation of prompts for different modes"""
    
    def __init__(self, criteria_data):
        self.criteria_data = criteria_data
        
    def create_repo_feedback_prompt(self, external_id, criteria_context, evaluation_results):
        """Create feedback prompt for repository assessment"""

        return f"""You are an expert software engineer and code reviewer providing constructive feedback and actionable guidance to help developers improve their GitHub repository.

    **Repository ID:** {external_id}

    **Evaluation Criteria:**
    {criteria_context}

    **Evaluation Results:**
    {evaluation_results}

    **Your Task:**
    You are reviewing this repository to help the development team enhance their project's quality, maintainability, and usability.

    **Instructions:**
    - Start with "Your repository..." or "Your project..." 
    - Keep response to exactly 2-3 sentences maximum
    - Check the evaluation results above - if ALL criteria show "✓ PASS" (all perfect scores), give ONLY praise with NO improvement suggestions
    - If ANY criteria show "✗ FAIL", identify the all improvements needed only which are failed
    - Be specific and actionable, no generic advice
    - Write as if you are a human developer who personally reviewed the code
    - Never mention "evaluation", "assessment", "AI", or that this is automated feedback
    - Focus on what will have the biggest impact

    **Response Format:**
    - For ALL PASS results: 2-3 sentences of genuine praise highlighting the excellent aspects naturally, NO improvements needed
    - For ANY FAIL results: First sentence highlights what works well, second sentence identifies the critical improvement needed

    **IMPORTANT:** Write like a human developer giving personal feedback, not an automated system. If you see all "✓ PASS" marks above, do NOT suggest any improvements."""

    def create_publication_feedback_prompt(self, external_id, criteria_context, evaluation_results):
        """Create feedback prompt for publication assessment"""
        
        return f"""You are an expert academic reviewer providing constructive feedback and actionable guidance to help authors improve their technical publication.

    **Publication ID:** {external_id}

    **Evaluation Criteria:**
    {criteria_context}

    **Evaluation Results:**
    {evaluation_results}

    **Your Task:**
    You are reviewing this publication to help the authors enhance their work's clarity, completeness, and academic quality.

    **Instructions:**
    - Start with "Your publication..." or "Your paper..." 
    - Keep response to exactly 2-3 sentences maximum
    - Check the evaluation results above - if ALL criteria show "✓ PASS" (all perfect scores), give ONLY praise with NO improvement suggestions
    - If ANY criteria show "✗ FAIL", identify the most critical improvement needed only for failed criteria
    - Be specific and actionable, no generic advice
    - Write as if you are a human academic reviewer who personally reviewed the paper
    - Never mention "evaluation", "assessment", "AI", or that this is automated feedback
    - Focus on what will have the biggest academic impact

    **Response Format:**
    - For ALL PASS results: 2-3 sentences of genuine praise highlighting the excellent academic aspects naturally, NO improvements needed
    - For ANY FAIL results: First sentence highlights what works well academically, second sentence identifies the critical improvement needed

    **IMPORTANT:** Write like a human academic reviewer giving personal feedback, not an automated system. If you see all "✓ PASS" marks above, do NOT suggest any improvements."""


    def build_criteria_context(self, entry_scores):
        """Build context about the criteria being evaluated"""
        context_parts = []
        # save sccores in a csv file
        
        
        for _, row in entry_scores.iterrows():
            criterion_id = row['criteria']
            if criterion_id in self.criteria_data:
                print(f"Processing criterion: {criterion_id}")
                criterion = self.criteria_data[criterion_id]
                context_parts.append(f"- **{criterion['criterion_name']}**: {criterion['criterion_description']}")

      
        
        return "\n".join(context_parts)
    
    def build_evaluation_results(self, entry_scores, criteria_data):
        """Build evaluation results summary"""
        results_parts = []
        
        for _, row in entry_scores.iterrows():
            criterion_id = row['criteria']
            score = row['score']
            explanation = row['explanation']
            feedback = row['feedback'] if 'feedback' in row and pd.notna(row['feedback']) else "No specific feedback provided"
            url = row['url'] if 'url' in row and pd.notna(row['url']) else "No URL provided"
            
            criterion_name = criteria_data[criterion_id]['criterion_name'] if criterion_id in criteria_data else criterion_id
            
            status = "✓ PASS" if score == 1 else "✗ FAIL"
            
            results_parts.append(f"""
**{criterion_name}** ({status} - {score}/1)
- Repository URL: {url}
- Explanation: {explanation}
- Feedback: {feedback}
""")
        
        return "\n".join(results_parts)
    
    def generate_prompt(self, mode, external_id, criteria_context, evaluation_results):
        """Generate appropriate prompt based on mode"""
        if mode == "repo":
            return self.create_repo_feedback_prompt(external_id, criteria_context, evaluation_results)
        elif mode == "publication":
            print("Generating publication feedsssssssssssssssssssback prompt")
            return self.create_publication_feedback_prompt(external_id, criteria_context, evaluation_results)
        else:
            raise ValueError(f"Unknown mode: {mode}")