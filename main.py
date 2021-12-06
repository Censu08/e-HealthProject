from Library.Recognizer import *
from Library.Dashboard import *
from Library.Benchmark_Game_Classification import *

while True:
    option = int(input("Enter option: "))
    if option == 0:
        break
    if option == 1:
        read_serious_games()
    if option == 2:
        real_validator()
    if option == 3:
        print_dashboard()
    if option == 4:
        run_benchmark_first_part()
    else:
        continue
    """
    option 5:
        benchmark_validation
    option 6:
        benchmark_validated_games
    option 7:
        find games according to the clinical field (learning category)
    """
