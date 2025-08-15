from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

pipe = pickle.load(open('pipe.pkl', 'rb'))

teams = ['Kolkata Knight Riders', 'Sunrisers Hyderabad', 'Punjab Kings', 'Delhi Capitals',
         'Gujarat Titans', 'Rajasthan Royals', 'Lucknow Super Giants', 'Chennai Super Kings',
         'Mumbai Indians', 'Royal Challengers Bengaluru']

match_type = ['League', 'Eliminator', 'Qualifier 1', 'Qualifier 2', 'Final']

cities = ['Bangalore', 'Chandigarh', 'Delhi', 'Mumbai', 'Kolkata', 'Jaipur',
          'Hyderabad', 'Chennai', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Rajkot', 'Kanpur', 'Indore', 'Bengaluru', 'Dubai', 'Sharjah',
          'Navi Mumbai', 'Lucknow', 'Guwahati', 'Mohali']

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    input_data = None
    form_values = {}  # Store form values for repopulation

    if request.method == 'POST':
        try:
            # Store all form values for repopulation
            form_values = request.form.to_dict()
            
            # Get and validate form data
            selected_match_type = request.form['match_type']
            selected_city = request.form['city']
            batting_team = request.form['batting_team']
            bowling_team = request.form['bowling_team']
            
            # Validate teams are different
            if batting_team == bowling_team:
                raise ValueError("Batting and Bowling teams must be different")
                
            # Convert and validate numerical inputs
            target = int(request.form['target'])
            target_overs = int(request.form['target_overs'])
            score = int(request.form['score'])
            wickets = int(request.form['wickets'])
            overs = int(request.form['overs'])
            balls = int(request.form['balls'])
            batsman_runs = int(request.form['batsman_runs'])
            batsman_strikerate = float(request.form['batsman_strikerate'])
            non_striker_runs = int(request.form['non_striker_runs'])
            non_striker_strikerate = float(request.form['non_striker_strikerate'])

            # Validate score doesn't exceed target
            if score >= target:
                raise ValueError("Current score must be less than target runs")
                
            # Validate overs/balls logic
            if overs >= target_overs:
                raise ValueError("Completed overs must be less than target overs")

            # Calculate match metrics
            runs_left = target - score
            balls_left = (target_overs * 6) - (overs * 6) - balls
            crr = round(score / (overs + balls / 6),2) if (overs!=0 or balls!=0) else 0
            rrr = round((runs_left * 6) / balls_left,2) if balls_left != 0 else 0

            # Prepare input for model
            input_df = pd.DataFrame({
                'city': [selected_city],
                'match_type': [selected_match_type],
                'target_runs': [target],
                'batting_team': [batting_team],
                'bowling_team': [bowling_team],
                'current_score': [score],
                'wickets': [wickets],
                'crr': [crr],
                'rrr': [rrr],
                'batter_total_runs': [batsman_runs],
                'batter_strikerate': [batsman_strikerate],
                'non_striker_runs': [non_striker_runs],
                'non_striker_strikerate': [non_striker_strikerate]
            })

            # Make prediction
            result = pipe.predict_proba(input_df)[0]
            prediction = {
                'batting_team': batting_team,
                'bowling_team': bowling_team,
                'bat_win': int(round(result[1] * 100, 0)),
                'bowl_win': int(round(result[0] * 100, 0))
            }
            
            input_data = {
                'remaining_runs': target-score,
                'remaining_balls': 6*(target_overs-overs)-balls,
                'crr': crr,
                'rrr': rrr,
                'batter_total_runs': batsman_runs,
                'batter_strikerate': batsman_strikerate,
                'non_striker_runs': non_striker_runs,
                'non_striker_strikerate': non_striker_runs
            }

        except ValueError as e:
            # Handle validation errors
            error_message = str(e)
            return render_template('index.html', 
                                teams=sorted(teams), 
                                match_type=match_type,
                                cities=sorted(cities), 
                                error=error_message,
                                form_values=form_values)

    return render_template('index.html', 
                         teams=sorted(teams), 
                         match_type=match_type,
                         cities=sorted(cities), 
                         prediction=prediction, 
                         input_data=input_data,
                         form_values=form_values)

if __name__ == '__main__':
    app.run(debug=True)