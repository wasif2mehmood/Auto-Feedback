from feedback_generator import FeedbackGenerator

def process_single_entry(external_id, config_path="config.json"):
    """Process a single entry and return feedback"""
    generator = FeedbackGenerator(config_path)
    
    # Check if this external_id should be processed
    target_ids = generator.get_target_external_ids()
    if external_id not in target_ids:
        print(f"Warning: {external_id} not in target list {target_ids}")
    
    result = generator.process_entry(external_id)
    
    # Save result
    generator.save_results([result])
    
    return result

def process_all_target_entries(config_path="config.json"):
    """Process all target entries specified in config"""
    generator = FeedbackGenerator(config_path)
    target_ids = generator.get_target_external_ids()
    
    results = []
    for external_id in target_ids:
        result = generator.process_entry(external_id)
        results.append(result)
    
    # Save all results
    generator.save_results(results)
    
    return results

def interactive_feedback(config_path="config.json"):
    """Interactive feedback generation"""
    generator = FeedbackGenerator(config_path)
    target_ids = generator.get_target_external_ids()
    all_ids = generator.get_all_external_ids()
    
    print(f"Target entries (from config): {target_ids}")
    print(f"All available entries: {all_ids}")
    
    results = []
    while True:
        external_id = input("\nEnter external_id (or 'quit' to exit): ").strip()
        
        if external_id.lower() == 'quit':
            break
            
        if external_id in all_ids:
            if external_id not in target_ids:
                print(f"Warning: {external_id} not in target list")
            
            result = generator.process_entry(external_id)
            results.append(result)
            
            print("\n" + "="*50)
            print("FEEDBACK:")
            print("="*50)
            print(result["feedback"])
        else:
            print(f"Entry '{external_id}' not found. Available: {all_ids}")
    
    # Save results if any were generated
    if results:
        generator.save_results(results)
        
    return results