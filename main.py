from feedback_generator import FeedbackGenerator
from utils import process_single_entry, process_all_target_entries, interactive_feedback

def main():
    """Process first target entry"""
    generator = FeedbackGenerator()
    
    # Get target entries based on config
    target_ids = generator.get_target_external_ids()
    
    # Process single entry
    if target_ids:
        external_id = target_ids[0]  # Process first target entry
        result = generator.process_entry(external_id)
        
        # Save result
        output_path = generator.save_results([result])
        
        print("\n" + "="*50)
        print("FEEDBACK:")
        print("="*50)
        print(result["feedback"])
        print(f"\nResults saved to: {output_path}")
        
        return result
    else:
        print("No entries found to process")

if __name__ == "__main__":
    main()