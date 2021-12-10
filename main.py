from Library.Benchmark.Benchmark_Game_Classification import run_benchmark_game_classification
from Library.Benchmark.Benchmark_Validator import run_validator_benchmark
from Library.Recognizer import read_serious_games, import_df
from Library.Validator import real_validator

while True:
    option = int(input("Enter option: "))
    if option == 0:
        break
    if option == 1:
        read_serious_games()
    if option == 2:
        real_validator()
    if option == 3:
        run_benchmark_game_classification()
    if option == 4:
        run_validator_benchmark()
    if option == 5:
        import_df()
    if option == 6:
        import_df()
        read_serious_games()
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
