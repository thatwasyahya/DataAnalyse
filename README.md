# Data Analysis for IPS & ASTRE Scores

This project provides a web-based data analysis tool for comparing student scores in the IPS and ASTRE programs. Using a Flask backend and an interactive frontend, it dynamically updates graphs and displays based on user input, allowing adjustments to score weights and importance levels to visualize student program preferences.

## Table of Contents
- [Demo](#demo)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Technologies Used](#technologies-used)
- [License](#license)

## Demo

You can view the live project at: [dataanalyse.onrender.com](https://dataanalyse.onrender.com)

## Features

- Dynamic data visualization using bar charts to display student IPS and ASTRE scores.
- Adjustable score weights and importance levels to influence the displayed data.
- Real-time updates of students likely to choose either IPS or ASTRE based on the current scores.
- Interactive control panel for filtering by field and hypothesis.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/thatwasyahya/DataAnalyse.git
   cd DataAnalyse
   ```

2. **Install dependencies**:
   This project requires Python and Flask. Install dependencies using:
   ```bash
   pip install pip install flask pandas gunicorn flask-cors
   ```

3. **Prepare Data Files**:
   Ensure `reponses_etudiants.csv` and `conditions.csv` are in the project directory, as they are essential for score calculations.

4. **Run the app locally**:
   ```bash
   python app.py
   ```
   Add this code to the end of app.py
   ```python
   if __name__ == '__main__':
     app.run(debug=True, port=9090)
   ```
   The app will start locally at `http://127.0.0.1:9090`.

## Usage

1. **Access the live app**:
   Visit [dataanalyse.onrender.com](https://dataanalyse.onrender.com) to view and interact with the application.

2. **Using the Controls**:
   - Select a program and hypothesis from the dropdowns.
   - Adjust weight and importance using the sliders, then click "Mettre à jour le graphique" to see updated scores.
   - View the number of students likely to choose each program based on the scores in the results section.

## API Documentation

### Endpoints

- **`GET /api/scores`**  
  Returns the calculated scores for each student, including `IPS_percentage` and `ASTRE_percentage`.

- **`GET /api/hypotheses`**  
  Returns a list of available hypotheses for the selected program (IPS or ASTRE).

- **`POST /api/updatedelta`**  
  Updates the weights and importance level for a specified hypothesis.  
  **Body Parameters**:
  - `filiere` (string): The program (e.g., `ips`, `astre`).
  - `hypothesis` (string): The selected hypothesis.
  - `weight` (number): New weight for the hypothesis.
  - `importance` (number): New importance level for the hypothesis.

- **`GET /api/results`**  
  Returns the count of students with over 50% preference for IPS and ASTRE programs.

## Technologies Used

- **Backend**: Flask, Pandas for data processing.
- **Frontend**: HTML, CSS, JavaScript, Highcharts for interactive graphs.
- **Hosting**: Render for deployment.

## License

This project is licensed under the APACH License.
