import csv
import time
from agent import Mouse
from environment import generate_maze
from levels import MAZE_SIZES

# List of AI methods to test
AI_METHODS = [
    ("random", False), ("random", True),
    ("greedy", False), ("greedy", True),
    ("a_star", False), ("a_star", True),
    ("bfs", False), ("bfs", True),
    ("ucs", False), ("ucs", True)
]
NUM_RUNS = 30

# CSV Header
CSV_HEADER = ["level", "ai_method", "run", "steps", "time_ms", "cost", "success", "replans"]

def run_experiments():
    with open("results.csv", mode="w", newline="") as results_file, \
         open("results_summary.csv", mode="w", newline="") as summary_file:

        writer = csv.writer(results_file)
        summary_writer = csv.writer(summary_file)

        writer.writerow(["level", "ai_method", "run", "steps", "time_ms", "cost", "success", "replans", "fallbacks"])
        summary_writer.writerow(["level", "ai_method", "avg_steps", "avg_time_us", "avg_cost", "success_rate_percent", "avg_replans", "avg_fallbacks"])

        for level_index, maze_size in enumerate(MAZE_SIZES):
            print(f"\n=== Running experiments for Level {level_index + 1} ===")
            maze, actual_width, actual_height = generate_maze(*maze_size)
            cheese_pos = (actual_width - 1, actual_height - 1)

            for ai_method, is_noisy in AI_METHODS:


                total_steps = 0
                total_time_us = 0
                total_cost = 0
                success_count = 0
                total_replans = 0
                total_fallbacks = 0


                method_label = f"{ai_method}{'_noise' if is_noisy else ''}"


                for run in range(1, NUM_RUNS + 1):
                    mouse = Mouse(start_pos=(0, 0), noisy_perception=is_noisy)
                    mouse.set_mode(ai_method, cheese_pos, maze)

                    start_time = time.perf_counter()
                    steps = 0
                    
                    while mouse.position != cheese_pos and steps < 1000:
                        mouse.move(maze)
                        steps += 1

                    success = (mouse.position == cheese_pos)
                    elapsed_time_us = (time.perf_counter() - start_time) * 1_000_000
                    cost = mouse.get_total_cost()
                    total_replans += mouse.replans_due_to_noise
                    total_fallbacks += mouse.fallback_count

                    if mouse.failed_and_fallback and "_fallback" not in method_label:
                        method_label += "_fallback"
                        success = False

                    # Save results
                    writer.writerow([
                        level_index + 1,
                        method_label,
                        run,
                        steps,
                        round(elapsed_time_us, 2),
                        cost,
                        success,
                        mouse.replans_due_to_noise,
                        mouse.fallback_count
                    ])

                    # add up values for averaging
                    total_steps += steps
                    total_time_us += elapsed_time_us
                    total_cost += cost
                    if success:
                        success_count += 1

                    print(f"Level {level_index + 1}, {method_label}, Run {run}: {steps} steps, {round(elapsed_time_us, 2)}us,  Cost: {cost}, Success: {success}")

                print(f"\n>>> [LEVEL {level_index + 1}] {method_label.upper()} AVERAGES:")
                print(f"Average Steps: {round(total_steps / NUM_RUNS, 2)}")
                print(f"Average Time: {round(total_time_us / NUM_RUNS, 2)} us")
                print(f"Average Cost: {round(total_cost / NUM_RUNS, 2)}")
                print(f"Success Rate: {round(100 * success_count / NUM_RUNS, 1)}%\n")
                print(f"Average Replans Due to Noise: {round(total_replans / NUM_RUNS, 2)}\n")
                print(f"Average Fallbacks: {round(total_fallbacks / NUM_RUNS, 2)}\n")

                              
                summary_writer.writerow([
                    level_index + 1,
                    method_label,
                    round(total_steps / NUM_RUNS, 2),
                    round(total_time_us / NUM_RUNS, 2),
                    round(total_cost / NUM_RUNS, 2),
                    round(100 * success_count / NUM_RUNS, 1),
                    round(total_replans / NUM_RUNS, 2),
                    round(total_fallbacks / NUM_RUNS, 2)
                ])


if __name__ == "__main__":
    run_experiments()
