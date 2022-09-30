'''
    books.py
    Jeff Ondich, 29 September 2022

    Alex Widman
    Serafin Patino
    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2022.
'''
import csv
import sys
from booksdatasource import BooksDataSource


def main():
    # with open('books1.csv', 'r') as csv_file:
    #     csv_reader = csv.reader(csv_file)
    filename = 'books1.csv'
    allbooks = BooksDataSource(filename)

    command = sys.argv[1]
    # all the indexes were off by 1 since he first sysargv idx was the file name
    # added __repr__ into booksearch and author search, it returns the string form of an object
    if command == 'booksearch':     #books(self, search_text=None, sort_by='title'):
        if len(sys.argv) == 3 and sys.argv[2] == '--h':
            print("booksearch  <string>  Prints a list of books whose titles contain string (case-insensitive). ")
            print("[--h] [--help] Prints the synopsis and a list of the options for the booksearch function.")
            print("[ --t | --y] [ --title | --year] Indicates whether this list is sorted by title in alphabetical order (default)")
            print("or by publication year from most rrrecent to least recent.")
        elif len(sys.argv) == 4 and sys.argv[2] == '--t':
            string = sys.argv[3]
            list = (allbooks.books(string))
        elif len(sys.argv) == 3:
            string = sys.argv[2]
            list = (allbooks.books(string))
        elif len(sys.argv) == 4 and sys.argv[2] == '--y':
            string = sys.argv[3]  
            list = (allbooks.books(string, 'year'))
        else:
            print("Your command was not valid, try again! :(")
        for i in list:
            print(i.title, i.publication_year, end = "")
            for j in i.authors:
                print(",", j)
    
    elif  command == 'authorsearch':            #def authors(self, search_text=None):
        if len(sys.argv) == 4 and sys.argv[2] == '-h':
            print("Prints a list of authors whose names contain S (case-insensitive) and a list")
            print("of their published books in no particular order. Authors will be printed in alphabetical")
            print("order by surname with ties being broken by given name.")
            print("[--h] [--help]")
            print("Prints the synopsis and a list of the options for the authorsearch function.")
        elif len(sys.argv) == 3:
            string = sys.argv[2]
            list = (allbooks.authors(string))
        else:
            print("Your command was in valid, please try again :,(")
        for i in list:
            print(i.given_name, i.surname, i.birth_year, "-", i.death_year, end = ":")
            for j in i.books:
                print(j, end = ", ")

    
    elif command == 'yearsearch':               #def books_between_years(self, start_year=None, end_year=None):
        if len(sys.argv) == 3 and sys.argv[2] == '--h':
            print('Prints a list of books published between the beginning year and ending year ')
            print('inclusive) of an inputed range. Books are printed in order of publication ')
            print('year from most recent to least recent.')
            print('[--h] [--help] Prints the synopsis and a list of the options for the yearsearch function.')
        elif len (sys.argv) == 4:
            start_year = sys.argv[2]
            end_year = sys.argv[3] 
            if start_year != 'None':
                try:
                    value = int(start_year)
                except ValueError:
                    print("This is not a valid year")
                    exit()
            if end_year != 'None':
                try:
                    value = int(end_year)
                except ValueError:
                    print("This is not a valid year")
                    exit()
            else:
                list = allbooks.books_between_years(start_year, end_year)
        else:
            print('Your command was invalid, please try again :(')
        for i in list:
            print(i.title, i.publication_year, end = ": ")
            for j in i.authors:
                print(j)

if __name__ == "__main__":
    main()