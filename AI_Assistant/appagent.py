from agent import execute_task


def main():
    print("\n=== 🤖 AI Research Agent ===\n")

    while True:
        task = input("Enter a task (or type 'exit'): ")

        if task.lower() == "exit":
            print("👋 Exiting...")
            break

        if not task.strip():
            continue

        print("\nPlanning task...\n")

        plan, result = execute_task(task)

        print("\n=== 📌 Agent Plan ===\n")
        print(plan)

        print("\n=== ✅ Agent Result ===\n")
        print(result)


if __name__ == "__main__":
    main()