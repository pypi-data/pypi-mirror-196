from collections import namedtuple
from critparse import CriterionMovieParse


def movie_info_to_text(criterion_parser):
    if criterion_parser.url_type == 'movie':
        print('Examined ' + criterion_parser.url)
        __movies_to_text(criterion_parser)  # [['', criterion_parser.url]]
    elif criterion_parser.url_type == 'collection':
        print('Examined ' + criterion_parser.url)
        __movies_to_text(criterion_parser)  # criterion_parser.extracted_episode_info
    elif criterion_parser.url_type == 'edition':
        print('Examined ' + criterion_parser.url)
        __movies_to_text(criterion_parser)  # criterion_parser.extracted_episode_info
    else:
        print('Examined ' + criterion_parser.url)
        print('+' * 54)
        print(criterion_parser.series_name)
        print(criterion_parser.description)
        print('+' * 54)
        print()
        print()
        __movies_to_text(criterion_parser)

        print()
        print()
        __egrep_section_to_text(criterion_parser.extracted_episode_info)

        if not criterion_parser.url_type == 'movie':
            print()
            print()
            __collection_update_info_to_text(criterion_parser.all_movie_parsed_data, criterion_parser.series_name)


def __movies_to_text(criterion_parser):
    MovieInfo = namedtuple("MovieInfo", "just_title year title director country stars descr length url")
    # if there is only one movie in a collection (a collection of one)
    # then this is merely an envelope and should not create a collection
    series_name = criterion_parser.series_name
    if len(criterion_parser.all_movie_parsed_data) == 1 and criterion_parser.url_type == "collection":
        series_name = ""
    episode = 0
    for movie in criterion_parser.all_movie_parsed_data:
        episode += 1
        print('=' * 54)
        movie_info = MovieInfo(*movie)
        __movie_details_to_text(movie_info, episode, series_name)
        print('=' * 54)
        print()
        print()


def __movie_details_to_text(movie_info, episode_number, series_name):
    print(episode_number)
    print(movie_info.length)
    print(CriterionMovieParse.valueIfDefinedOrNONE(series_name))
    print(movie_info.url)
    print(movie_info.title)
    print('##' + movie_info.title + ' Watched')
    print(CriterionMovieParse.valueIfDefinedOrNONE(movie_info.director))
    print(CriterionMovieParse.valueIfDefinedOrNONE(movie_info.country))
    print(CriterionMovieParse.valueIfDefinedOrNONE(movie_info.stars))
    print()
    print(CriterionMovieParse.valueIfDefinedOrNONE(movie_info.descr))


def __egrep_section_to_text(extracted_episode_info):
    for movie in extracted_episode_info:
        title = movie[2]
        str_end = ' \\([1,2,N]" *\n'
        if title[:2] == "A ":
            title = title[2:]
            str_end = ', A \\([1,2,N]" *\n'
        if title[:4] == "The ":
            title = title[4:]
            str_end = ', The \\([1,2,N]" *\n'
        output_text = 'egrep "^' + title + str_end[:-1]
        print(output_text)


def __collection_update_info_to_text(all_movie_parsed_data, series_name):
    all_titles = ""
    for movie_data in all_movie_parsed_data:
        all_titles += movie_data[2] + "; "
    print(all_titles[:-2])
    print(series_name)
