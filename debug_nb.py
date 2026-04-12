import nbformat
import os

def debug_notebook_loading(nb_path):
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found")
        return
        
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    code_to_exec = ""
    for cell in nb.cells:
        if cell.cell_type == 'code':
            source = cell.source
            # Check for potential issues in skipping logic
            if 'plt.show()' in source or 'get_recommendations(' in source and 'def ' not in source:
                continue
            code_to_exec += source + "\n"
            
    print("--- Code to be executed ---")
    print(code_to_exec)
    print("--------------------------")
    
    namespace = {}
    try:
        exec(code_to_exec, namespace)
        print("Execution successful!")
        if 'get_recommendations' in namespace:
            print("Found 'get_recommendations' function.")
        else:
            print("Error: 'get_recommendations' function NOT found in namespace.")
    except Exception as e:
        print(f"Execution failed: {e}")

if __name__ == "__main__":
    debug_notebook_loading('recommender.ipynb')
