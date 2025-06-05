def calculate_bmi(height, weight):

    # Convert the user's height to meters
    height_m = height / 100

    # Calculate the user's BMI
    bmi = weight / (height_m ** 2)

    # Determine the user's health status
    
    if bmi < 18.5: 
        health_status = 'You are underweight.' 
    elif bmi < 25:
        health_status = 'You are at a healthy weight.'
    elif bmi < 30:
        health_status = 'You are overweight.'
    else: 
        health_status = 'You are obese.'

    # Return the user's BMI and health status
    return round(bmi, 2), health_status