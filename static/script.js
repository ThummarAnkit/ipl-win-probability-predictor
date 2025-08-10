document.addEventListener('DOMContentLoaded', function() {
    // Initialize form validation and team selection
    initializeForm();
});

function initializeForm() {
    // Set initial max values based on target
    updateScoreMax();
    updateOversMax();
    
    // Validate team selection on form submission
    const form = document.querySelector('form');
    form.addEventListener('submit', function(e) {
        const battingTeam = document.getElementById('batting_team');
        const bowlingTeam = document.getElementById('bowling_team');
        
        if (battingTeam.value === bowlingTeam.value) {
            e.preventDefault();
            alert('Batting and Bowling teams must be different!');
            return false;
        }
        
        // Additional validation can be added here
        return true;
    });
}

function updateTeams(changed) {
    const battingSelect = document.getElementById('batting_team');
    const bowlingSelect = document.getElementById('bowling_team');
    
    // Reset all disabled options first
    Array.from(battingSelect.options).forEach(opt => opt.disabled = false);
    Array.from(bowlingSelect.options).forEach(opt => opt.disabled = false);
    
    // Disable the selected team in the opposite dropdown
    if (changed === 'batting' && battingSelect.value) {
        Array.from(bowlingSelect.options).forEach(option => {
            option.disabled = (option.value === battingSelect.value);
        });
    }
    
    if (changed === 'bowling' && bowlingSelect.value) {
        Array.from(battingSelect.options).forEach(option => {
            option.disabled = (option.value === bowlingSelect.value);
        });
    }
}

function updateScoreMax() {
    const targetInput = document.getElementById('target');
    const scoreInput = document.getElementById('score');
    
    if (targetInput.value) {
        scoreInput.max = targetInput.value - 1;
        scoreInput.placeholder = `0-${scoreInput.max}`;
        
        // Also update batsman runs max
        updateBatsmanScore();
    }
}

function updateOversMax() {
    const targetOversInput = document.getElementById('target_overs');
    const oversInput = document.getElementById('overs');
    
    if (targetOversInput.value) {
        oversInput.max = targetOversInput.value - 1;
        oversInput.placeholder = `0-${oversInput.max}`;
    }
}

function updateBatsmanScore(type) {
    const scoreInput = document.getElementById('score');
    const batsmanRunsInput = document.getElementById('batsman_runs');
    const nonStrikerRunsInput = document.getElementById('non_striker_runs');
    
    if (!scoreInput.value) return;
    
    if (!type) {
        // Initial update - set both max values
        batsmanRunsInput.max = scoreInput.value;
        nonStrikerRunsInput.max = scoreInput.value;
    } else if (type === 'batsman') {
        // Update non-striker max based on batsman runs
        nonStrikerRunsInput.max = scoreInput.value - batsmanRunsInput.value;
    } else if (type === 'nonStriker') {
        // Update batsman max based on non-striker runs
        batsmanRunsInput.max = scoreInput.value - nonStrikerRunsInput.value;
    }
}