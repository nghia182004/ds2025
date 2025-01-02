from collections import defaultdict
import glob
import os

def mapper(line):
    """
    Map phase: emit (path_length, path) pairs
    Input: single line containing a file path
    Output: tuple of (length, path) if it's a valid path
    """
    path = line.strip()
    
    if path.startswith('/') or (len(path) > 2 and path[1:3] == ':/'):
        path_length = len(path)
        return [(path_length, path)]
    return []

def reducer(mapped_values):
    """
    Reduce phase: find the longest path(s)
    Input: list of (length, path) pairs
    Output: dictionary with max_length and corresponding paths
    """
    if not mapped_values:
        return {"max_length": 0, "paths": []}

    paths_by_length = defaultdict(list)
    for length, path in mapped_values:
        paths_by_length[length].append(path)
    
    max_length = max(paths_by_length.keys())
    return {
        "max_length": max_length,
        "paths": paths_by_length[max_length]
    }

def find_longest_paths(input_dir):
    """
    Main function to process multiple files and find longest paths
    Input: directory containing path files from different laptops
    """
    all_mapped_values = []
    
    
    path_files = glob.glob(os.path.join(input_dir, "*.txt"))
    
    
    for file_path in path_files:
        laptop_name = os.path.basename(file_path).replace('.txt', '')
        print(f"\nProcessing paths from laptop: {laptop_name}")
        
        with open(file_path, 'r') as file:
            for line in file:
                mapped = mapper(line)
                all_mapped_values.extend(mapped)
    
   
    result = reducer(all_mapped_values)
    
   
    print(f"\nMaximum path length: {result['max_length']}")
    print("\nLongest paths found:")
    for path in result['paths']:
        print(path)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python longestpath.py <input_directory>")
        sys.exit(1)
    
    find_longest_paths(sys.argv[1])