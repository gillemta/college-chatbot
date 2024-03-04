from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

chatbot_messages = [
    "Welcome to College Enquiry Chatbot!",
    "Before we begin, could you please provide your information?",
    "What is your first name?"
]

questions = [
    "- Does the college have a football team?",
    "- Does it have Computer Science Major?",
    "- What is the in-state tuition?",
    "- Does it have on campus housing?"
]

user_info = {}

@app.route("/", methods=["GET"])
def index():
    global user_info
    user_info = {}
    return render_template("index.html")

@app.route("/message", methods=["POST"])
def handle_message():
    user_input = request.form.get("userInput")
    if user_input:
        if "first_name" not in user_info:
            user_info["first_name"] = user_input
            return jsonify({"response": f"Hello {user_input}! What is your last name?"})
        elif "last_name" not in user_info:
            user_info["last_name"] = user_input
            return jsonify({"response": "What is your email address?"})
        elif "email" not in user_info:
            user_info["email"] = user_input
            questions_message = "<br>".join(questions)
            return jsonify({"response": f"Thank you for providing your information. Here are some questions you can ask:<br>{questions_message}"})
        else:
            if user_input.lower() == "end":
                return jsonify({"response": "Thank you for using College Enquiry Chatbot! Here's a summary of your interaction:", "summary": get_summary()})
            else: 
                answer = handle_question(user_input)
                return jsonify({"response": answer})
    return jsonify({"response": "No message received"})

def handle_question(user_input):
    user_input = user_input.lower()
    if user_input == "does the college have a football team?":
        return "Yes, the team is called the UC Bearcats."
    elif user_input == "does it have a computer science major?":
        return "Yes, there is a computer science major that is offered"
    elif user_input == "what is the in-state tuition?":
        return "The in-state tuition cost for a full-time student is $14,452.00 per semester."
    elif user_input == "does it have on campus housing?":
        return "Yes, there are numerous options to pick from for on-campus housing."
    else:
        return "That is not a possible question, check spelling and punctuation."


@app.route("/initial_messages", methods=["GET"])
def get_initial_messages():
    return jsonify({"messages": chatbot_messages})


@app.route("/summary", methods=["GET"])
def get_summary():
    if len(user_info) == 3:
        summary = {
            "user_information": user_info,
            "chatbot_creator_information": {
                "first_name": "Tashan",
                "last_name": "Gillem",
                "school_email": "gillemta@mail.uc.edu"
            }
        }
        return summary
    else:
        return jsonify({"response": "User information incomplete"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)