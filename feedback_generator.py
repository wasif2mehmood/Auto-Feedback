import json
from datetime import datetime
from pathlib import Path

from config_loader import ConfigLoader
from prompts_generaor import PromptGenerator
from bot import LLMClient
from processor import DataProcessor

class FeedbackGenerator:
    """Main class for generating feedback on repositories or publications"""
    
    def __init__(self, config_path="config.json"):
        self.config_loader = ConfigLoader(config_path)
        self.criteria_data = self.config_loader.load_criteria()
        self.scores_df = self.config_loader.load_scores()
        
        self.prompt_generator = PromptGenerator(self.criteria_data)
        self.llm_client = LLMClient()
        self.data_processor = DataProcessor(self.scores_df, self.criteria_data)
    
    def process_entry(self, external_id):
        """Process a single entry and return feedback"""
        # Get entry scores
        entry_scores = self.data_processor.get_entry_scores(
            external_id, 
            self.config_loader.get_criteria_filter()
        )
        
        if entry_scores.empty:
            return {"error": f"No scores found for {external_id}"}
        
        # Build contexts
        criteria_context = self.prompt_generator.build_criteria_context(entry_scores)
        evaluation_results = self.prompt_generator.build_evaluation_results(entry_scores, self.criteria_data)
        
        # Generate prompt
        prompt = self.prompt_generator.generate_prompt(
            self.config_loader.get_mode(),
            external_id,
            criteria_context,
            evaluation_results
        )
        
        # Get LLM feedback
        feedback = self.llm_client.get_feedback(prompt)
        
        # Calculate summary
        score_summary = self.data_processor.calculate_score_summary(entry_scores)
        repo_url = self.data_processor.get_repository_url(entry_scores)
        
        result = {
            "external_id": external_id,
            "repository_url": repo_url,
            "mode": self.config_loader.get_mode(),
            "timestamp": datetime.now().isoformat(),
            "score_summary": score_summary,
            "feedback": feedback,
            "criteria_evaluated": len(entry_scores)
        }
        
        return result
    
    def get_target_external_ids(self):
        """Get external IDs to process based on config"""
        return self.data_processor.get_target_external_ids(
            self.config_loader.get_target_publications()
        )
    
    def get_all_external_ids(self):
        """Get all unique external IDs from the scores"""
        return self.data_processor.get_all_external_ids()
    
    def save_results(self, results):
        """Save results to output path"""
        output_path = self.config_loader.get_output_path()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return output_path