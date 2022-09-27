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

from pyrsistent import s

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

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

class BooksDataSource: 
    ''' The books CSV file format looks like this:

            title,publication_year,author_description

        For example:

            All Clear,2010,Connie Willis (1945-)
            "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

        This __init__ method parses the specified CSV file and creates
        suitable instance variables for the BooksDataSource object containing
        a collection of Author objects and a collection of Book objects.
    '''
    our_books = []
    our_authors = []    #we can do this right

    def __init__(self, books_csv_file_name): 
        with open(books_csv_file_name, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for line in csv_reader:
                    title = line[0]
                    publication_year = line[1]
                    rest = line[2]
                    individuals = rest.split(" and ")
                    list_of_authors = []
                    for i in individuals:
                        components = i.split(" ")
                        firstname = components[0]
                        if len(components) == 4:
                            lastname = components[1] + i[2]
                            date_range = components[3]
                        else:
                            lastname = components[1]
                            date_range = components[2]
                        dates = date_range.split("-")
                        birth_year = (dates[0])[1:]
                        death_year = (dates[1])[:-1]  #may have to change this, right now death_year when still alive is ""
                        list_of_titles = []
                        this_author = Author(lastname, firstname, birth_year, death_year, list_of_titles)
                        if this_author in BooksDataSource.our_authors:
                            found_index = BooksDataSource.our_authors.index(this_author)
                            this_list_of_titles = BooksDataSource.our_authors[found_index].books
                            this_list_of_titles.append(title)
                            new_this_author = Author(lastname, firstname, birth_year, death_year, this_list_of_titles)
                            BooksDataSource.our_authors.append(new_this_author)    #updates values with a new appended list of titles
                        else:
                            list_of_titles.append(title)
                            BooksDataSource.our_authors.append(this_author)         #appends the authors list with a new author
                        list_of_authors.append(this_author)
                    this_book = Book(title, publication_year, list_of_authors)
                    BooksDataSource.our_books.append(this_book)

                    for this_book in BooksDataSource.our_books:
                        print(this_book.title, this_book.publication_year)

                    for this_author in BooksDataSource.our_authors:
                        print(this_author.surname, this_author.books)
        pass

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        if search_text == None:
            return BooksDataSource.our_authors
        else:
            specified_author_list = []
            for i in BooksDataSource.our_authors:
                if search_text in i.surname or i.firstname:
                    specified_author_list.append(i)
            for j in specified_author_list:
                pass
            return []
    
    def alphabetsort (self, word1, word2):
        if word1 > word2:
            return 1
        elif word2 > word1:
            return 2
        else:
            return 0

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
        return []

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
        return []

def main():
    testing = BooksDataSource("books1.csv")
    testing2 = testing.authors("Orenstein")

if __name__ == "__main__":
    main()