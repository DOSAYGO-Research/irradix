import subprocess
import sys

# Available tests and their corresponding Python files
TESTS = {
    "1": ("Test irradix/derradix conversion", "ta1.py"),
    "2": ("Test no '101' sequence in irradix", "ta2.py"),
    "3": ("Test packing sequences of random integers with encoding/decoding", "ta3.py"),
    "4": ("Test irradix integer map and measure some properties", "ta4.py"),
}

def run_test(test_file):
    # Runs the selected test file
    subprocess.run([sys.executable, test_file])

def main():
    print("Available Tests:")
    for key, (description, _) in TESTS.items():
        print(f"{key}: {description}")

    choice = input("\nEnter the number of the test you want to run (or 'q' to quit): ").strip()

    if choice in TESTS:
        description, test_file = TESTS[choice]
        print(f"\nRunning {description}...")
        run_test(test_file)
    elif choice.lower() == 'q':
        print("Exiting...")
    else:
        print("Invalid choice. Please select a valid test number.")

if __name__ == "__main__":
    main()

