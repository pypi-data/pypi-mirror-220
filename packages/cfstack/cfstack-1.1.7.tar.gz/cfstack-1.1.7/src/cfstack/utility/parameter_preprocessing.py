def parameter_preprocessing(inputs):
    transformed_parameters = []
    for parameter_key,parmaeter_value in inputs.items():
        transformed_parameters.append({
            "ParameterKey":parameter_key,
            "ParameterValue":parmaeter_value
        })
    return transformed_parameters