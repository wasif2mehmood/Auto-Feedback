import pandas as pd

class DataProcessor:
    """Handles data processing and filtering operations"""
    
    def __init__(self, scores_df, criteria_data):
        self.scores_df = scores_df
        self.criteria_data = criteria_data
    
    def get_entry_scores(self, external_id, criteria_filter=None):
        """Get all scores for a specific entry, filtered by criteria"""
        entry_scores = self.scores_df[self.scores_df['publication_external_id'] == external_id]
        
        # Filter by criteria if specified
        if criteria_filter:
            entry_scores = entry_scores[entry_scores['criteria'].isin(criteria_filter)]
        
        return entry_scores
    
    def get_target_external_ids(self, config_publications=None):
        """Get external IDs to process based on config"""
        if config_publications:
            return config_publications
        else:
            return self.scores_df['publication_external_id'].unique().tolist()
    
    def get_all_external_ids(self):
        """Get all unique external IDs from the scores"""
        return self.scores_df['publication_external_id'].unique().tolist()
    
    def calculate_score_summary(self, entry_scores):
        """Calculate score summary for an entry"""
        total_score = entry_scores['score'].sum()
        max_score = len(entry_scores)
        
        return {
            "total_score": int(total_score),
            "max_score": int(max_score),
            "percentage": round((total_score / max_score * 100), 2) if max_score > 0 else 0
        }
    
    def get_repository_url(self, entry_scores):
        """Get repository URL from entry scores"""
        if not entry_scores.empty and 'url' in entry_scores.columns:
            return entry_scores['url'].iloc[0]
        return "No URL available"