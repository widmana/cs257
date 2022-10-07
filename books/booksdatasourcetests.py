'''
   booksdatasourcetest.py
   Jeff Ondich, 23 September 2022
   Alex Widman and Serafin Patino
'''

from booksdatasource import Author, Book, BooksDataSource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = BooksDataSource('books1.csv')

    def tearDown(self):
        pass

    #Testing authors function
    def test_unique_author(self):
        '''tests to see if searching by last name returns one author'''
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))

    def test_authors_equalLast(self):
        '''Searching by first and last name returns one author despite same last names'''
        tiny_data_source = BooksDataSource('tinybooks.csv')
        authors = (tiny_data_source.authors('John Green'))
        index = 1
        print("this is the length:", len(authors))
        for i in authors:
            print(index, i.given_name)
            index+=1
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Green', 'John'))

    def test_authors_equalFirst(self):
        '''Searching by first and last name returns one author despite same first names'''
        tiny_data_source = BooksDataSource('tinybooks.csv')
        authors = tiny_data_source.authors('Herman Melville')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Melville', 'Herman'))

    def test_authors_tieBreak(self):
        '''breaks ties using the given name'''
        tiny_data_source = BooksDataSource('tinybooks.csv')
        authors = tiny_data_source.authors('Green')
        self.assertTrue(len(authors) == 2)
        self.assertTrue(authors[0] == Author('Green', 'Herman'))
        self.assertTrue(authors[1] == Author('Green', 'John'))

    def test_authors_multipleBooks(self):
        '''prints all books of a given author'''
        tiny_data_source = BooksDataSource('tinybooks.csv')
        authors = tiny_data_source.authors('John Green')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Green', 'John'))
        self.assertTrue('The Fault in Our Stars' in authors[0].books)
        self.assertTrue('Looking for Alaska' in authors[0].books)
    
    def test_all_authors(self):
        '''If search_text is None, returns all of the author objects (alphabetically by last name)'''
        tiny_data_source = BooksDataSource('tinybooks.csv')
        authors = tiny_data_source.authors()
        self.assertTrue(len(authors) == 5)
        self.assertTrue(authors[0] == Author('Austen', 'Jane'))
        self.assertTrue(authors[1] == Author('Gaiman', 'Neil'))
        self.assertTrue(authors[2] == Author('Green', 'Herman'))
        self.assertTrue(authors[3] == Author('Green', 'John'))
        self.assertTrue(authors[4] == Author('Melville ', 'Herman'))

    def test_incomplete_author(self):
        '''If search_text is an incomplete word and has an uppercase letter, returns all of the possible author objects (alphabetically)'''
        tiny_data_source = BooksDataSource('tinybooks.csv')
        authors = tiny_data_source.authors('aN')
        self.assertTrue(len(authors) == 4)
        self.assertTrue(authors[0] == Author('Austen', 'Jane'))
        self.assertTrue(authors[1] == Author('Gaiman', 'Neil'))
        self.assertTrue(authors[2] == Author('Green', 'Herman'))
        self.assertTrue(authors[3] == Author('Melville ', 'Herman'))

    #Testing books function
    def test_unique_book(self):
        '''unique book title returns correct author and publication_year'''
        books = self.data_source.books('A Wild Sheep Chase')
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0].authors[0] == Author('Murakami', 'Haruki'))
        self.assertTrue(books[0].publication_year == '1982')

    def test_multiple_authors(self):
        '''unique book title w/multiple authors returns multiple authors (alphabetically)'''
        books = self.data_source.books('Good Omens')
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0].authors[0] == Author('Gaiman', 'Neil'))
        self.assertTrue(books[0].authors[1] == Author('Pratchett', 'Terry'))

    def test_unique_book_commas(self):
        '''unique book title with commas returns correct author and publication_year'''
        books = self.data_source.books('Right Ho, Jeeves')
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0].authors[0] == Author('Grenville Wodehouse', 'Pelham'))
        self.assertTrue(books[0].publication_year == '1934')

    def test_books_by_title(self):
        '''multiple books sorted by title'''
        books = self.data_source.books('se')
        self.assertTrue(len(books) == 4)
        self.assertTrue(books[0].title == 'A Wild Sheep Chase')
        self.assertTrue(books[1].title == 'Boys and Sex')
        self.assertTrue(books[2].title == 'Girls and Sex')
        self.assertTrue(books[3].title == 'Sense and Sensibility')

    def test_books_by_year(self):
        '''multiple books sorted by year'''
        books = self.data_source.books('se', 'year')
        self.assertTrue(len(books) == 4)
        self.assertTrue(books[0].publication_year == '2020')
        self.assertTrue(books[1].publication_year == '2016')
        self.assertTrue(books[2].publication_year == '1982')
        self.assertTrue(books[3].publication_year == '1813')

    def test_books_by_year_tieBreak(self):
        '''multiple books sorted by year, tiebreak with title'''
        duplicates_data_source = BooksDataSource('duplicatebooks.csv')
        books = duplicates_data_source.books('dog', 'year')
        self.assertTrue(len(books) == 4)
        self.assertTrue(books[0].publication_year == '1934')
        self.assertTrue(books[1].publication_year == '1994')
        self.assertTrue(books[2].publication_year == '2011')
        self.assertTrue(books[2].title == 'Looking for Dogs')
        self.assertTrue(books[3].publication_year == '2011')
        self.assertTrue(books[3].title == 'The Fault in Our Dogs')

    def test_all_books(self):
        '''If search_text is None, returns all of the book objects (alphabetically by title)'''
        books = self.data_source_tiny.books()
        self.assertTrue(len(books) == 6)
        self.assertTrue(books[0].title == 'Emma')
        self.assertTrue(books[1].title == 'Looking for Alaska')
        self.assertTrue(books[2].title == 'Moby Dick')
        self.assertTrue(books[3].title == 'Neverwhere')
        self.assertTrue(books[4].title == 'Omoo')
        self.assertTrue(books[5].title == 'The Fault in Our Stars')
 
    #Testing books_between_years function
    def test_books_between_years(self):
        '''checks if inclusivity works when both years are the same'''
        books = self.data_source.books_between_years('1987', '1987')
        self.assertTrue(len(books)==1)
        self.assertTrue(books[0].title == 'Beloved')

    def test_books_between_years_works(self):
        '''Checks if BBY actually works given two different years'''
        books = self.data_source.books_between_years('2016','2018')
        self.assertTrue(len(books)== 2)
        self.assertTrue(books[0].title == 'Girls and Sex' and books[1].title == 'There, There')

    def test_books_between_years_tie_breaker(self):
        '''Checks if BBY's tie breaker f(x) works'''
        books = self.data_source.books_between_years('1994', '1994')
        self.assertTrue(len(books)== 2)
        self.assertTrue(books[0].title == 'Mirror Dance' and books[1].title == 'Schoolgirls')

    def test_books_between_years_empty_search(self):
        '''Checks if BBY's empty search returns all the books'''
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books_between_years()
        self.assertTrue(len(books) == 6)
        self.assertTrue(books[0].title == 'Emma')
        self.assertTrue(books[1].title == 'Looking for Alaska')
        self.assertTrue(books[2].title == 'Moby Dick')
        self.assertTrue(books[3].title == 'Neverwhere')
        self.assertTrue(books[4].title == 'Omoo')
        self.assertTrue(books[5].title == 'The Fault in Our Stars')

    def test_books_between_years_end_year_none(self):
        '''Checks if BBY's end year is empty, s.t. books on or after start year are included'''
        books = self.data_source.books_between_years('2018', 'None')
        self.assertTrue(len(books)== 3)
        self.assertTrue(books[0].title == 'There, There' and books[1].title == 'Fine, Thanks' and
        books[2].title == 'Boys and Sex')
    
    def test_books_between_years_start_year_none(self):
        '''Checks if BBY's start year is empty, s.t. books on or before end year are included'''
        books = self.data_source.books_between_years('None' ,'1815')
        for book in books:
            authors_list = [a.given_name + " " + a.surname for a in book.authors]
            print(book.title + ", " + book.publication_year + ", " + " and ".join(authors_list))
        self.assertTrue(len(books)== 3)
        self.assertTrue(books[0].title == 'Pride and Prejudice' and books[1].title == 'Sense and Sensibility' and books[2].title == 'Emma')

    def test_books_between_years_dont_exist(self):
        '''checks if when user puts in years that arent in BBY's database, that it returns an empty list'''
        books = self.data_source.books_between_years('5' ,'7')
        self.assertTrue(len(books)== 0)
        # return empty list, throw exception error (crashes program), prompt user to re enter
        
    def test_books_between_years_wrong_order(self):
        '''Checks if when user types two years in the wrong order, that BBY throws an error'''
        books = self.data_source.books_between_years('2002' ,'1995')
        self.assertTrue(len(books)== 0)


if __name__ == '__main__':
    unittest.main()

