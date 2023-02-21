import math
import typing
import random

class ToeplitzMatrix:
    __rows: int
    __columns: int
    __matrix: typing.List[int]
    __iterator_index: int = 0
      
    def fill_with_toeplitz_generator(self, rows: int, columns: int) -> None:
        """Fill matrix use toeplitz
        
        Keyword arguments:
        rows -- ammount of rows
        columns -- ammount of columns
        """
        temp_array: typing.List[int] = [None] * (rows + columns - 1)
        for i in range(len(temp_array)):
            temp_array[i] = random.getrandbits(1)
        self.__rows = rows
        self.__iterator_index = rows - 1
        self.__columns = columns;
        self.__matrix = temp_array
    
    def __iter__(self):
        self.__iterator_index = self.__rows - 1
        return self
       
    def __next__(self):
        if self.__iterator_index < 0:
            raise StopIteration
        else:
            self.__iterator_index -= 1
            return self.__matrix[self.__iterator_index + 1: self.__iterator_index + 1 + self.__columns]
        
    def __getitem__(self, position: typing.Tuple[int]) -> int:
        return self.__matrix[self.__rows - 1 - position[0] + position[1]]
        
    def __len__(self):
        return self.__rows


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


def multiply_matrix(matrix: ToeplitzMatrix, token: str) -> str:
    """Return the string representing multiplication result
        
    Keyword arguments:
    token -- vector-string to multiply
    matrix -- matrix to multiply
    """
    result_token: int = 1
    
    for matrix_row in range(len(matrix)):
        temporary_value : int = 0
        
        for bit_index, string_bit in enumerate(token):
            temporary_value = temporary_value ^ (int(string_bit) & matrix[matrix_row, bit_index])
        
        result_token = (result_token << 1) + temporary_value
        
    return str(bin(result_token)[-len(matrix):])
    

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


def evaluate_compression_length(occurrence: int, tokensAmount: int) -> int:
    probability: float = occurrence/tokensAmount
    Hmin = -math.log(probability, 2)
    return int(n // (8 / Hmin))


TOKEN_LENGTH: int = 8                        #Lenght of bitword
filename: str = 'raw20k.txt'         #Name of file, where stored data to squish
output_file: str = 'Truerandomness.txt'       #Name of file, where would be stored result


#Begin programm
if __name__ == '__main__':
    occurrence : int = 0                    #Maximum of occurrences
    maxToken: str = ''                      #Most found token
    
    input_data_string = open(filename, 'r').read().replace('\n', '')
    maxToken, occurrence = find_max_occurence_token(input_data_string, TOKEN_LENGTH)
    
    n = len(input_data_string)
    m = evaluate_compression_length(occurrence, n//occurrence)
    
    matrix: ToeplitzMatrix = ToeplitzMatrix()
    matrix.fill_with_toeplitz_generator(m, n)
    
    multiplication_result = multiply_matrix(matrix, input_data_string)
    save_string_to_file(multiplication_result, output_file)
