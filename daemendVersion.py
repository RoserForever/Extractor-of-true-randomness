import math
import typing
from re import sub

class RandomReader:
    def __init__(self, file_name: str):
        self.__file = open(file_name, 'r')
    
    def get_next_bit(self) -> str:
        """Return string token representing random bit"""
        result_value: str = self.__file.read(1)
        
        while result_value != '0' and result_value != '1':
            result_value = self.__file.read(1)
            if len(result_value) == 0: raise EOFError("Can't read random value")
            
        return RandomReader.get_token_of_length(self, 1)
        
    
    def get_token_of_length(self, token_length: int ) -> str:
        """Return string token of random bits"""
        result_value: str = RandomReader.__filter_bits(self.__file.read(token_length))
        
        while len(result_value) < token_length:
            result_value += __filter_bits(self.__file.read(token_length - result_value))
        
        return result_value
    
    def __filter_bits(token: str) -> str:
        return sub("[^0-1]", "", token)


class BitMatrix:
    rows: int
    columns: int
    matrix: typing.List[str]
    
    def fill_with_size_and_string_random_source(self, rows: int, columns: int, random_source: RandomReader) -> None:
        """Fill matrix with random values read from RandomReader
        
        Keyword arguments:
        rows -- ammount of rows
        columns -- ammount of columns
        random_source -- instance of RandomReader class, able to provide <rows + columns - 1> random values
        """
        self.rows = rows
        self.columns = columns
        matrix = [None] * rows
        matrix[0] = random_source.get_token_of_length(columns)
        
        for row_number in range(1, rows):
            matrix[row_number] = random_source.get_next_bit()
            matrix[row_number] += matrix[row_number-1][:-1]
            
        self.matrix = matrix
        return None
        
    #TODO: NotImplemented 
    def fill_with_size_and_byte_random_source(self, rows: int, columns: int, random_source) -> None:
        self.rows = rows
        self.columns = columns
        raise NotImplementedError("fill_with_size_and_byte_random_source is not implemented")
        
    def __iter__(self):
        return self.matrix.__iter__()
    
    def __getitem__ (self, key) -> Iterator[str]:
        return self.matrix[key]


def find_max_occurence_token(input_data_string: str, token_length: int) -> typing.Tuple[str, int]:
    """Return the token with the most occurrences and the number of occurrences
        
    Keyword arguments:
    input_data_string -- string to be parsed
    token_length -- length of word
    """
    tokens_dict : Dict[str, int] = dict()
    
    for token_begin_index in range(0, len(input_data_string), token_length):
        buffered_value: str = input_data_string[token_begin_index:token_begin_index + token_length]
        tokens_dict[buffered_value] = tokens_dict.get(buffered_value, 0) + 1
        
    maximum_occurrence: int = 0
    maximum_occurrences_token: str
    
    for token, occurrence in tokens_dict.items():
        if occurrence > maximum_occurrence:
            maximum_occurrences_token = token
            maximum_occurrence = occurrence
            
    return maximum_occurrences_token, maximum_occurrence   


def multiply_matrix(token: str, matrix: BitMatrix) -> str:
    """Return the string representing multiplication result
        
    Keyword arguments:
    token -- vector-string to multiply
    matrix -- matrix to multiply
    """
    result_token: str = ''
    
    for matrix_row in matrix:
        temporary_value : int = 0
        
        for bit_index, string_bit in enumerate(token):
            temporary_value = temporary_value ^ (int(string_bit) & int(matrix_row[bit_index]))
        
        result_token += str(temporary_value)
        
    return result_token


def save_string_to_file(token: str, file_name: str = 'output.txt')  -> None:   #Save string to file;
    """Saves string to a file
    
    Keyword arguments:
    token -- string to save in file
    file_name -- full file name, where string would be stored
    """
    file = open(file_name, 'w')
    file.write(token)
    file.close()
  
    
def save_bits_to_file(token: str, file_name: str = 'output.dat') -> None:
    """Saves string to a binary file
    
    Keyword arguments:
    token -- string to save in file
    file_name -- full file name, where string would be stored
    """
    file = open(file_name, 'wb')
    file.write(int(token[::-1], 2).to_bytes(len(token)//8, 'little'))
    file.close()


TOKEN_LENGTH: int = 8                        #Lenght of bitword
filename: str = 'data1000.1.txt'             #Name of file, where stored data to squish
randombits_file_name: str = ''
output_file: str = 'Truerandomness.txt'       #Name of file, where would be stored result


#Begin programm
if __name__ == '__main__':
    occurrence : int = 0                    #Maximum of occurrences
    maxToken: str = ''                      #Most found token
    
    input_data_string = open(filename, 'r').read().replace('\n', '')
    maxToken, occurrence = find_max_occurence_token(inputDataString, TOKEN_LENGTH)
    
    n = len(input_data_string)
    Pmax = occurrence/(n/TOKEN_LENGTH)
    Hmin = -math.log(Pmax,2)
    e = 10**(-30)
    m = int(Hmin + 2*math.log((1/e),2))
    Rand_Length = n+m-1
    
    random_source = RandomReader(randombits_file_name)
    matrix: BitMatrix = BitMatrix()
    
    matrix.fill_with_size_and_string_random_source(m, n, random_source)
    
    multiplication_result = multiply_matrix(input_data_string, matrix)
    save_string_to_file(multiplication_result, output_file)
    print(multiplication_result)
