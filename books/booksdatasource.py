#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2022

    Alex Widman
    Serafin Patino
    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2022.
'''
import csv
from pickle import FALSE, TRUE

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None, books=[]):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year
        self.books = books

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

    def __repr__(self):
        return self.surname +  " " + self.given_name
    
    def __lt__(self, other):
        if self.surname < other.surname:
            return True
        elif self.surname == other.surname and self.given_name < other.given_name:
            return True
        else:
            return False

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __repr__(self):
        return self.title

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

    def __lt__(self, other):
        if self.surname < other.surname:
            return True
        elif self.surname == other.surname and self.given_name < other.given_name:
            return True
        else:
            return False



class BooksDataSource: 
    ''' This __init__ method parses the specified CSV file and creates
        suitable instance variables for the BooksDataSource object containing
        a collection of Author objects and a collection of Book objects.
    '''
    def __init__(self, books_csv_file_name): 
        self.our_books = []
        self.our_authors = [] 

        with open(books_csv_file_name, 'r') as csv_file:

            csv_reader = csv.reader(csv_file)

            for line in csv_reader:
                title = line[0]
                publication_year = line[1]
                rest = line[2]                      #csv reader only seperates the title and publication year, the rest of the line is in 'rest'

                individuals = rest.split(" and ")   #if there are multiple authors
                list_of_authors = []
                for individual in individuals:      #for each author

                    #get names
                    individual_components = individual.split(" ")                    
                    if len(individual_components) == 4:     #if the author has a middle name, include the middle name in surname
                        surname = individual_components[1] + " " + individual_components[2]
                        date_range = individual_components[3]
                    else:
                        surname = individual_components[1]
                        date_range = individual_components[2]
                    given_name = individual_components[0]

                    #get dates               
                    dates = date_range.split("-")
                    birth_year = (dates[0])[1:]
                    if len(dates[1]) == 1:
                        death_year = None
                    else:
                        death_year = (dates[1])[:-1]

                    #instantiate the author with an empty list of book titles
                    list_of_titles = []
                    this_author = Author(surname, given_name, birth_year, death_year, list_of_titles)
        
                    #if the author is already in the our_authors list, add the title to the titles instance list and replace the old author object
                    if this_author in self.our_authors:     
                        found_index = self.our_authors.index(this_author)
                        this_list_of_titles = self.our_authors[found_index].books
                        this_list_of_titles.append(title)
                        new_this_author = Author(surname, given_name, birth_year, death_year, this_list_of_titles)
                        del self.our_authors[found_index]
                        self.our_authors.append(new_this_author)   
                    #otherwise, just append the new author object
                    else:
                        list_of_titles.append(title)                        
                        self.our_authors.append(this_author)       
                    list_of_authors.append(this_author)
                
                #create a new book and add it to the our_books list
                this_book = Book(title, publication_year, list_of_authors)
                self.our_books.append(this_book) 
        pass

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Bront?? comes before Charlotte Bront??).
        '''
        if search_text == None:
            return sorted(self.our_authors)
        else:
            specified_author_list = []
            for author in self.our_authors:
                fullname = (author.given_name + " " + author.surname).upper()
                if search_text.upper() in fullname:
                    specified_author_list.append(author)
                else:
                    pass
            return sorted(specified_author_list)

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        specified_books_list = []
        if search_text == None or search_text == "None":
            specified_books_list = self.our_books
        else:
            for book in self.our_books:
                if search_text.upper() in book.title.upper():
                    specified_books_list.append(book)
            if sort_by == 'year':       
                return sorted(specified_books_list, key = lambda book: (book.publication_year, book.title))
        return sorted(specified_books_list, key = lambda book: (book.title, book.publication_year))

    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        specified_books_list = []
        if start_year == None and end_year == None:
            specified_books_list = self.our_books
        elif start_year == 'None':
             for book in self.our_books:
                if int(book.publication_year) <= int(end_year):
                    specified_books_list.append(book)
                else:
                    pass
        elif end_year == 'None':
                for book in self.our_books:
                    if int(book.publication_year) >= int(start_year):
                        specified_books_list.append(book)
                    else:
                        pass           
        else:
            for book in self.our_books:
                if int(book.publication_year) >= int(start_year) and int(book.publication_year) <= int(end_year):
                    specified_books_list.append(book)
                else:
                    pass
        return sorted(specified_books_list, key = lambda book: (book.publication_year, book.title))

