# Questions, options, and answers
questions = [
    "What is the capital of India?",
    "What is 5 + 3?",
    "What is the color of the sky?"
]

options = [
    ["A. Mumbai", "B. Delhi", "C. Chennai", "D. Kolkata"],
    ["A. 5", "B. 8", "C. 10", "D. 7"],
    ["A. Green", "B. Blue", "C. Red", "D. Yellow"]
]

answers = ["B", "B", "B"]  # correct options

score = []  # list to store results

print("=== QUIZ START ===\n")

for i in range(len(questions)):
    print(questions[i])
    
    for opt in options[i]:
        print(opt)
    
    user_answer = input("Your answer (A/B/C/D): ").upper()

    if user_answer == answers[i]:
        print("Correct!\n")
        score.append(1)   # 1 means correct
    else:
        print("Wrong!\n")
        score.append(0)   # 0 means wrong

# Final scoreboard
total_score = sum(score)

print("=== SCOREBOARD ===")
print("Your answers list:", score)
print("Total Score:", total_score, "/", len(questions))
