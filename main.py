from KakuroSolver import KakuroSolver
import time
if __name__ == '__main__':
    kakuroSolver = KakuroSolver()
    start_time = time.perf_counter()
    kakuroSolver.kakuro_solver()
    kakuroSolver.print_kakuro()
    end_time = time.perf_counter()
    print("Time elapsed: " + str(end_time - start_time))
