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
    filename = 'books1.csv'
    allbooks = BooksDataSource(filename)

    command = sys.argv[1]
    if command == 'booksearch':     
        if len(sys.argv) == 3 and sys.argv[2] == '--h':
            print('')
            print("booksearch  <string>")
            print("     Prints a list of books whose titles contain string (case-insensitive). ")
            print("[--h] [--help]")
            print("     Prints the synopsis and a list of the options for the booksearch function.")
            print("[ --t | --y] [ --title | --year]") 
            print("     Indicates whether this list is sorted by title in alphabetical order (default) or by publication year from most recent to least recent.")
            print('')
            exit()
        elif len(sys.argv) == 4 and sys.argv[2] == '--t':
            user_input = sys.argv[3]
            booksearch_books = (allbooks.books(user_input))
        elif len(sys.argv) == 3:
            user_input = sys.argv[2]
            booksearch_books = (allbooks.books(user_input))
        elif len(sys.argv) == 4 and sys.argv[2] == '--y':
            user_input = sys.argv[3]  
            booksearch_books = (allbooks.books(user_input, 'year'))
        else:
            print("Your command was not valid, try again! :(")
        for book in booksearch_books:
            authors = [a.given_name + " " + a.surname for a in book.authors]
            print(book.title + ", " + book.publication_year + ", " + " and ".join(authors))
    
    elif  command == 'authorsearch': 
        if len(sys.argv) == 3 and sys.argv[2] == '--h':
            print('')
            print("authorsearch <string>")
            print("     Prints a list of authors whose names contain S (case-insensitive) and a list")
            print("     of their published books in no particular order. Authors will be printed in alphabetical")
            print("     order by surname with ties being broken by given name.")
            print("[--h] [--help]")
            print("     Prints the synopsis and a list of the options for the authorsearch function.")
            print('')
            exit()
        elif len(sys.argv) == 3:
            user_input = sys.argv[2]
            authorsearch_authors = (allbooks.authors(user_input))
        else:
            print("Your command was in valid, please try again :,(")
            exit()
        for author in authorsearch_authors:
            if author.death_year != None:
                print(author.given_name, author.surname, "(" + author.birth_year + "-" + author.death_year + ")" + ": " + ", ".join(author.books))
            else:
                print(author.given_name, author.surname, "(" + author.birth_year + "-): " + ", ".join(author.books))
    
    elif command == 'yearsearch':        
        if len(sys.argv) == 3 and sys.argv[2] == '--h':
            print('')
            print("yearsearch <beginning_year> <ending_year>")
            print('     Prints a list of books published between the beginning year and ending year ')
            print('     inclusive) of an inputed range. Books are printed in order of publication ')
            print('     year from most recent to least recent. If the user wishes to not include a beginning')
            print('     and/or ending year, then the user must input "None" in the place of a year. ')
            print('[--h] [--help]')
            print('     Prints the synopsis and a list of the options for the yearsearch function.')
            print('')
        elif len (sys.argv) == 4:
            start_year = sys.argv[2]
            end_year = sys.argv[3] 
            failure = 0  
            if start_year != 'None':
                try:
                    value = int(start_year)
                    failure = 1
                    pass
                except ValueError:
                    print("You did not enter two valid years")
                    exit()

            if end_year != 'None':
                try:
                    value = int(end_year)
                    failure = 1
                    pass
                except ValueError:
                    print("You did not enter two valid years")
                    exit()
            if failure == 1:
                yearsearch_books = allbooks.books_between_years(start_year, end_year)
                for book in yearsearch_books:
                    authors = [a.given_name + " " + a.surname for a in book.authors]
                    print(book.title + ", " + book.publication_year + ", " + " and ".join(authors))
        else:
            print('Your command was invalid, please try again :(')
       

if __name__ == "__main__":
    main()