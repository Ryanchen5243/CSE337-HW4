#!/usr/bin/env/python3

import db
from objects import Movie

def display_title():
    print("The Movie List program")
    print()    
    display_menu()

def display_menu():
    print("COMMAND MENU")
    print("cat  - View movies by category")
    print("year - View movies by year")
    print("add  - Add a movie")
    print("del  - Delete a movie")
    print("exit - Exit program")
    print("min - Max Running Time")
    print()    

def display_categories():
    print("CATEGORIES")
    categories = db.get_categories()    
    for category in categories:
        print(str(category.id) + ". " + category.name)
    print()

def display_movies(movies, title_term):
    print("MOVIES - " + title_term)
    line_format = "{:3s} {:37s} {:6s} {:5s} {:10s}"
    print(line_format.format("ID", "Name", "Year", "Mins", "Category"))
    print("-" * 64)
    for movie in movies:
        print(line_format.format(str(movie.id), movie.name,
                                 str(movie.year), str(movie.minutes),
                                 movie.category.name))
    print()    

def display_movies_by_category():
    category_id = int(input("Category ID: "))
    category = db.get_category(category_id)
    if category == None:
        print("There is no category with that ID.\n")
    else:
        print()
        movies = db.get_movies_by_category(category_id)
        display_movies(movies, category.name.upper())
    
def display_movies_by_year():
    year = int(input("Year: "))
    print()
    movies = db.get_movies_by_year(year)
    display_movies(movies, str(year))

def add_movie():
    name        = input("Name: ")
    year        = int(input("Year: "))
    minutes     = int(input("Minutes: "))
    category_id = int(input("Category ID: "))
    
    category = db.get_category(category_id)
    if category == None:
        print("There is no category with that ID. Movie NOT added.\n")
    else:        
        movie = Movie(name=name, year=year, minutes=minutes,
                      category=category)
        db.add_movie(movie)    
        print(name + " was added to database.\n")

def delete_movie():
    movie_id = int(input("Movie ID: "))

    # get movie object for specified id
    movie = db.get_movie(movie_id)
    if movie is None:
        print("Couldn't find movie with movie id ",str(movie_id))
        return
    confirm = input("Are you sure you want to delete '{}'? (y/n): ".format(movie.name))
    if confirm.lower() == 'y':
        db.delete_movie(movie_id)
        print("Movie ID " + str(movie_id) + " was deleted from database.\n")
    else:
        print("Delete operation cancelled.")

def display_movies_by_minutes():
    '''
    6. In the ui module, add a display_movies_by_minutes()
    function that calls the
    get_int() function to get the maximum number of minutes from 
    the user and displays
    all selected movies. This should sort the movies by minutes 
    in ascending order.
    ''' 
    max_time = int(input("Maximum number of minutes: "))
    print("MOVIES - LESS THAN {} MINUTES".format(max_time))
    result = db.get_movies_by_minutes(max_time)
    print("{:<4}{:<30}{:<8}{:<8}{:<10}".format("ID","Name","Year","Mins","Category"))
    print("-"*60)
    for movie in result:
        print("{:<4}{:<30}{:<8}{:<8}{:<10}".format(
            str(movie.id),str(movie.name),str(movie.year),str(movie.minutes),str(movie.category.name))
            )

def main():
    db.connect()
    db.initialize_database() # testing
    display_title()
    display_categories()
    while True:        
        command = input("Command: ")
        if command == "cat":
            display_movies_by_category()
        elif command == "year":
            display_movies_by_year()
        elif command == "add":
            add_movie()
        elif command == "del":
            delete_movie()
        elif command == "min":
            display_movies_by_minutes()
        elif command == "exit":
            break
        else:
            print("Not a valid command. Please try again.\n")
            display_menu()
    db.close()
    print("Bye!")

if __name__ == "__main__":
    main()
