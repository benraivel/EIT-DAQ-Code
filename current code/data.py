'''
Data.py
Ben Raivel

Reads CSV files, stores data, access/filter data by variable name
From CS 251 project 1
Spring 2021
'''

import numpy as np
import csv

'''
    To Do:
        - check inputs to init and provide error messages
'''

class Data:
    def __init__(self, filepath=None, headers=None, data=None, header2col=None, head = False):
        self.filepath = filepath
        self.headers = headers
        self.data = data
        self.header2col = header2col

        if filepath is not None:
            self.filepath = filepath
            if head:
                self.read(self.filepath)
            else:
                self.read_no_head(self.filepath)

    def read(self, filepath):
        # open file using file path
        self.csv_file = open(filepath, 'r')

        # get headers from 1st line
        line = self.csv_file.readline()
        temp_headers = line.split(',')
        self.headers = []
        for header in temp_headers:
            self.headers.append(header.strip())

        
        # get numeric data indices from 2nd line
        line = self.csv_file.readline()
        types = line.split(',')
        stripped_types = []
        for type in types:
            stripped_types.append(type.strip())
        self.data_indices = []
        index = 0
        for type in stripped_types:
            if type == 'numeric':
                self.data_indices.append(index)
            index += 1

        numeric_headers = []
        for index in self.data_indices:
            numeric_headers.append(self.headers[index])

        self.headers = numeric_headers

        # add headers to dict
        self.header2col = {}
        index = 0
        for header in self.headers:
            self.header2col[header] = index
            index += 1


        # read in data
        self.data = []
        line = self.csv_file.readline()
        while line != '':
            data = line.split(',')
            temp = []
            for index in self.data_indices:
                temp.append(data[index].strip())
            self.data.append(temp)
            line = self.csv_file.readline()

        # convert to numpy
        self.data = np.array(self.data)

    def read_no_head(self, filepath):
        # open file using file path
        self.csv_file = open(filepath, 'r')
        
        # read in data
        self.data = []
        line = self.csv_file.readline()
        while line != '':
            data = line.split(',')
            temp = []
            for item in data:
                temp.append(item.strip())
            self.data.append(temp)
            line = self.csv_file.readline()

        # convert to numpy
        self.data = np.array(self.data)

    def __str__(self):
        temp = "string summary of Data object \n"
        temp += self.filepath + '\n'

        for heading in self.headers:
            temp += heading + " "
        temp += '\n'

        temp += str(self.get_num_dims()) + ' columns, ' + str(self.get_num_samples()) + ' rows\n'

        for i in range(5):
            try:
                temp += str(self.data[i]) + '\n'
            except:
                return temp
        
        temp += 'etc...'

        return temp

    def get_headers(self):
        return self.headers

    def get_mappings(self):
        return self.header2col

    def get_num_dims(self):
        return len(self.headers)

    def get_num_samples(self):
        return len(self.data)

    def get_sample(self, rowInd):
        return self.data[rowInd]

    def get_header_indices(self, headers):
        temp = []
        for header in headers:
            temp.append(self.header2col.get(header))
        return temp

    def get_all_data(self):

        return np.copy(self.data)

    def head(self):
        # slice first 5 rows and all columns
        return self.data[0:5,]

    def tail(self):
        # slice last 5 rows and all columns
        return self.data[-5:,]

    def limit_samples(self, start_row, end_row):
        
        self.data = self.data[start_row:end_row,]

    def select_data(self, headers, rows=[]):
        
        # create list for column indices
        col_indices =[]

        # if one column is requested
        if type(headers) == str:
            col_indices.append(self.header2col[headers])
         
        # if multiple columns are requested
        else:
            for header in headers:
                col_indices.append(self.header2col[header])

        temp_data = np.empty((self.get_num_samples(), len(col_indices)))
        
        # loop over selected columns add to array
        new_col_index = 0
        for index in col_indices:
            temp_data[:,new_col_index] = self.data[:,index]
            new_col_index += 1

    
        # return all rows
        if rows == []:
            return temp_data
        
        # return specific rows
        else:
            temp_rows = np.empty((len(rows), len(col_indices)))
            rows_index = 0
            for row in rows:
                temp_rows[rows_index] = temp_data[row]
                rows_index += 1
    

            return temp_rows
    
    def select_dimension(self, index):
        temp_data = np.empty((self.get_num_samples(), 1))
        temp_data[:,0] = self.data[:,index]
        return temp_data

