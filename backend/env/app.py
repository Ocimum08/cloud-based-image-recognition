from flask import Flask, request, jsonify
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

# ... Other imports as needed 

# Replace placeholders with your Azure credentials
subscription_key = "393e9efc71714cb9bcb6e0d81cd2927c"
endpoint = "https://surveillance-object-detection.cognitiveservices.azure.com/"

vision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

app = Flask(__name__)

def analyze_for_objects(image_file):
    # Open the image (adapt if image_file isn't a file-like object)
    with open(image_file, 'rb') as image_stream: 
        # Call Azure Object Detection API
        analysis = vision_client.analyze_image_in_stream(image_stream, visual_features=['Objects'])

        # Process the response
        detected_objects = []
        for obj in analysis.objects:
            detected_objects.append({
                'label': obj.object_property,
                'confidence': obj.confidence
            })
        return detected_objects  # Return the structured data
    
def analyze_for_faces(image_file):
    # Open the image (adapt if needed)
    with open(image_file, 'rb') as image_stream:
        # Call Azure Facial Recognition API
        analysis = vision_client.analyze_image_in_stream(
            image_stream, 
            visual_features=['Faces'] # Adjust the features if needed
        )

        # Process Azure's response 
        detected_faces = []
        for face in analysis.faces:
            detected_faces.append({
                'age': face.age,
                'gender': face.gender,
                # ... other facial attributes you want to include
            })
        return detected_faces
    
def analyze_for_license_plate(image_file):
    # ... Open the image ...
    with open(image_file, 'rb') as image_stream:
    # Call Azure License Plate Recognition Service
        analysis = vision_client.recognize_license_plates_in_stream(image_stream) 
    # Hypothetical example - adapt based on the actual service

    license_plates = []
    for plate in analysis.plates:  # Assuming 'plates' exists in the response
        license_plates.append({
            'text': plate.text,
            'confidence': plate.confidence
        }) 

    return license_plates

def analyze_for_counting_car(image_file):
    # ... Open the image ... 

    # Call Object Detection 
    analysis_results = analyze_for_objects(image_file)

    car_count = 0
    for obj in analysis_results:
        if obj['label'] == 'car': 
            car_count += 1

    return {'car_count': car_count}

def analyze_for_counting_people(image_file):
    # ... Open the image ... 

    # Call Object Detection 
    analysis_results = analyze_for_objects(image_file)

    people_count = 0
    for obj in analysis_results:
        if obj['label'] == 'person': 
            people_count += 1

    return {'people_count': people_count}

@app.route('/analyze', methods=['POST'])
def analyze_image():
    # ... (existing image retrieval) ...
    print("anything......")
    image_file = request.files['image'] # Access the image
    service_type = request.form.get('service') 

    try:
        if service_type == 'object-detection':
            analysis_results = analyze_for_objects(image_file)
        elif service_type == 'facial-recognition':
            analysis_results = analyze_for_faces(image_file)
        elif service_type == 'counting-car':
            analysis_results = analyze_for_counting_car(image_file)
        elif service_type == 'people-counting':
            analysis_results = analyze_for_counting_people(image_file)  
        # ... and so on
        return jsonify(analysis_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 
