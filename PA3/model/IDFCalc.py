import sys
import os.path
import marshal
import math

def get_idf(root_dir, idf_filename):
    sortedDirList = sorted(os.listdir(root_dir))
    N = 0
    doc_id = 0
    df = {}
    file_length = 0
    
    for dir_name in sortedDirList:
        print >> sys.stderr, 'processing dir_name: ' + dir_name
        dir_name = os.path.join(root_dir, dir_name)
    
        sortedFileList = sorted(os.listdir(dir_name))
        for f in sortedFileList:
            #count_file()
            N += 1
            file_id = os.path.join(dir_name, f)
            doc_id += 1
            fullpath = os.path.join(dir_name, f)
            file = open(fullpath, 'r')
            file_words = {}
            for line in file.readlines():
                words = line.strip().split()
                file_length += len(words)
                for word in words:
                    file_words[word] = 1
            for w in file_words:
                    df[w] = df.get(w, 0) + 1
            
                    
    idf = {}
    for t in df:
        idf[t] = math.log10(1.0*N/df[t])
    avg_file_length = 1.0*file_length/N
    serialize_data(dict(idf), idf_filename)
    serialize_data(avg_file_length, 'avg_file_length')
    return idf
    
    
def serialize_data(data, fname):
    """
    Writes `data` to a file named `fname`
    """
    with open(fname, 'wb') as f:
        marshal.dump(data, f)
        
        
if __name__=='__main__':
    data_path = 'data'
    idf = get_idf(data_path, 'idf')  
