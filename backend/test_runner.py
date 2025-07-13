import subprocess


def run_appwright_test(test_path: str) -> str:
    try:
        result = subprocess.run(
            ["npx", "appwright", "test", test_path],
            check=True,
            capture_output=True,
            text=True,
        )
        print("AppWright passed:\n", result.stdout)
        return "success"
    except subprocess.CalledProcessError as e:
        print("AppWright failed:\n", e.stdout, e.stderr)
        return "failed"

