from flask import Flask, render_template, request, jsonify
import pandas as pd
import re
import os

app = Flask(__name__)

EXCEL_FILE = "GEU-fee.xlsx"


def get_courses():
    try:
        excel = pd.ExcelFile(EXCEL_FILE)
        return excel.sheet_names
    except Exception as e:
        print("Course Load Error:", e)
        return []


def calculate_percentage_from_marks(marks_text):
    try:

        numbers = re.findall(
            r'\d+(?:\.\d+)?',
            str(marks_text)
        )

        if not numbers:
            return 0

        marks = [
            float(x)
            for x in numbers
        ]

        percentage = (
            sum(marks) / len(marks)
        )

        return round(
            percentage,
            2
        )

    except Exception as e:

        print(
            "Percentage Error:",
            e
        )

        return 0


def get_best_scholarship(course, percentage):

    try:

        df = pd.read_excel(
            EXCEL_FILE,
            sheet_name=course,
            header=None
        )

        header_row = 2
        scholarship_row = 4

        best_scholarship = 0

        for col in range(2, df.shape[1]):

            try:

                slab_text = str(
                    df.iloc[header_row, col]
                )

                scholarship_text = str(
                    df.iloc[scholarship_row, col]
                )

                cutoff_match = re.search(
                    r'>=?\s*(\d+(\.\d+)?)',
                    slab_text
                )

                if not cutoff_match:
                    continue

                cutoff = float(
                    cutoff_match.group(1)
                )

                scholarship_match = re.search(
                    r'(\d+(?:,\d+)?(?:\.\d+)?)',
                    scholarship_text
                )

                if not scholarship_match:
                    continue

                scholarship = float(
                    scholarship_match.group(1).replace(",", "")
                )

                if percentage >= cutoff:

                    best_scholarship = max(
                        best_scholarship,
                        scholarship
                    )

            except Exception:
                continue

        return int(best_scholarship)

    except Exception as e:

        print(
            "Scholarship Error:",
            e
        )

        return 0


@app.route("/")
def home():

    return render_template(
        "index.html",
        courses=get_courses()
    )


@app.route("/calculate", methods=["POST"])
def calculate():

    try:

        data = request.get_json()

        marks_text = data.get(
            "marks",
            ""
        )

        percentage = calculate_percentage_from_marks(
            marks_text
        )

        course = data.get(
            "course",
            ""
        )

        scholarship = get_best_scholarship(
            course,
            percentage
        )

        return jsonify({
            "success": True,
            "percentage": percentage,
            "scholarship": scholarship
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })


if __name__ == "__main__":

    print("=" * 60)
    print("GEU Scholarship Calculator Started")
    print("Current Folder :", os.getcwd())
    print("Excel File     :", EXCEL_FILE)
    print("=" * 60)

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
