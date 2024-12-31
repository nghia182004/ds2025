from collections import defaultdict

def mapper(line):
    
    word_counts = []
    for word in line.lower().split():
        word_counts.append((word, 1))
    return word_counts

def reducer(mapped_values):
    
    counts = defaultdict(int)
    for word, count in mapped_values:
        counts[word] += count
    return counts

def word_count(filename):
    
    all_mapped_values = []
    
    
    with open(filename, 'r') as file:
        for line in file:
            mapped = mapper(line)
            all_mapped_values.extend(mapped)
    
   
    result = reducer(all_mapped_values)
    
    
    for word, count in result.items():
        print(f"{word}: {count}")

if __name__ == '__main__':
    word_count('input.txt')