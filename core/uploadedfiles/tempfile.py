    # ** Means it's required
    ''' 
    Network 
        POST request
            {
                "name": "Network 2"
            }
        PUT request
            {
                "name": "Network 2.5"
            }
        PATCH request 
        # Checks for surveys.key to see if the instance is method or organisation
            [{
                "name": "newmethod",
                "surveys": []
            }]
            or
            [{
                "name": "Organisation 3",
            }]
    
     Organisation 
        POST request
            {
                "name": "Organisation 2"
            }
        PUT request
            {
                "name": "Organisation 2.5"
            }
        PATCH request 
        # Checks for surveys.key to see if the instance is method or organisation
            [{
                "name": "newmethod",
                "surveys": []
            }]
            or
            [{
                "name": "Organisation 3",
            }]

    Survey
        POST request
        {
            "name": "Survey 1"
        }
    
    '''