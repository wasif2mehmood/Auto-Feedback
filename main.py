from feedback_generator import FeedbackGenerator
from utils import process_single_entry, process_all_target_entries, interactive_feedback

def main():
    """Process all target entries"""
    generator = FeedbackGenerator()
    target_ids = generator.get_target_external_ids()
    middle_ids = target_ids[30:35]
    if target_ids:
        results = []
        
        for external_id in middle_ids:
            result = generator.process_entry(external_id)
            results.append(result)
            
            if "error" not in result:
                print(f"\n--- {external_id} ---")
                print(result["feedback"])
        
        generator.save_results(results)
        return results
    else:
        print("No entries found to process")

if __name__ == "__main__":
    main()