import pandas as pd
class PromptGenerator:
    """Handles generation of prompts for different modes"""
    
    def __init__(self, criteria_data):
        self.criteria_data = criteria_data
    
    def create_repo_feedback_prompt(self, external_id, criteria_context, evaluation_results):
        """Create feedback prompt for repository assessment"""
     
        return f"""You are an expert code reviewer providing constructive feedback on a GitHub repository's RAG implementation.

**Repository ID:** {external_id}

**Evaluation Criteria:**
{criteria_context}

**Evaluation Results:**
{evaluation_results}

**Instructions:**
- Give the most critical improvements needed (1-2 sentences max)
- Mention ONLY the strongest aspect that works well (1 sentence max)
- Be specific and actionable, no generic advice
- Focus on what will have the biggest impact

Please provide concise feedback covering what works well and what needs improvement.
Dont give strcutured output, write like a human in giving feedback in a summarized way single paragraph
"""
    
    def create_publication_feedback_prompt(self, external_id, criteria_context, evaluation_results):
        """Create feedback prompt for publication assessment"""

        
        print("Creating publication feedback prompt")
        print(f"External ID: {external_id}")
        print(f"Criteria Context: {criteria_context}")
      
        return f"""You are an expert academic reviewer providing constructive feedback on a technical publication content.

**Publication ID:** {external_id}

**Evaluation Criteria:**
{criteria_context}

**Evaluation Results:**
{evaluation_results}

**Instructions:**
- Give the most critical improvements needed (1-2 sentences max)
- Mention ONLY the strongest aspect that works well (1 sentence max)
- Be specific and actionable, no generic advice
- Focus on what will have the biggest impact

Please provide concise feedback covering what works well and what needs improvement.
Dont give strcutured output, write like a human in giving feedback in a summarized way single paragraph"""
    
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